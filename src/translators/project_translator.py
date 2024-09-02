import logging
from pathlib import Path
import asyncio
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.prompt_template.prompt_template_config import PromptTemplateConfig
from src.translators import text_translator, image_translator
from src.config.base_config import Config
from src.config.constants import SUPPORTED_IMAGE_EXTENSIONS
from src.utils.file_utils import read_input_file, handle_empty_document, write_output_file
from src.utils.markdown_utils import load_mappings, generate_prompt_template

logger = logging.getLogger(__name__)

class ProjectTranslator:
    def __init__(self, language_codes, root_dir='.'):
        self.language_codes = language_codes.split()
        self.root_dir = Path(root_dir)
        self.translations_dir = self.root_dir / 'translations'
        self.image_dir = self.root_dir / 'translated_images'
        self.text_translator = text_translator.TextTranslator()
        self.image_translator = image_translator.ImageTranslator()
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
        for lang_code in self.language_codes:
            lang_dir = self.translations_dir / lang_code
            lang_dir.mkdir(parents=True, exist_ok=True)

    def translate_image(self, image_path, language_code):
        try:
            translated_image_path = self.image_translator.translate_image(image_path, language_code, self.image_dir)
            logger.info(f"Translated image {image_path} to {language_code} and saved to {translated_image_path}")
        except Exception as e:
            logger.error(f"Failed to translate image {image_path}: {e}")

    async def process_all_markdown_files(self):
        tasks = []
        for md_file in self.root_dir.glob('**/*.md'):
            for language_code in self.language_codes:
                tasks.append(self.translate_markdown_file(md_file, language_code, language_code))
        await asyncio.gather(*tasks)

    def process_all_image_files(self):
        for image_file in self.root_dir.glob('**/*'):
            if image_file.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS:
                for language_code in self.language_codes:
                    self.translate_image(image_file, language_code)

    async def translate_markdown(self, file_path, output_lang, language_code):
        """
        Translate a Markdown file, update image links, and save the translated content.

        Args:
            file_path (Path): The file path of the Markdown document to translate.
            output_lang (str): The target language for translation.
            language_code (str): The language code for updating image links.
        """
        try:
            # Step 1: Read the content of the file
            document = read_input_file(file_path)
            if not document:
                # Handle empty document by copying the input file to output path
                relative_path = file_path.relative_to(self.root_dir)
                output_file = self.translations_dir / language_code / relative_path
                handle_empty_document(file_path, output_file)
                return

            # Step 2: Process the document into chunks and generate prompts
            document_chunks = self._process_markdown(document)
            prompts = [generate_prompt_template(output_lang, chunk, self._is_rtl(output_lang)) for chunk in document_chunks]

            # Step 3: Run the prompts and get the translated content
            results = await self._run_prompts(prompts)
            translated_content = "\n".join(results)

            # Step 4: Update image links in the translated content
            docs_dir = self.root_dir / 'docs'
            updated_content = text_translator.update_image_link(file_path, translated_content, language_code, docs_dir)

            # Step 5: Save the final translated content with updated links
            relative_path = file_path.relative_to(self.root_dir)
            translated_path = self.translations_dir / language_code / relative_path
            translated_path.parent.mkdir(parents=True, exist_ok=True)
            write_output_file(translated_path, [updated_content])

            # Step 6: Add a disclaimer to the final document
            await self._add_disclaimer(output_lang, translated_path)

            logger.info(f"Translated {file_path} to {language_code} and saved to {translated_path}")

        except Exception as e:
            logger.error(f"Failed to translate {file_path}: {e}")


    def _is_rtl(self, output_lang):
        mappings = load_mappings(self.root_dir)
        return mappings.get(output_lang, {}).get('rtl', False)

    async def _run_prompts(self, prompts):
        tasks = [self._run_prompt(prompt, i+1, len(prompts)) for i, prompt in enumerate(prompts)]
        return await asyncio.gather(*tasks)

    async def _run_prompt(self, prompt, index, total):
        logger.info(f"Running prompt {index}/{total}")
        req_settings = self.kernel.get_prompt_execution_settings_from_service_id("chat-gpt")
        req_settings.max_tokens = 4096
        req_settings.temperature = 0.7
        req_settings.top_p = 0.8

        prompt_template_config = PromptTemplateConfig(
            template=prompt,
            name="translate",
            description="Translate a text to another language",
            template_format="semantic-kernel",
            execution_settings=req_settings,
        )

        function = self.kernel.add_function(
            function_name="translate_function",
            plugin_name="translate_plugin",
            prompt_template_config=prompt_template_config,
        )

        return await self.kernel.invoke(function)

    async def _add_disclaimer(self, output_lang, output_file):
        disclaimer_prompt = generate_prompt_template(output_lang, "Disclaimer: The translation was translated from its original by an AI model and may not be perfect. Please review the output and make any necessary corrections.", self._is_rtl(output_lang))
        disclaimer = await self._run_prompt(disclaimer_prompt, 'disclaimer prompt', 1)
        write_output_file(output_file, [disclaimer])

    def translate_project(self):
        self.create_translation_directories()
        asyncio.run(self.process_all_markdown_files())
        self.process_all_image_files()
