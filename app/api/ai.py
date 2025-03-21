from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
from ..services.ai_service import AIService
from pydantic import BaseModel

router = APIRouter()
ai_service = AIService()

class DecisionRequest(BaseModel):
    context: Dict[str, Any]
    options: List[str]

class AnalysisRequest(BaseModel):
    data: Dict[str, Any]
    question: str

class RecommendationRequest(BaseModel):
    user_context: Dict[str, Any]

@router.post("/decision")
async def get_decision(request: DecisionRequest):
    try:
        result = await ai_service.get_decision(request.context, request.options)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze")
async def analyze_data(request: AnalysisRequest):
    try:
        result = await ai_service.analyze_data(request.data, request.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recommend")
async def get_recommendation(request: RecommendationRequest):
    try:
        result = await ai_service.get_recommendation(request.user_context)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 