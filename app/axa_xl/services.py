import logging
import random

from app.axa_xl.api_types import InsuranceQuoteRequest, InsuranceQuoteResponse
from app.axa_xl.database.db_operations import ConnectionProvider, DbOperations
from app.axa_xl.database.types import InsuranceQuote

logger = logging.getLogger()


async def new_insurance_quote(request: InsuranceQuoteRequest) -> InsuranceQuoteResponse:
    """
    Generates new insurance quote for the request.
    :param request:
    :return: InsuranceQuoteResponse representing the calculated quote
    """
    logger.info("New insurance quote request",
                extra={"vehicle_registration": request.vehicle_registration})

    conn_provider = await ConnectionProvider.create()
    async with conn_provider.connection() as db_conn:
        discount = round(random.uniform(1, 20), 2)
        record = {
            "quote_amount": round(random.uniform(250, 5000), 2),
            "proposer": request.proposer,
            "is_business_use": request.is_business_use,
            "vehicle_registration": request.vehicle_registration,
            "agent_discount_amount": discount,
            "agent_notes": f"Random agent notes: {discount}"
        }
        result = await DbOperations.insert_record(InsuranceQuote, db_conn, record)
        response = InsuranceQuoteResponse(**result.dict())
        logger.info("Completing new insurance quote request",
                    extra={"vehicle_registration": request.vehicle_registration})
        return response
