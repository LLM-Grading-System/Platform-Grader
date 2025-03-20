from typing import Annotated

from faststream import Depends

from src.infrastructure.minio.client import get_s3_client, Minio
from src.infrastructure.aiohttp.client import get_session, ClientSession
from src.infrastructure.langchain import get_llm, BaseChatModel


S3Client = Annotated[Minio, Depends(get_s3_client)]
HTTPClient = Annotated[ClientSession, Depends(get_session)]
LLM = Annotated[BaseChatModel, Depends(get_llm)]
