from fastapi import FastAPI, Query
import requests
import os

# Load .env locally, skip if not found (e.g., in EC2)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = FastAPI()

API_KEY = os.getenv("API_KEY")  # Will work from .env locally or from GitHub Actions on EC2

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/version")
def version():
    return {
        "app": "weather-api",
        "version": os.getenv("APP_VERSION", "unknown"),
        "environment": os.getenv("ENVIRONMENT", "local")
    }


@app.get("/weather")
def get_weather(lat: float = Query(...), lon: float = Query(...)):
    if not API_KEY:
        return {"error": "API key missing"}
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    print(f"Calling: {url}")
    response = requests.get(url)
    return response.json()
