from fastapi import FastAPI

# internal dependencies
from routes import pokemon
from exceptions.handlers import register_exception_handlers

# Create FastAPI app
app = FastAPI(
    title="Pokédex API",
    description="Simple REST API to fetch and translate Pokémon information using PokéAPI and FunTranslations.",
    version="1.0.0",
)

# Include routes
app.include_router(pokemon.router)

# Register global exception handlers
register_exception_handlers(app)