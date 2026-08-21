from fastapi import APIRouter
from api.health import router as health_router
from api.verification import router as verification_router
from api.claim import router as claim_router
from api.evidence import router as evidence_router
from api.predict_router import router as predict_router

api_router = APIRouter(prefix="/api")
api_router.include_router(health_router)
api_router.include_router(verification_router)
api_router.include_router(claim_router)
api_router.include_router(evidence_router)
api_router.include_router(predict_router)
