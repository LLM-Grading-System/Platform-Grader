from typing import cast

from langchain_core.language_models import BaseChatModel

from src.infrastructure.langchain import grading_prompt, CriteriaFeedback


class LLMGrader:
    def __init__(self, llm: BaseChatModel) -> None:
        self._chain = grading_prompt | llm.with_structured_output(CriteriaFeedback)


    async def generate(self, system_prompt: str, user_prompt: str) -> CriteriaFeedback:
        result = await self._chain.ainvoke({"system_prompt": system_prompt, "user_prompt": user_prompt})
        return cast(CriteriaFeedback, result)
