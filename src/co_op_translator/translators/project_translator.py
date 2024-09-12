import logging
import os
from pathlib import Path
import asyncio
from tqdm.asyncio import tqdm_asyncio
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from co_op_translator.translators import text_translator, image_translator, markdown_translator
from co_op_translator.config.base_config import Config
from co_op_translator.config.constants import SUPPORTED_IMAGE_EXTENSIONS, EXCLUDED_DIRS
from co_op_translator.utils.file_utils import read_input_file, handle_empty_document, get_filename_and_extension, filter_files, reset_translation_directories, generate_translated_filename, delete_translated_images_by_language_code, delete_translated_markdown_files_by_language_code

logger = logging.getLogger(__name__)

class ProjectTranslator:
    def __init__(self, language_codes, root_dir='.'):
        self.language_codes = language_codes.split()
        self.root_dir = Path(root_dir).resolve()
        self.translations_dir = self.root_dir / 'translations'
        self.image_dir = self.root_dir / 'translated_images'
        self.text_translator = text_translator.TextTranslator()
        self.image_translator = image_translator.ImageTranslator(default_output_dir=self.image_dir, root_dir=self.root_dir)
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

    async def translate_image(self, image_path, language_code):
        image_path = Path(image_path).resolve()
        if image_path.exists() and image_path.is_file():
            logger.info(f"Image exists: {image_path}")
            if os.access(image_path, os.R_OK):
                logger.info(f"Read permission granted for: {image_path}")
            else:
                logger.warning(f"Read permission denied for: {image_path}")
        else:
            logger.error(f"Image does not exist or is not a valid file: {image_path}")
        
        try:
            translated_image_path = self.image_translator.translate_image(image_path, language_code, self.image_dir)
            logger.info(f"Translated image {image_path} to {language_code} and saved to {translated_image_path}")
        except Exception as e:
            logger.error(f"Failed to translate image {image_path}: {e}", exc_info=True)

    async def translate_markdown(self, file_path, language_code):
        """
        Translate a markdown file to the specified language.

        Args:
            file_path (Path): Path to the markdown file to be translated.
            language_code (str): Target language code.
        """
        file_path = Path(file_path).resolve()
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

    async def translate_all_markdown_files(self, update=False):
        """
        Handles the markdown translation process. If update is True, it cleans the existing translated files
        before processing the markdown files. If update is False, it skips translating markdown files that already exist.
        """
        logger.info("Starting markdown translation tasks...")

        # Step 1: If update is True, delete all existing translated markdown files for the specified languages
        if update:
            for language_code in self.language_codes:
                delete_translated_markdown_files_by_language_code(language_code, self.translations_dir)
                logger.info(f"Deleted all translated markdown files for language: {language_code}")

        # Step 2: Gather markdown files for translation
        markdown_files = filter_files(self.root_dir, EXCLUDED_DIRS)
        tasks = []

        for md_file_path in markdown_files:
            md_file_path = md_file_path.resolve()

            # Check if the file extension is a markdown file
            if md_file_path.suffix == '.md':
                for language_code in self.language_codes:
                    relative_path = md_file_path.relative_to(self.root_dir)
                    translated_md_path = self.translations_dir / language_code / relative_path

                    if not update and translated_md_path.exists():
                        logger.info(f"Skipping already translated markdown file: {translated_md_path}")
                        continue  # Skip to the next markdown file

                    logger.info(f"Translating markdown file: {md_file_path} for language: {language_code}")
                    tasks.append(self.translate_markdown(md_file_path, language_code))

                    # If tasks reach 5 items, process them asynchronously and update the progress bar
                    if len(tasks) >= 5:
                        await tqdm_asyncio.gather(*tasks, total=len(tasks), desc="Translating markdown files")
                        tasks = []  # Reset tasks list after processing

        # Step 3: Process any remaining tasks
        if tasks:
            await tqdm_asyncio.gather(*tasks, total=len(tasks), desc="Translating remaining markdown files")
        else:
            logger.info("No markdown translation tasks to run.")


    async def translate_all_image_files(self, update=False):
        """
        Handles the image translation process. If update is True, it cleans the existing translated files
        before processing the images. If update is False, it skips translating images that already exist.
        """
        logger.info("Starting image translation tasks...")

        # Step 1: If update is True, delete all existing translated images for the specified languages
        if update:
            for language_code in self.language_codes:
                delete_translated_images_by_language_code(language_code, self.image_dir)
                logger.info(f"Deleted all translated images for language: {language_code}")

        # Step 2: Gather image files for translation
        image_files = filter_files(self.root_dir, EXCLUDED_DIRS)
        tasks = []

        for image_file_path in image_files:
            image_file_path = image_file_path.resolve()

            # Check if the file extension is a supported image format
            if get_filename_and_extension(image_file_path)[1] in SUPPORTED_IMAGE_EXTENSIONS:
                for language_code in self.language_codes:
                    translated_filename = generate_translated_filename(image_file_path, language_code, self.root_dir)
                    translated_image_path = Path(self.image_dir) / translated_filename

                    # If not updating, skip if the translated image already exists
                    if not update and translated_image_path.exists():
                        logger.info(f"Skipping already translated image: {translated_image_path}")
                        continue  # Skip to the next image file

                    # Translate the image and save it to the output directory
                    logger.info(f"Translating image: {image_file_path} for language: {language_code}")
                    tasks.append(self.translate_image(image_file_path, language_code))

                    # If tasks reach 5 items, process them asynchronously and update the progress bar
                    if len(tasks) >= 5:
                        await tqdm_asyncio.gather(*tasks, total=len(tasks), desc="Translating images")
                        tasks = []  # Reset tasks list after processing

        # Process any remaining tasks
        if tasks:
            await tqdm_asyncio.gather(*tasks, total=len(tasks), desc="Translating remaining images")
        else:
            logger.info("No image translation tasks to run.")



    async def translate_project_async(self, images=False, markdown=False, update=False):
        """
        Translate the project by processing both markdown and image files asynchronously.
        """
        logger.info("Starting project translation tasks...")

        # Step 1: Based on flags, process markdown and/or image files
        tasks = []
        
        # If neither images nor markdown is specified, translate both by default
        if not images and not markdown:
            images = True
            markdown = True
        
        # Process image translation
        if images:
            logger.info(f"Starting image translation tasks (update={update})...")
            tasks.append(self.translate_all_image_files(update=update))

        # Process markdown translation
        if markdown:
            logger.info(f"Starting markdown translation tasks (update={update})...")
            tasks.append(self.translate_all_markdown_files(update=update))

        # Step 2: Run tasks asynchronously
        if tasks:
            await asyncio.gather(*tasks)
        else:
            logger.warning("No tasks to run. Skipping translation.")

    def translate_project(self, images=False, markdown=False, update=False):
        """
        Public method to start the project translation.
        """
        asyncio.run(self.translate_project_async(images=images, markdown=markdown, update=update))
