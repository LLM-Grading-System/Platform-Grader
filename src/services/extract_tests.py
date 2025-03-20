import zipfile
from io import BytesIO


class ProjectTestsSectionExtractor:
    SECTION_TITLE = "## Tests Logs (pytest)"
    FILENAME = "autotests.log"

    def __init__(self, content: BytesIO):
        self._content = content

    def generate(self) -> str:
        code_content = self._get_file_content(self._content)
        return self.SECTION_TITLE + "\n\n" + code_content

    @staticmethod
    def _get_file_content(content: BytesIO) -> str:
        with zipfile.ZipFile(content, 'r') as full_zip_ref:
            for file in full_zip_ref.filelist:
                if file.filename == ProjectTestsSectionExtractor.FILENAME:
                    with full_zip_ref.open(file) as code_file:
                        return code_file.read().decode(encoding="utf-8")
        raise ValueError(f"No {ProjectTestsSectionExtractor.FILENAME} in archive")
