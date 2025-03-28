import logging

from fastapi import APIRouter, status

from app.axa_xl import services
from app.axa_xl.api_types import InsuranceQuoteResponse, InsuranceQuoteRequest

router = APIRouter()
logger = logging.getLogger()


@router.get("/healthcheck", status_code=status.HTTP_200_OK)
def get_health_check():
    return {"status": "fine"}


@router.post("/insurance-quote", response_model=InsuranceQuoteResponse)
async def new_insurance_quote_request(request: InsuranceQuoteRequest) -> InsuranceQuoteResponse:
    return await services.new_insurance_quote(request)
