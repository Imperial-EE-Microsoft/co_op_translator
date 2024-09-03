import asyncio
import logging
import tempfile
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.prompt_template.prompt_template_config import PromptTemplateConfig
from src.utils.markdown_utils import process_markdown, update_image_link, generate_prompt_template
from src.config.base_config import Config 

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class MarkdownTranslator:
    def __init__(self, root_dir):
        """
        Initialize the MarkdownTranslator with the root directory.

        Args:
            root_dir (Path): The root directory of the project.
        """
        self.root_dir = root_dir
        self.kernel = self._initialize_kernel()

    def _initialize_kernel(self):
        """
        Initialize the semantic kernel with Azure OpenAI service.

        Returns:
            Kernel: Initialized semantic kernel.
        """
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

    async def translate_markdown(self, document, language_code, md_file_path):
        """
        Translate the markdown document to the specified language.

        Args:
            document (str): The content of the markdown file.
            language_code (str): The target language code.
            md_file_path (Path): The file path of the markdown file.

        Returns:
            str: The translated content with updated image links.
        """
        document_chunks = process_markdown(document)
        prompts = [generate_prompt_template(language_code, chunk, self._is_rtl(language_code)) for chunk in document_chunks]

        results = await self._run_prompts(prompts)
        translated_content = "\n".join(results)

        docs_dir = self.root_dir / 'docs'
        updated_content = update_image_link(md_file_path, translated_content, language_code, docs_dir)

        return updated_content

    async def _run_prompts(self, prompts):
        """
        Run the translation prompts asynchronously.

        Args:
            prompts (list): List of translation prompts.

        Returns:
            list: List of translated text chunks.
        """
        tasks = [self._run_prompt(prompt, i+1, len(prompts)) for i, prompt in enumerate(prompts)]
        return await asyncio.gather(*tasks)

    async def _run_prompt(self, prompt, index, total):
        """
        Execute a single translation prompt.

        Args:
            prompt (str): The translation prompt to execute.
            index (int): The index of the prompt.
            total (int): The total number of prompts.

        Returns:
            str: The translated text.
        """
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

    def _is_rtl(self, language_code):
        """
        Determine if the target language is right-to-left.

        Args:
            language_code (str): The language code to check.

        Returns:
            bool: True if the language is RTL, False otherwise.
        """
        mappings = load_mappings(self.root_dir)
        return mappings.get(language_code, {}).get('rtl', False)