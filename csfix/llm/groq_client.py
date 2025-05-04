import logging
import os

from groq import Groq

from csfix.llm.llm_client import LLMClient

logger = logging.getLogger(__name__)


class GroqClient(LLMClient):
    def __init__(self, api_key: str, model: str):
        # Check if API key starts with "gsk_" which is the Groq key format
        if not api_key.startswith("gsk_"):
            logger.warning(
                "Warning: API key doesn't have expected Groq format (should start with 'gsk_')"
            )

        self.groq = Groq(api_key=api_key)
        self.model = model
        logger.debug("Groq client initialized with model: %s", model)

    def get_completion(self, messages: list[dict[str, str]]) -> str:
        try:
            response = self.groq.chat.completions.create(
                model=self.model, messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            # Check if API key is in environment directly as a backup
            if "Invalid API Key" in str(e) and os.environ.get("GROQ_API_KEY"):
                logger.debug("Trying fallback to GROQ_API_KEY environment variable...")
                try:
                    backup_client = Groq(api_key=os.environ["GROQ_API_KEY"])
                    response = backup_client.chat.completions.create(
                        model=self.model, messages=messages
                    )
                    return response.choices[0].message.content
                except Exception as fallback_error:
                    raise Exception(
                        f"Original error: {str(e)}\nFallback also failed: {str(fallback_error)}"
                    )
            raise
