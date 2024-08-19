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
            str: The full path to the corresponding font file. If the font for the given language is not found,
                 returns the default font path (NotoSans-Medium.ttf).
        """
        # Get the font name based on the language code. Use the default font if the language is not specified.
        font_name = self.font_mappings.get(language_code, {}).get('font', 'NotoSans-Medium.ttf')
        # Return the full path to the font file.
        return os.path.join(self.BASE_DIR, font_name)
