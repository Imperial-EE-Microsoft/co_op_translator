import logging
from pathlib import Path
import asyncio
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from src.translators import text_translator, image_translator, markdown_translator
from src.config.base_config import Config
from src.config.constants import SUPPORTED_IMAGE_EXTENSIONS
from src.utils.file_utils import read_input_file, handle_empty_document, get_file_extension, filter_files

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class ProjectTranslator:
    def __init__(self, language_codes, root_dir='.'):
        self.language_codes = language_codes.split()
        self.root_dir = Path(root_dir)
        self.translations_dir = self.root_dir / 'translations'
        self.image_dir = self.root_dir / 'translated_images'
        self.text_translator = text_translator.TextTranslator()
        self.image_translator = image_translator.ImageTranslator(default_output_dir=self.image_dir)
        self.markdown_translator = markdown_translator.MarkdownTranslator(self.root_dir)
        self.kernel = self._initialize_kernel()

    def _initialize_kernel(self):
        kernel = Kernel()
        service_id = "chat-gpt"

        kernel.add_service(
            AzureChatCompletion(
                service_id=service_id,
                deployment_name=Config.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME,
                endpoint=Config.AZURE_OPENAI_ENDPOINT,
                api_key=Config.AZURE_OPENAI_API_KEY,
            )
        )
        return kernel

    def create_translation_directories(self):
        """
        Create necessary directories for storing translated files.
        """
        for lang_code in self.language_codes:
            lang_dir = self.translations_dir / lang_code
            lang_dir.mkdir(parents=True, exist_ok=True)

    async def translate_image(self, image_path, language_code):
        image_path = Path(image_path)
        try:
            translated_image_path = self.image_translator.translate_image(image_path, language_code, self.image_dir)
            logger.info(f"Translated image {image_path} to {language_code} and saved to {translated_image_path}")
        except Exception as e:
            logger.error(f"Failed to translate image {image_path}: {e}")

    async def translate_markdown(self, file_path, language_code):
        """
        Translate a markdown file to the specified language.

        Args:
            file_path (Path): Path to the markdown file to be translated.
            language_code (str): Target language code.
        """
        file_path = Path(file_path)
        try:
            document = read_input_file(file_path)
            if not document:
                relative_path = file_path.relative_to(self.root_dir)
                output_file = self.translations_dir / language_code / relative_path
                handle_empty_document(file_path, output_file)
                return

            translated_content = await self.markdown_translator.translate_markdown(document, language_code, file_path)
            relative_path = file_path.relative_to(self.root_dir)
            translated_path = self.translations_dir / language_code / relative_path
            translated_path.parent.mkdir(parents=True, exist_ok=True)

            with open(translated_path, "w", encoding='utf-8') as f:
                f.write(translated_content)
            logger.info(f"Translated {file_path} to {language_code} and saved to {translated_path}")

        except Exception as e:
            logger.error(f"Failed to translate {file_path}: {e}")

    async def process_all_markdown_files(self):
        """
        Process and translate all markdown files in the project directory.
        """
        tasks = []
        for md_file_path in self.root_dir.glob('**/*.md'):
            for language_code in self.language_codes:
                tasks.append(self.translate_markdown(md_file_path, language_code))
        await asyncio.gather(*tasks)

    async def process_all_image_files(self):
        tasks = []
        for image_file_path in filter_files(self.root_dir):
            if get_file_extension(image_file_path) in SUPPORTED_IMAGE_EXTENSIONS:
                for language_code in self.language_codes:
                    tasks.append(self.translate_image(image_file_path, language_code))
        await asyncio.gather(*tasks)

    async def translate_project_async(self):
        """
        Translate the project by processing both markdown and image files asynchronously.
        """
        self.create_translation_directories()
        await asyncio.gather(
            self.process_all_markdown_files(),
            self.process_all_image_files()
        )

    def translate_project(self):
        """
        Public method to start the project translation.
        """
        asyncio.run(self.translate_project_async())
