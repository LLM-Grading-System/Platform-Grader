from dataclasses import dataclass
from src.infrastructure.langchain import criteria_based_chain, CriteriaOutput


@dataclass
class EstimationDTO:
    positive_feedback: str
    negative_feedback: str
    scrore: int
    is_passed: bool


class CriteriaBasedGrader:
    def __init__(self, criteria: str, criteria_description: str) -> None:
        self.criteria = criteria
        self.criteria_description = criteria_description
        self.__chain = criteria_based_chain

    def run(self, task_description: str, code: str) -> EstimationDTO:
        result: CriteriaOutput = self.__chain.invoke({
            "criteria": self.criteria,
            "criteria_description": self.criteria_description,
            "code": code,
            "task_description": task_description,
        })
        return EstimationDTO(
            positive_feedback=result.positive_feedback,
            negative_feedback=result.negative_feedback,
            scrore=result.score,
            is_passed=result.is_ok
        )
