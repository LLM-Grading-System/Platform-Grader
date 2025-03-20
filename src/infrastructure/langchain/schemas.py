from pydantic import BaseModel, Field


class CriteriaNote(BaseModel):
    name: str = Field(description="The essence of the criterion")
    problem: str = Field(default="", description="What is the problem with the code according to the criterion")
    is_met: bool = Field(description="If the code meets the criteria, return True, otherwise False")


class CriteriaFeedback(BaseModel):
    criteria: list[CriteriaNote] = Field(default=[])
    general_feedback: str = Field(description="General feedback about the code according to the criteria for student")
    general_grade: str = Field(description="General grade of student code: excellent, good, ok, bad")
