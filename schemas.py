
"""
Schemas for the credit scoring API.
"""
from pydantic import BaseModel, Field
from typing import Optional

class ApplicantRequest(BaseModel):
    name: str = Field(..., min_length=1, description="Applicant's full name")
    income: float = Field(..., gt=0, description="Annual income in dollars")
    age: int = Field(..., ge=18, le=100, description="Age in years")
    existing_loans: int = Field(..., ge=0, description="Number of existing loans")

class CreditScoreResponse(BaseModel):
    applicant_id: int
    credit_score: int
    explanation: str
    risk_level: str
