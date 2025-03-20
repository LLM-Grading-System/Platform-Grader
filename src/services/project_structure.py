import zipfile
from io import StringIO, BytesIO
from zipfile import ZipFile


class ProjectStructureSectionGenerator:
    SECTION_TITLE = "## Project Structure"

    def __init__(self, content: BytesIO):
        self._content = content

    def generate(self) -> str:
        zip_reference = self._get_zip_reference(self._content)
        file_paths = self._get_file_paths(zip_reference)
        project_structure = self._build_project_structure(file_paths)
        project_structure_string = self._stringify(project_structure)
        return self.SECTION_TITLE + "\n\n" + project_structure_string.strip()

    @staticmethod
    def _get_zip_reference(content: BytesIO) -> ZipFile:
        with zipfile.ZipFile(content, 'r') as full_zip_ref:
            for file in full_zip_ref.filelist:
                if file.filename == "code.zip":
                    with full_zip_ref.open(file) as code_file:
                        code_content = BytesIO(code_file.read())
                    with zipfile.ZipFile(code_content, 'r') as zip_ref:
                        return zip_ref
        raise ValueError("No code.zip in archive")

    @staticmethod
    def _get_file_paths(zip_reference: ZipFile) -> list[str]:
        return list(map(lambda file: file.filename, zip_reference.filelist))

    @staticmethod
    def _build_project_structure(file_paths: list[str]):
        project_structure = {}
        for file_path in file_paths:
            parts = file_path.split("/")
            current_level = project_structure
            for part in parts[:-1]:
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]
            file_name = parts[-1]
            current_level[file_name] = None
        return project_structure

    @staticmethod
    def _stringify(structure, indent=0, last=True):
        output = StringIO()
        items = list(structure.items())
        for index, (key, value) in enumerate(items):
            prefix = '└── ' if last and index == len(items) - 1 else '├── '
            output.write(' ' * indent + prefix + key + '\n')
            if isinstance(value, dict):
                output.write(ProjectStructureSectionGenerator._stringify(value, indent + 4, last=(index == len(items) - 1)))
        return output.getvalue()
