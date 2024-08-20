import os
import yaml

class FontConfig:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../fonts'))
    FONT_MAPPINGS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), './font_language_mappings.yml'))

    def __init__(self):
        """
        Initialize the FontConfig class by loading the font mappings from a YAML file.
        """
        with open(self.FONT_MAPPINGS_FILE, 'r', encoding='utf-8') as file:
            self.font_mappings = yaml.safe_load(file)

    def get_font_path(self, language_code):
        """
        Retrieve the font path for a given language code.

        Args:
            language_code (str): The language code.

        Returns:
            str: The full path to the corresponding font file.

        Raises:
            ValueError: If the language code or font is not found in the mappings.
        """
        font_name = self.font_mappings.get(language_code, {}).get('font')
        
        if not font_name:
            raise ValueError(f"Font for language code '{language_code}' is not supported or not found.")
        
        return os.path.join(self.BASE_DIR, font_name)

    def get_language_name(self, language_code):
        """
        Retrieve the language name for a given language code.

        Args:
            language_code (str): The language code.

        Returns:
            str: The name of the language corresponding to the language code.

        Raises:
            ValueError: If the language code is not found in the mappings.
        """
        if language_code not in self.font_mappings:
            raise ValueError(f"Language code '{language_code}' is not supported.")
        
        return self.font_mappings.get(language_code, {}).get('name', language_code)
