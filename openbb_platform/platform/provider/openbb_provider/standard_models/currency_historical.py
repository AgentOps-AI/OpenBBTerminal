"""Currency aggregate end of day price data model."""


from datetime import (
    date as dateType,
    datetime,
)
from typing import List, Optional, Set, Union

from dateutil import parser
from pydantic import Field, PositiveFloat, field_validator

from openbb_provider.abstract.data import Data
from openbb_provider.abstract.query_params import QueryParams
from openbb_provider.utils.descriptions import DATA_DESCRIPTIONS, QUERY_DESCRIPTIONS


class CurrencyHistoricalQueryParams(QueryParams):
    """Currency end of day Query."""

    symbol: str = Field(
        description=QUERY_DESCRIPTIONS.get("symbol", "")
        + " Can use CURR1-CURR2 or CURR1CURR2 format."
    )
    start_date: Optional[dateType] = Field(
        default=None,
        description=QUERY_DESCRIPTIONS.get("start_date", ""),
    )
    end_date: Optional[dateType] = Field(
        default=None,
        description=QUERY_DESCRIPTIONS.get("end_date", ""),
    )

    @field_validator("symbol", mode="before", check_fields=False)
    def validate_symbol(
        cls, v: Union[str, List[str], Set[str]]
    ):  # pylint: disable=E0213
        """Convert symbol to uppercase and remove '-'."""
        if isinstance(v, str):
            return v.upper().replace("-", "")
        return ",".join([symbol.upper().replace("-", "") for symbol in list(v)])


class CurrencyHistoricalData(Data):
    """Currency end of day price Data."""

    date: datetime = Field(description=DATA_DESCRIPTIONS.get("date", ""))
    open: PositiveFloat = Field(description=DATA_DESCRIPTIONS.get("open", ""))
    high: PositiveFloat = Field(description=DATA_DESCRIPTIONS.get("high", ""))
    low: PositiveFloat = Field(description=DATA_DESCRIPTIONS.get("low", ""))
    close: PositiveFloat = Field(description=DATA_DESCRIPTIONS.get("close", ""))
    volume: float = Field(description=DATA_DESCRIPTIONS.get("volume", ""))
    vwap: Optional[PositiveFloat] = Field(
        description=DATA_DESCRIPTIONS.get("vwap", ""), default=None
    )

    @field_validator("date", mode="before", check_fields=False)
    def date_validate(cls, v):  # pylint: disable=E0213
        """Return formatted datetime."""
        return parser.isoparse(str(v))