from pydantic import BaseModel, Field
from typing import List, Optional


class JDOutput(BaseModel):
    role: str = "Unknown"
    skills: List[str] = Field(default_factory=list)
    experience_years: Optional[float] = 0
    must_have: List[str] = Field(default_factory=list)
    nice_to_have: List[str] = Field(default_factory=list)