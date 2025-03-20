from pydantic import BaseModel, Field


class TaskPromptResponseSchema(BaseModel):
    system_instructions: str = Field(examples=["Системная инструкция"])
