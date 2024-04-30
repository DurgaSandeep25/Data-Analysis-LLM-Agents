# Import things that are needed generically
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool

from typing import Optional, Type
import requests

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)


class CurrentWeatherInput(BaseModel):
    query: str = Field(description="should be a location name")


class CurrentWeatherTool(BaseTool):
    name = "current_weather"
    description = "useful for when you need to answer questions about current weather"
    args_schema: Type[BaseModel] = CurrentWeatherInput

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> dict:
        # API endpoint for current weather data by city name
        # attach your key here
        url = f"http://api.weatherapi.com/v1/current.json?key=your_key_here&q={query}&aqi=no"
        res = {}
        # return {"error": "error while fetching data, lets use some other tool to fetch weather details"}
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
            weather_data = response.json()
            res['query'] = query
            res['temperature'] = weather_data['current']['temp_c']
            res['feels_like'] = weather_data['current']['feelslike_c']
            res['wind'] = weather_data['current']['wind_mph']
            res['condition'] = weather_data['current']['condition']['text']
            print(f"Weather in {query}:")
            print(f"Temperature : {weather_data['current']['temp_c']}")
            print(f"Temperature feels like : {weather_data['current']['feelslike_c']}")
            print(f"Wind : {weather_data['current']['wind_mph']}")
            print(f"Overall Condition : {weather_data['current']['condition']['text']}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            
        return res

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
