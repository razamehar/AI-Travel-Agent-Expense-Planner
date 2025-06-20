from typing import List, Optional, Literal
from pydantic import BaseModel, Field, model_validator
from datetime import date

class Query(BaseModel):
    city: List[str] = Field(..., description="List of cities you plan to visit")
    duration: Optional[int] = Field(1, ge=1, description="Trip duration in days (default: 1, must be >= 1)")
    start_date: Optional[date] = Field(None, description="Preferred start date (YYYY-MM-DD)")
    end_date: Optional[date] = Field(None, description="Preferred end date (YYYY-MM-DD)")

    budget: Optional[float] = Field(None, ge=1, description="Total trip budget (must be >= 1)")
    from_currency: Literal["EUR"] = Field("EUR", description="Currency is fixed to EUR")
    to_currency: Optional[str] = Field("EUR", description="Currency to convert to for planning (default: EUR)")

    travelers: Optional[int] = Field(1, ge=1, description="Number of travelers (default: 1, must be >= 1)")
    trip_type: Optional[str] = Field(None, description="Trip type: e.g., family, honeymoon, adventure, etc.")

    interests: Optional[List[str]] = Field(
        None,
        description="Travel interests: e.g., museums, beaches, food, nightlife, hiking, etc."
    )

    accommodation: Optional[str] = Field(
        None,
        description="Preferred accommodation: e.g., hotel, hostel, Airbnb, guesthouse, etc."
    )

    miscellaneous: Optional[str] = Field(None, description="Other preferences or special requests")

    @model_validator(mode="after")
    def validate_dates_and_duration(self):
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValueError("End date cannot be before start date.")
            # Calculate duration is not provided or is None
            if self.duration is None:
                self.duration = (self.end_date - self.start_date).days + 1

        if self.to_currency is None:
            self.to_currency = "EUR"

        return self
