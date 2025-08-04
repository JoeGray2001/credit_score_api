"""
Credit scoring models to be used in a credit scoring API.
"""
from typing import Tuple

def calculate_credit_score(income: float, age: int, existing_loans: int) -> Tuple[int, str, str]:
    """
    Calculate credit score based on applicant data.
    Returns: (score, explanation, risk_level)
    """
    base_score = 500
    
    # Income factor (0-200 points)
    if income >= 100000:
        income_score = 200
    elif income >= 50000:
        income_score = 150
    elif income >= 30000:
        income_score = 100
    else:
        income_score = 50
    
    # Age factor (0-100 points)
    if age >= 35:
        age_score = 100
    elif age >= 25:
        age_score = 75
    else:
        age_score = 50
    
    # Existing loans penalty (0 to -150 points)
    loan_penalty = min(existing_loans * 30, 150)
    
    final_score = base_score + income_score + age_score - loan_penalty
    final_score = max(300, min(850, final_score))  # Clamp between 300-850
    
    # Risk level
    if final_score >= 700:
        risk_level = "Low"
    elif final_score >= 600:
        risk_level = "Medium"
    else:
        risk_level = "High"
    
    # Explanation
    explanation = f"Score based on: Income (${income:,.0f}), Age ({age}), Loans ({existing_loans})"
    
    return final_score, explanation, risk_level