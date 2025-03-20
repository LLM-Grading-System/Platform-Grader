from typing import cast

from langchain_core.language_models import BaseChatModel

from src.infrastructure.langchain import grading_prompt, CriteriaFeedback


class LLMGrader:
    def __init__(self, llm: BaseChatModel) -> None:
        self._chain = grading_prompt | llm.with_structured_output(CriteriaFeedback)

    async def generate(self, system_prompt: str, user_prompt: str) -> CriteriaFeedback:
        try:
            result = await self._chain.ainvoke({"system_prompt": system_prompt, "user_prompt": user_prompt})
        except Exception as ex:
            result = CriteriaFeedback(
                task="", files=[], criteria=[],
                general_feedback="Произошла ошибка во время оценки, свяжитесь пожалуйста с преподавателем",
                general_grade="error"
            )
        return cast(CriteriaFeedback, result)
