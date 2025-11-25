import requests
from datetime import datetime


# -----------------------------
# UTILITY: API REQUEST WRAPPER
# -----------------------------
def fetch_json(url: str, timeout: int = 20):
    """Safe GET request wrapper."""
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Network/API error: {e}")
        return None


# -----------------------------
# GET COORDINATES FOR ANY CITY
# -----------------------------
def get_coordinates(city: str):
    """
    Fetch latitude & longitude for any city in India (or world)
    using Open-Meteo Geocoding API.
    """
    city = city.strip()

    if not city:
        print("❌ City name cannot be empty!")
        return None

    url = (
        "https://geocoding-api.open-meteo.com/v1/search"
        f"?name={city}&count=1&language=en&format=json"
    )

    data = fetch_json(url)
    if not data or "results" not in data or len(data["results"]) == 0:
        print(f"❌ Could not find city: {city}")
        return None

    result = data["results"][0]
    return {
        "name": result.get("name", city),
        "lat": result["latitude"],
        "lon": result["longitude"],
        "country": result.get("country", ""),
    }


# -----------------------------
# FETCH WEATHER DETAILS
# -----------------------------
def get_weather(city: str):
    """
    Fetch current weather using Open-Meteo.
    Works for ANY Indian city.
    """

    coords = get_coordinates(city)
    if not coords:
        return None

    lat, lon = coords["lat"], coords["lon"]
    city_name = coords["name"]

    print(f"\n🌤️ Fetching weather for {city_name} ({lat}, {lon})...")

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&current_weather=true&temperature_unit=celsius"
        "&hourly=relativehumidity_2m"
    )

    data = fetch_json(url)
    if not data or "current_weather" not in data:
        print("❌ Weather data unavailable!")
        return None

    current = data["current_weather"]
    temp = current["temperature"]
    wind = current["windspeed"]
    code = current["weathercode"]

    # Optional: Convert weather code → human-readable text
    weather_condition = WEATHER_CODES.get(code, "Unknown")

    now = datetime.now().strftime("%I:%M %p")

    print(
        f"""
╔══════════════════════════════════════╗
║     WEATHER UPDATE - {city_name}
╚══════════════════════════════════════╝
🌡️  Temperature : {temp}°C
💨 Wind Speed  : {wind} km/h
🌦️ Condition   : {weather_condition}
⏰ Time        : {now}
"""
    )

    # Alerts
    if temp > 35:
        print("🔥 ALERT: Very hot! Stay hydrated.")
    elif temp < 15:
        print("🧥 ALERT: Cold temperature! Wear warm clothes.")

    if code in [51, 61, 63, 80, 81]:
        print("🌧️ ALERT: Chance of rain. Carry an umbrella!")

    return data


# WEATHER CODE MEANINGS (Optional)
WEATHER_CODES = {
    0: "Clear",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Depositing Rime Fog",
    51: "Light Drizzle",
    61: "Light Rain",
    63: "Moderate Rain",
    65: "Heavy Rain",
    71: "Snowfall",
    95: "Thunderstorm",
    99: "Severe Thunderstorm",
}


# -----------------------------
# BONUS JOKE FUNCTION
# -----------------------------
def get_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    data = fetch_json(url, timeout=10)

    if not data:
        print("Couldn't fetch joke right now.")
        return

    print("\n😄 BONUS JOKE:")
    print(data["setup"])
    input("Press Enter for punchline...")
    print(f"👉 {data['punchline']}\n")


# -----------------------------
# MAIN PROGRAM
# -----------------------------
if __name__ == "__main__":
    print("=" * 55)
    print("     SIMPLE PYTHON AUTOMATION - WEATHER CHECKER")
    print("=" * 55)

    # Ask user for any Indian city
    user_city = input("\nEnter any city of India: ").strip()

    weather_data = get_weather(user_city)

    if weather_data:
        print("\n✅ Success! Weather data fetched.\n")
        get_joke()

    print("=" * 55)
