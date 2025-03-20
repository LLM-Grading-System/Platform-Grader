import zipfile
from io import BytesIO


class ProjectCodeSectionGenerator:
    SECTION_TITLE = "## Project Code"

    def __init__(self, content: BytesIO):
        self._content = content

    def generate(self) -> str:
        code_content = self._get_zip_code_content(self._content)
        project_files = self._get_project_files(code_content)
        project_file_sections = [f"### {pf[0]}\n\n```\n{pf[1]}\n```" for pf in project_files]
        return self.SECTION_TITLE + "\n\n" + "\n\n".join(project_file_sections)

    @staticmethod
    def _get_zip_code_content(content: BytesIO) -> BytesIO:
        with zipfile.ZipFile(content, 'r') as full_zip_ref:
            for file in full_zip_ref.filelist:
                if file.filename == "code.zip":
                    with full_zip_ref.open(file) as code_file:
                        return BytesIO(code_file.read())
        raise ValueError("No code.zip in archive")

    @staticmethod
    def _get_project_files(code_content: BytesIO) -> list[tuple[str, str]]:
        project_files = []
        with zipfile.ZipFile(code_content, 'r') as zip_ref:
            for file in zip_ref.filelist:
                with zip_ref.open(file) as code_file:
                    code_content = code_file.read().decode(encoding="utf-8")
                project_files.append((file.filename, code_content))
        return project_files
