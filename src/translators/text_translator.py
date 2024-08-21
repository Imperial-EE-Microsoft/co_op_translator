from openai import AzureOpenAI
from src.config.base_config import Config
from src.utils.text_utils import gen_image_translation_prompt, remove_code_backticks, extract_yaml_lines

class TextTranslator:
    def __init__(self):
        self.client = self.get_openai_client()

    def get_openai_client(self):
        """
        Initialize and return an OpenAI client.

        Returns:
            AzureOpenAI: The initialized OpenAI client.
        """
        return AzureOpenAI(
            api_key=Config.AZURE_OPENAI_API_KEY,
            api_version=Config.AZURE_OPENAI_API_VERSION,
            base_url=f"{Config.AZURE_OPENAI_ENDPOINT}/openai/deployments/{Config.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME}"
        )

    def translate_image_text(self, text_data, target_language):
        """
        Translate text data using the Azure OpenAI API.

        Args:
            text_data (list): List of text lines to be translated.
            target_language (str): Target language for translation.

        Returns:
            list: List of translated text lines.
        """
        prompt = gen_image_translation_prompt(text_data, target_language)
        response = self.client.chat.completions.create(
            model=Config.AZURE_OPENAI_MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000
        )
        return extract_yaml_lines(remove_code_backticks(response.choices[0].message.content))