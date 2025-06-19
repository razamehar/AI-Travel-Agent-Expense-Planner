from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date

class Query(BaseModel):
    city: List[str] = Field(..., description="List of city names")
    duration: Optional[int] = Field(None, description="Trip duration in days")
    start_date: Optional[date] = Field(None, description="Start date of the trip")
    end_date: Optional[date] = Field(None, description="End date of the trip")
    budget: Optional[float] = Field(None, description="Total budget for the trip")
    from_currency: Optional[str] = Field("EUR", description="Currency to convert from (default: EUR)")
    to_currency: Optional[str] = Field(None, description="Currency to convert to")
    query: Optional[str] = Field(None, description="The actual query")
