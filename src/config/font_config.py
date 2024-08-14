import os

class FontConfig:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../fonts'))

    # Define paths to all the fonts used in the project
    NOTO_SANS_MEDIUM = os.path.join(BASE_DIR, "NotoSans-Medium.ttf")

    # Define the default font
    DEFAULT = NOTO_SANS_MEDIUM

    @staticmethod
    def get_font_path(font_name):
        """
        Get the font path by name.

        Args:
            font_name (str): The name of the font attribute in the FontConfig class.

        Returns:
            str: The full path to the font file.
        """
        return getattr(FontConfig, font_name, None)
