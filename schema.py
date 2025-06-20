from typing import List, Optional, Literal
from pydantic import BaseModel, Field, model_validator
from datetime import date

class Query(BaseModel):
    city: List[str] = Field(..., description="List of cities you plan to visit")
    duration: Optional[int] = Field(1, ge=1, description="Trip duration in days (default: 1, must be >= 1)")
    start_date: Optional[date] = Field(None, description="Preferred start date (YYYY-MM-DD)")
    end_date: Optional[date] = Field(None, description="Preferred end date (YYYY-MM-DD)")


    from_currency: Literal["EUR"] = Field("EUR", description="Currency is fixed to EUR")
    to_currency: str = Field("EUR", description="Currency given by the user")

    travelers: Optional[int] = Field(1, ge=1, description="Number of travelers (default: 1, must be >= 1)")

    # You can extend the allowed trip types here or keep as str for flexibility
    trip_type: Optional[Literal["solo", "family", "honeymoon", "adventure", "business", "other"]] = Field(
        None, description="Trip type: e.g., solo, family, honeymoon, adventure, business, other"
    )

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
            calculated_duration = (self.end_date - self.start_date).days + 1
            # If duration is missing or inconsistent, correct it
            if self.duration is None or self.duration != calculated_duration:
                self.duration = calculated_duration
        return self
