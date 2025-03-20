from langchain_core.prompts import ChatPromptTemplate


grading_prompt = ChatPromptTemplate(
    [
        (
            "system",
            "{system_prompt}"
        ),
        (
            "human",
            "{user_prompt}"
        ),
    ]
)
