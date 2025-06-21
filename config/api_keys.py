from dotenv import load_dotenv
import os

load_dotenv()

class APIKeysConfig:
    weather_api_key = os.getenv("WEATHER_API_KEY")
    foursquare_api_key = os.getenv("FOURSQUARE_API_KEY")
    forex_api_key = os.getenv("FOREX_API_KEY")
    hotels_api_key = os.getenv("HOTELS_API_KEY")
    hotels_secret_key = os.getenv("HOTELS_SECRET_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
