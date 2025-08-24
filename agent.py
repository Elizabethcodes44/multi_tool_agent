import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent 
import requests 

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get API key
API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city using OpenWeatherMap API."""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code != 200:
            return {"status":"error", "error_message": data.get("message", "API error")}
        
        # Extract info
        temp = data["main"] ["temp"]
        description = data["weather"][0]["description"]
        country = data["sys"]["country"]
        
        report = f"The weather in {city}, {country} is {description} with a temperature of {temp}°C."
        return {"status": "success", "report": report}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}

def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}


root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.5-flash",
    description=(
        "Agent to answer questions about the time and weather in a city."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city. "
    ),
    tools=[get_weather, get_current_time],
)
print(get_weather("Lagos"))