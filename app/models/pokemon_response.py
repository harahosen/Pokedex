from pydantic import BaseModel, Field, StrictBool

class PokemonResponse(BaseModel):
    name: str
    description: str
    habitat: str
    is_legendary: StrictBool = Field(alias="isLegendary")

    model_config = {
        "validate_by_name": True
    }