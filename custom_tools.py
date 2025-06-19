from langchain.tools import tool
from typing import Union, List, Tuple, Dict
from langchain_community.tools import DuckDuckGoSearchResults
import requests
from dotenv import load_dotenv
import os

load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
FOURSQUARE_API_KEY = os.getenv("FOURSQUARE_API_KEY")
FOREX_API_KEY = os.getenv("FOREX_API_KEY")


@tool
def get_current_weather(city: str) -> Dict[str, Union[str, float, int]]:
    """
    Fetch the current weather data for a specified city using the WeatherAPI.

    Args:
        city (str): The name of the city to retrieve weather information for.

    Returns:
        dict: A dictionary containing:
            - location (str): The city name.
            - country (str): The country name.
            - temperature_c (float): The current temperature in Celsius.
            - condition (str): The current weather condition description.
            - humidity (int): The current humidity percentage.
            - wind_kph (float): The wind speed in kilometers per hour.
            - error (str, optional): An error message if the API call fails.
    """
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        return {
            "location": data["location"]["name"],
            "country": data["location"]["country"],
            "temperature_c": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"],
            "humidity": data["current"]["humidity"],
            "wind_kph": data["current"]["wind_kph"]
        }
    else:
        return {
            "error": data.get("error", {}).get("message", "Failed to fetch data")
        }


@tool
def get_weather_forecast(city: str, days: int = 3) -> Dict[str, Union[str, list]]:
    """
    Retrieve the weather forecast for a specified city over a number of days using the WeatherAPI.

    Args:
        city (str): The name of the city for which to get the weather forecast.
        days (int): The number of days to forecast (default is 3; max typically 10).

    Returns:
        dict: A dictionary containing:
            - location (str): The city name.
            - country (str): The country name.
            - forecast (list): A list of dictionaries for each day containing:
                - date (str): The forecast date.
                - max_temp_c (float): The maximum temperature in Celsius.
                - min_temp_c (float): The minimum temperature in Celsius.
                - condition (str): The weather condition description.
                - chance_of_rain (str or int): The chance of rain percentage.
            - error (str, optional): An error message if the API call fails.
    """
    url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={city}&days={days}&aqi=no&alerts=no"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        forecast_days = []
        for day in data["forecast"]["forecastday"]:
            forecast_days.append({
                "date": day["date"],
                "max_temp_c": day["day"]["maxtemp_c"],
                "min_temp_c": day["day"]["mintemp_c"],
                "condition": day["day"]["condition"]["text"],
                "chance_of_rain": day["day"].get("daily_chance_of_rain", "N/A")
            })
        return {
            "location": data["location"]["name"],
            "country": data["location"]["country"],
            "forecast": forecast_days
        }
    else:
        return {
            "error": data.get("error", {}).get("message", "Failed to fetch forecast")
        }


@tool
def get_top_attractions(city: str) -> Union[List[Tuple[str, str]], str]:
    """
    Get a list of top attractions in a specified city using the Foursquare Places API.

    Args:
        city (str): The city to find attractions in.

    Returns:
        Union[List[Tuple[str, str]], str]:
            - On success: List of tuples containing (attraction_name, address).
            - On failure: Error message string describing the issue.
    """
    api_key = os.getenv("FOURSQUARE_API_KEY")
    if not api_key:
        return "Foursquare API key not found. Please set the FOURSQUARE_API_KEY environment variable."

    # Endpoint to get places in city (using text search with category 'attractions')
    url = "https://api.foursquare.com/v3/places/search"

    headers = {
        "Accept": "application/json",
        "Authorization": api_key
    }

    params = {
        "query": "attractions",
        "near": city,
        "limit": 10,
        "sort": "POPULARITY"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        results = []
        for place in data.get("results", []):
            name = place.get("name")
            location = place.get("location", {})
            address = location.get("formatted_address") or ", ".join(filter(None, [
                location.get("address"),
                location.get("locality"),
                location.get("region"),
                location.get("country")
            ]))
            if name and address:
                results.append((name, address))

        if not results:
            return f"No attractions found in {city}."

        return results

    except requests.RequestException as e:
        return f"Error retrieving data from Foursquare API: {str(e)}"


@tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """
    Convert a monetary amount from one currency to another by searching DuckDuckGo.

    This function performs a search to find the conversion rate and returns a snippet
    containing both currency codes and the converted amount if available.

    Args:
        amount (float): The amount of money to convert.
        from_currency (str): The source currency code (e.g., "USD").
        to_currency (str): The target currency code (e.g., "EUR").

    Returns:
        str: A snippet containing conversion information or "Conversion not found."
    """
    search = DuckDuckGoSearchResults(output_format='list')
    query = f"{amount} {from_currency} to {to_currency}"
    results = search.invoke(query)
    if not results:
        return "Conversion not found."
    for item in results:
        title = item.get("title", "").strip()
        snippet = item.get("snippet", "")
        if from_currency in snippet and to_currency in snippet:
            return snippet
    return "Conversion not found."


@tool
def get_accommodation(city: str) -> List[str]:
    """
    Retrieve a list of accommodation options such as hotels in the specified city
    by searching DuckDuckGo.

    Returns up to five results containing hotel names and brief details like ratings,
    prices per night, addresses, or websites.

    Args:
        city (str): The city to search accommodation options in.

    Returns:
        List[str]: Up to five strings with hotel title and a short snippet of details.
    """
    search = DuckDuckGoSearchResults(output_format='list')
    query = f"hotels in {city} with ratings, prices per night, addresses, and websites"
    results = search.invoke(query)
    accommodations = []
    for item in results:
        title = item.get("title", "").strip()
        snippet = item.get("snippet", "").strip()
        if title and snippet:
            accommodations.append(f"{title} - {snippet}")
        if len(accommodations) >= 5:
            break
    return accommodations


@tool
def get_travel_advisory(city: str) -> List[str]:
    """
    Retrieve travel advisories for a city including safety tips, scams, cultural norms,
    and weather concerns by searching DuckDuckGo.

    Returns up to five formatted advisories with title and description snippets.

    Args:
        city (str): The city for which to obtain travel advisory information.

    Returns:
        List[str]: Up to five strings with advisory titles and descriptions.
    """
    search = DuckDuckGoSearchResults(output_format='list')
    query = f"travel advisory {city} safety scams cultural norms weather"
    results = search.invoke(query)
    advisories = []
    for item in results:
        title = item.get("title", "").strip()
        snippet = item.get("snippet", "").strip()
        if title and snippet:
            advisories.append(f"{title} - {snippet}")
        if len(advisories) >= 5:
            break
    return advisories


@tool
def estimate_hotel_cost(price_per_night: float, total_days: int) -> float:
    """Calculate total hotel cost"""
    return price_per_night * total_days


@tool
def add_costs(cost1: float, cost2: float) -> float:
    """Add two costs together"""
    return cost1 + cost2


@tool
def multiply_costs(cost: float, multiplier: float) -> float:
    """Multiply cost by a multiplier"""
    return cost * multiplier


@tool
def calculate_total_expense(*costs: float) -> float:
    """Calculate total expense from multiple costs"""
    return sum(costs)


@tool
def calculate_daily_budget(total_cost: float, days: int) -> float:
    """Calculate daily budget"""
    return total_cost / days if days else 0