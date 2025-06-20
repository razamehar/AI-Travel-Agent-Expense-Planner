from datetime import datetime
from typing import Optional
from schema import *


from datetime import datetime
from typing import Optional, List

def ask_user_for_trip_info() -> Query:
    print("Let's plan your trip! Please answer the following questions.\n")

    def get_list_input(prompt: str) -> Optional[List[str]]:
        user_input = input(prompt).strip()
        return [item.strip() for item in user_input.split(",")] if user_input else None

    def get_optional_date(prompt: str) -> Optional[datetime.date]:
        date_str = input(prompt).strip()
        return datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None

    def get_optional_int(prompt: str, default: Optional[int] = None) -> Optional[int]:
        val = input(prompt).strip()
        return int(val) if val else default

    def get_optional_float(prompt: str) -> Optional[float]:
        val = input(prompt).strip()
        return float(val) if val else None

    def get_optional_str(prompt: str) -> Optional[str]:
        val = input(prompt).strip()
        return val if val else None

    cities = get_list_input("Enter the cities you plan to visit (comma-separated): ") or []

    start_date = get_optional_date("Enter your preferred start date (YYYY-MM-DD), or press Enter to skip: ")
    end_date = get_optional_date("Enter your preferred end date (YYYY-MM-DD), or press Enter to skip: ")

    duration = get_optional_int("Enter the duration of the trip in days (press Enter to auto-calculate): ")
    budget = get_optional_float("Enter your total trip budget (press Enter to skip): ")
    to_currency = get_optional_str("Enter your currency ((default is EUR): ")

    travelers = get_optional_int("How many people are traveling? (default is 1): ", default=1)
    trip_type = get_optional_str("Trip type (family, honeymoon, adventure, solo, business) [optional]: ")
    interests = get_list_input("Enter your interests (comma-separated: museums, beaches, food, nightlife, etc.) [optional]: ")
    accommodation = get_optional_str("Preferred accommodation (hotel, hostel, airbnb, guesthouse, resort, villa) [optional]: ")
    miscellaneous = get_optional_str("Any other preferences or requests? [optional]: ")

    return Query(
        city=cities,
        duration=duration,
        start_date=start_date,
        end_date=end_date,
        budget=budget,
        from_currency="EUR",
        to_currency=to_currency,
        travelers=travelers,
        trip_type=trip_type,
        interests=interests,
        accommodation=accommodation,
        miscellaneous=miscellaneous
    )