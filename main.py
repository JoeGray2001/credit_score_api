"""
This is the main.py for a FastAPI credit scoring API
"""
# main.py

"""
This is the main.py for a FastAPI credit scoring API
"""
from fastapi import FastAPI, HTTPException
from schemas import ApplicantRequest, CreditScoreResponse
from models import calculate_credit_score
from database import create_connection, create_tables, insert_applicant, DB_PATH
import logging
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    conn = create_connection(str(DB_PATH))
    create_tables(conn)
    conn.close()
    logging.info("Database initialized successfully")
    yield
    # Shutdown (if needed)

app = FastAPI(title="Credit Scoring API", version="1.0.0", lifespan=lifespan)

@app.post("/score", response_model=CreditScoreResponse)
async def score_applicant(applicant: ApplicantRequest):
    """Calculate credit score for an applicant."""
    try:
        # Store applicant in database
        conn = create_connection(str(DB_PATH))
        applicant_id = insert_applicant(
            conn, 
            applicant.name, 
            applicant.income, 
            applicant.age, 
            applicant.existing_loans
        )
        conn.close()
        
        # Calculate credit score
        score, explanation, risk_level = calculate_credit_score(
            applicant.income, 
            applicant.age, 
            applicant.existing_loans
        )
        
        return CreditScoreResponse(
            applicant_id=applicant_id,
            credit_score=score,
            explanation=explanation,
            risk_level=risk_level
        )
    
    except Exception as e:
        logging.error(f"Error processing applicant: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/")
async def root():
    return {"message": "Credit Scoring API is running"}