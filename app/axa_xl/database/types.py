from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel


class TableModel(BaseModel, ABC):
    @staticmethod
    @abstractmethod
    def table_name() -> str:
        pass


T = TypeVar("T", bound=TableModel)

from datetime import datetime
from decimal import Decimal


class InsuranceQuote(TableModel):
    id: int
    quote_amount: Decimal
    proposer: str
    vehicle_registration: str
    is_business_use: bool = False
    quote_date: datetime = None
    agent_discount_amount: Decimal = None
    agent_notes: str = None

    @staticmethod
    def table_name() -> str:
        return "insurance_quote"

