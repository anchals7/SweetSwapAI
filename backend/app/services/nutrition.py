import os
import requests

USDA_SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"


def enrich_nutrition_data(drink_name: str) -> dict:
    api_key = os.getenv("NUTRITION_API_KEY")
    if not api_key:
        return {}

    response = requests.post(
        USDA_SEARCH_URL,
        json={
            "query": drink_name,
            "pageSize": 1,
            "requireAllWords": True,
        },
        params={"api_key": api_key},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    foods = data.get("foods", [])
    if not foods:
        return {}

    nutrients = foods[0].get("foodNutrients", [])
    sugar = next((n["value"] for n in nutrients if n.get("nutrientName") == "Sugars, total including NLEA"), None)
    caffeine = next((n["value"] for n in nutrients if n.get("nutrientName") == "Caffeine"), None)

    return {
        "sugar_grams": sugar,
        "caffeine_mg": caffeine,
        "data_source": "usda",
    }

