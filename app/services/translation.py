import requests

# internal dependenies
from utils.logger import logger
from exceptions.handlers import TranslationError
from utils.config import FUNTRANSLATION_URL

def translate_description(description: str, habitat: str, is_legendary: bool) -> str:
    """Translate Pokémon description using FunTranslations API with rules:
    - Yoda: if habitat == 'cave' or is_legendary
    - Shakespeare: otherwise
    - Fallback: original description if translation fails
    """
    if not description:
        return description

    # Rule-based translation type
    translation_type = "yoda" if habitat == "cave" or is_legendary else "shakespeare"

    try:
        response = requests.post(
            f"{FUNTRANSLATION_URL}{translation_type}.json",
            data={"text": description},
            timeout=5
        )

        if response.status_code != 200:
            logger.warning(f"Translation API ({translation_type}) returned {response.status_code}, "
                f"using original description."
            )
            # raise TranslationError(f"API returned {response.status_code}")

        data = response.json()
        #return data.get("contents", {}).get("translated", description)

        # validate the response structure
        translated = data.get("contents", {}).get("translated", description)
        if not translated:
            logger.warning(f"Translation API returned invalid payload for {translation_type}.")
            raise TranslationError("Malformed response from translation API")

        return translated

    except requests.RequestException as e:
        logger.error(f"Translation API request failed: {e}")
        #raise TranslationError(str(e))
        return description

    except ValueError as e:
        # JSON decoding issues → handled by exception middleware
        logger.error(f"Invalid JSON from translation API: {e}")
        raise TranslationError("Invalid response format from translation API")
