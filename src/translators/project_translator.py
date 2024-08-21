from pathlib import Path

from src.translators import TextTranslator
from src.translators import ImageTranslator

class ProjectTranslator:
    def __init__(self, languages, root_dir='.'):
        self.languages = languages.split(',')
        self.root_dir = Path(root_dir)
        self.translations_dir = self.root_dir / 'translations'
        self.image_dir = self.root_dir / 'translated_images'
        self.text_translator = TextTranslator()
        self.image_translator = ImageTranslator()

    def create_translation_directories(self):
        for lang in self.languages:
            lang_dir = self.translations_dir / lang
            lang_dir.mkdir(parents=True, exist_ok=True)

    def translate_markdown_file(self, file_path, language):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        translated_content = self.text_translator.translate(content, language)
        
        relative_path = file_path.relative_to(self.root_dir)
        translated_path = self.translations_dir / language / relative_path
        translated_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(translated_path, 'w', encoding='utf-8') as file:
            file.write(translated_content)

    def translate_image(self, image_path, language):
        """
        Translate the text within an image to the target language and save it to the specified destination.

        Args:
            image_path (str): Path to the original image file.
            language (str): The target language for translation.
            destination_path (str, optional): The path where the translated image will be saved.
                                            If None, the image will be saved in the default directory.

        Returns:
            str: The path to the translated image.
        """
        # Determine the final destination path
        destination_path = self.image_dir

        # Translate the image
        translated_image_path = self.image_translator.translate_image(image_path, language, destination_path)
        
        return translated_image_path

    def process_all_markdown_files(self):
        for md_file in self.root_dir.glob('**/*.md'):
            for language in self.languages:
                self.translate_markdown_file(md_file, language)

    def process_all_image_files(self):
        for image_file in self.root_dir.glob('**/*.[png|jpg|jpeg]'):
            for language in self.languages:
                self.translate_image(image_file, language)

    def translate_project(self):
        self.create_translation_directories()
        self.process_all_markdown_files()
        self.process_all_image_files()
