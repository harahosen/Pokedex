from fastapi import APIRouter, HTTPException

# internal dependencies
from models.pokemon_response import PokemonResponse
from services import pokeapi, translation

router = APIRouter(prefix="/pokemon", tags=["Pokemon"])

@router.get("/{name}", response_model=PokemonResponse)
def get_pokemon(name: str):
    """Fetch basic Pokémon information."""
    pokemon = pokeapi.get_pokemon_data(name.lower())
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokémon not found")
    return pokemon

@router.get("/translated/{name}", response_model=PokemonResponse)
def get_translated_pokemon(name: str):
    """Fetch Pokémon info and translated description."""
    pokemon = pokeapi.get_pokemon_data(name.lower())
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokémon not found")

    pokemon["description"] = translation.translate_description(
        pokemon["description"], pokemon["habitat"], pokemon["isLegendary"]
    )
    
    return pokemon
