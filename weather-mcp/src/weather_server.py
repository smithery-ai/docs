"""
Weather MCP Server - Get weather data for any city
Built with FastMCP for simplicity
"""
from typing import Optional, Dict, Any
from datetime import datetime
from urllib.parse import quote
import httpx
import os
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP with metadata
mcp = FastMCP(
    "weather-server",
    version="1.0.0",
    description="Get real-time weather data for any city"
)

# Use a free weather API (no key required for demo)
WEATHER_API = "https://wttr.in"

@mcp.tool()
async def get_weather(
    city: str,
    units: str = "metric",
    detailed: bool = False
) -> Dict[str, Any]:
    """
    Get current weather for a city.
    
    Args:
        city: City name (e.g., "London", "New York")
        units: Temperature units - "metric" (°C) or "imperial" (°F)
        detailed: Include extended forecast and additional data
    
    Returns:
        Weather data including temperature, conditions, and optional forecast
    """
    # Validate inputs
    if not city:
        return {"error": "City name is required"}
    
    if units not in ["metric", "imperial"]:
        return {"error": "Units must be 'metric' or 'imperial'"}
    
    try:
        # Build API request
        params = {
            "format": "j1",  # JSON format
            "m": "" if units == "metric" else "f"  # Units
        }
        
        async with httpx.AsyncClient() as client:
            # URL encode city name to handle spaces and special characters
            encoded_city = quote(city)
            response = await client.get(
                f"{WEATHER_API}/{encoded_city}",
                params=params,
                timeout=10.0
            )
            response.raise_for_status()
            
        data = response.json()
        
        # Check if the response contains an error
        if isinstance(data, str) and "Unknown location" in data:
            return {"error": f"Unknown location: {city}"}
        
        if "current_condition" not in data or not data["current_condition"]:
            return {"error": f"No weather data available for {city}"}
            
        current = data["current_condition"][0]
        
        # Build response
        result = {
            "city": city,
            "temperature": f"{current['temp_C']}°C" if units == "metric" else f"{current['temp_F']}°F",
            "feels_like": f"{current['FeelsLikeC']}°C" if units == "metric" else f"{current['FeelsLikeF']}°F",
            "condition": current["weatherDesc"][0]["value"],
            "humidity": f"{current['humidity']}%",
            "wind": f"{current['windspeedKmph']} km/h" if units == "metric" else f"{current['windspeedMiles']} mph",
            "wind_direction": current["winddir16Point"],
            "uv_index": current["uvIndex"],
            "visibility": f"{current['visibility']} km" if units == "metric" else f"{current['visibilityMiles']} miles",
            "pressure": f"{current['pressure']} mb",
            "updated": datetime.now().isoformat()
        }
        
        # Add forecast if requested
        if detailed:
            forecast = []
            for day in data["weather"][:3]:  # Next 3 days
                forecast.append({
                    "date": day["date"],
                    "max_temp": f"{day['maxtempC']}°C" if units == "metric" else f"{day['maxtempF']}°F",
                    "min_temp": f"{day['mintempC']}°C" if units == "metric" else f"{day['mintempF']}°F",
                    "condition": day["hourly"][4]["weatherDesc"][0]["value"],  # Noon forecast
                    "rain_chance": f"{day['hourly'][4]['chanceofrain']}%"
                })
            result["forecast"] = forecast
            
        return result
        
    except httpx.HTTPStatusError as e:
        return {"error": f"Weather API error: {e.response.status_code}"}
    except Exception as e:
        return {"error": f"Failed to get weather: {str(e)}"}

@mcp.tool()
async def get_weather_alerts(
    city: str,
    severity: str = "all"
) -> Dict[str, Any]:
    """
    Get weather alerts and warnings for a city.
    
    Args:
        city: City name to check for alerts
        severity: Filter by severity - "all", "high", "medium", "low"
    
    Returns:
        Active weather alerts if any
    """
    # Simulated alerts for demo - in production, use a real alerts API
    alerts_db = {
        "miami": [
            {
                "type": "Hurricane Watch",
                "severity": "high",
                "description": "Tropical storm may strengthen to hurricane",
                "expires": "2024-09-15T18:00:00Z"
            }
        ],
        "denver": [
            {
                "type": "Winter Storm Warning",
                "severity": "medium",
                "description": "6-10 inches of snow expected",
                "expires": "2024-12-22T12:00:00Z"
            }
        ]
    }
    
    city_lower = city.lower()
    alerts = alerts_db.get(city_lower, [])
    
    # Filter by severity if specified
    if severity != "all":
        alerts = [a for a in alerts if a["severity"] == severity]
    
    return {
        "city": city,
        "alerts": alerts,
        "checked_at": datetime.now().isoformat()
    }

@mcp.tool()
async def compare_weather(
    cities: list[str],
    metric: str = "temperature"
) -> Dict[str, Any]:
    """
    Compare weather between multiple cities.
    
    Args:
        cities: List of cities to compare (max 5)
        metric: What to compare - "temperature", "humidity", "wind", "conditions"
    
    Returns:
        Comparison data for the specified metric
    """
    if len(cities) > 5:
        return {"error": "Maximum 5 cities for comparison"}
    
    if not cities:
        return {"error": "At least one city required"}
    
    comparisons = []
    
    for city in cities:
        weather = await get_weather(city, units="metric", detailed=False)
        if "error" not in weather:
            comparisons.append({
                "city": city,
                "temperature": weather["temperature"],
                "humidity": weather["humidity"],
                "wind": weather["wind"],
                "condition": weather["condition"]
            })
    
    # Sort by the requested metric
    if metric == "temperature":
        comparisons.sort(key=lambda x: float(x["temperature"].replace("°C", "")), reverse=True)
    elif metric == "humidity":
        comparisons.sort(key=lambda x: float(x["humidity"].replace("%", "")), reverse=True)
    elif metric == "wind":
        comparisons.sort(key=lambda x: float(x["wind"].split()[0]), reverse=True)
    
    return {
        "metric": metric,
        "cities": comparisons,
        "timestamp": datetime.now().isoformat()
    }

# Entry point for the server
if __name__ == "__main__":
    mcp.run()