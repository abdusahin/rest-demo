from datetime import datetime
from decimal import Decimal
from typing import Any, List

from pydantic import BaseModel, field_validator, model_validator, StrictBool


class InsuranceQuoteRequest(BaseModel):
    proposer: str
    vehicle_registration: str
    is_business_use: StrictBool = False

    @model_validator(mode='before')
    @classmethod
    def validate_model(cls, data: Any) -> Any:
        if 'proposer' not in data:
            raise ValueError("proposer is required")
        if 'vehicle_registration' not in data:
            raise ValueError("vehicle_registration is required")
        return data

    @field_validator('vehicle_registration')
    def validate_vehicle_registration(cls, value: str) -> str:
        trimmed_value = value.strip()
        if len(trimmed_value) < 1 or len(trimmed_value) > 10:
            raise ValueError("vehicle_registration must be between 1 and 10 characters")
        return trimmed_value

    @field_validator('proposer')
    def validate_proposer(cls, value: str) -> str:
        trimmed_value = value.strip()
        if len(trimmed_value) < 1 or len(trimmed_value) > 50:
            raise ValueError("proposer must be between 1 and 50 characters")
        return trimmed_value


class InsuranceQuoteResponse(BaseModel):
    id: int
    quote_amount: Decimal
    quote_date: datetime
    proposer: str
    vehicle_registration: str


class InsuranceQuotesResponse(BaseModel):
    quotes: List[InsuranceQuoteResponse]
