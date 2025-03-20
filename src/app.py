import json
from io import BytesIO

from faststream.asgi import AsgiFastStream

from src.api.dependencies import S3Client, HTTPClient, LLM
from src.api.events import SubmissionEventSchema, SUBMISSION_TOPIC, SUBMISSION_CONSUMER_GROUP
from src.infrastructure.faststream.app_with_healthcheck import create_app_with_health_check
from src.infrastructure.faststream.broker import add_broker
from src.services.extract_linters import ProjectLinterSectionExtractor
from src.services.extract_tests import ProjectTestsSectionExtractor
from src.services.llm_grader import LLMGrader
from src.services.project_code import ProjectCodeSectionGenerator
from src.services.project_structure import ProjectStructureSectionGenerator
from src.settings import app_settings


def create_application() -> AsgiFastStream:
    application = create_app_with_health_check()
    add_broker(application)
    return application


app = create_application()

@app.broker.subscriber(SUBMISSION_TOPIC, group_id=SUBMISSION_CONSUMER_GROUP, auto_commit=False)
async def handle_new_submission(data: SubmissionEventSchema, s3_client: S3Client, http_client: HTTPClient, llm: LLM) -> None:
    # Get assignment content
    s3_response = await s3_client.get_object(app_settings.MINIO_BUCKET, data.code_filename, http_client)
    s3_response_content = await s3_response.read()
    project_structure_section = ProjectStructureSectionGenerator(BytesIO(s3_response_content)).generate()
    project_code_section = ProjectCodeSectionGenerator(BytesIO(s3_response_content)).generate()
    project_tests_section = ProjectTestsSectionExtractor(BytesIO(s3_response_content)).generate()
    project_linters_section = ProjectLinterSectionExtractor(BytesIO(s3_response_content)).generate()

    # Get task
    get_task_endpoint_url = f"http://{app_settings.API_HOST}:{app_settings.API_PORT}/api/tasks/{data.task_id}/prompt"
    api_response = await http_client.get(get_task_endpoint_url)
    api_response_data = await api_response.json(encoding="utf-8")
    task_system_instructions_section = api_response_data["systemInstructions"]
    task_github_repo_url = api_response_data["githubRepoUrl"]

    # Get actual task description from GitHub
    organization, repo_name = task_github_repo_url.split("/")[-2:]
    readme_content_url = f"https://raw.githubusercontent.com/{organization}/{repo_name}/main/README.md"
    readme_response = await http_client.get(readme_content_url)
    readme_response_content = await readme_response.text(encoding="utf-8")

    # Prompts
    system_prompt = "\n\n".join([task_system_instructions_section, readme_response_content])
    user_prompt = "\n\n".join([project_tests_section, project_linters_section, project_structure_section, project_code_section])

    # Grading
    grader = LLMGrader(llm)
    result = await grader.generate(system_prompt, user_prompt)

    # Sending results
    update_submission_endpoint_url = f"http://{app_settings.API_HOST}:{app_settings.API_PORT}/api/submissions/{data.submission_id}"
    data = {
      "llmGrade": result.general_grade,
      "llmFeedback": result.general_feedback,
      "llmReport": result.model_dump()
    }
    submission_response = await http_client.put(update_submission_endpoint_url, json=data)
    submission_response_text = await submission_response.text(encoding="utf-8")
    print(submission_response_text)

    # with open("system_prompt.md", "w", encoding="utf-8") as f:
    #     f.write(system_prompt)
    # with open("user_prompt.md", "w", encoding="utf-8") as f:
    #     f.write(user_prompt)
    # with open("result.json", "w", encoding="utf-8") as f:
    #     result_json_string = json.dumps(result.model_dump())
    #     f.write(result_json_string)
