import requests

# internal dependencies
from utils.logger import logger
from exceptions.handlers import ExternalAPIError
from utils.config import POKEAPI_URL

def get_pokemon_data(name: str):
    try:
        response = requests.get(f"{POKEAPI_URL}{name.lower()}")
        if response.status_code != 200:
            logger.warning(f"PokéAPI returned {response.status_code} for {name}")
            raise ExternalAPIError("PokeAPI", response.status_code, f"Failed to fetch data for {name}")
        data = response.json()
    except requests.RequestException as e:
        logger.error(f"PokéAPI request failed: {e}")
        raise ExternalAPIError("PokeAPI", 503, str(e))

    # Extract English flavor text
    # taking the first one having the name of the language english
    description = next(
        (entry["flavor_text"].replace("\n", " ").replace("\f", " ")
         for entry in data["flavor_text_entries"]
         if entry["language"]["name"] == "en"),
        "No description available."
    )

    return {
        "name": data["name"],
        "description": description,
        "habitat": data["habitat"]["name"] if data["habitat"] else "unknown",
        "isLegendary": data["is_legendary"]
    }
