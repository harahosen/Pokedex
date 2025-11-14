import pytest
from pydantic import ValidationError

# internal dependencies
from app.models.pokemon_response import PokemonResponse

@pytest.mark.schema
def test_pokemon_response_validation_ok():
    payload = {
        "name": "mew",
        "description": "Cute",
        "habitat": "cave",
        "isLegendary": True
    }
    p = PokemonResponse(**payload)
    assert p.name == "mew"
    assert p.is_legendary is True

@pytest.mark.schema
def test_pokemon_response_validation_ko():
    # isLegendary must be bool
    try:
        PokemonResponse(**{"name": "mew","description":"x","habitat":"cave","isLegendary":"yes"})
        assert False, "Schema not valid"
    except ValidationError:
        assert True
