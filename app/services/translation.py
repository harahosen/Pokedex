import requests

# internal dependencies
from utils.logger import logger
from exceptions.handlers import TranslationError
from utils.config import FUNTRANSLATION_URL

def translate_description(description: str, habitat: str, is_legendary: bool) -> str:
    
    # 1. Yoda: if habitat == 'cave' or is_legendary
    # 2. Shakespeare: otherwise
    # 3. Fallback: original description if translation fails

    if not description:
        return description

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

        data = response.json()

        translated = data.get("contents", {}).get("translated", description)
        if not translated:
            logger.warning(f"Translation API returned invalid payload for {translation_type}.")
            raise TranslationError("Malformed response from translation API")

        return translated

    except requests.RequestException as e:
        logger.error(f"Translation API request failed: {e}")
        return description

    except ValueError as e:
        logger.error(f"Invalid JSON from translation API: {e}")
        raise TranslationError("Invalid response format from translation API")
