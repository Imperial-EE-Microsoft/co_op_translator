"""
This module contains utility functions for handling Markdown content.
Functions include loading language mappings, generating translation prompts,
and processing specific Markdown structures such as comments and URLs.
"""
import os
import re
import tiktoken
from pathlib import Path
from urllib.parse import urlparse
import logging
from co_op_translator.config.constants import SUPPORTED_IMAGE_EXTENSIONS
from co_op_translator.utils.file_utils import generate_translated_filename, get_actual_image_path

logger = logging.getLogger(__name__)

def generate_prompt_template(output_lang: str, document_chunk: str, is_rtl: bool) -> str:
    """
    Generate a translation prompt for a document chunk, considering language direction.

    Args:
        output_lang (str): The target language for translation.
        document_chunk (str): The chunk of the document to be translated.
        is_rtl (bool): Whether the target language is right-to-left.

    Returns:
        str: The generated translation prompt.
    """

    # Check if there is only one line in the document
    if len(document_chunk.split("\n")) == 1:
        # Generate prompt for single line translation
        prompt = f"Translate the following text to {output_lang}. NEVER ADD ANY EXTRA CONTENT OUTSIDE THE TRANSLATION. TRANSLATE ONLY WHAT IS GIVEN TO YOU.. MAINTAIN MARKDOWN FORMAT\n\n{document_chunk}"
    else:
        prompt = f"""
        Translate the following markdown file to {output_lang}.
        Make sure the translation does not sound too literal. Make sure you translate comments as well.
        Do not translate  any XML or HTML tags.
        Do not translate any [!NOTE], [!WARNING], [!TIP], [!IMPORTANT], or [!CAUTION].
        Do not translate any entities, such as variable names, function names, or class names, but keep them in the file.
        Do not translate any urls or paths, but keep them in the file.
        """

    if is_rtl:
        prompt += "Please write the output from right to left, respecting that this is a right-to-left language.\n"
    else:
        prompt += "Please write the output from left to right.\n"

    # Append the actual document chunk to be translated
    prompt += "\n" + document_chunk

    return prompt

def get_tokenizer(encoding_name: str):
    """
    Get the tokenizer based on the encoding name.

    Args:
        encoding_name (str): The name of the encoding.

    Returns:
        tiktoken.Encoding: The tokenizer for the given encoding.
    """
    return tiktoken.get_encoding(encoding_name)

def count_tokens(text: str, tokenizer) -> int:
    """
    Count the number of tokens in a given text using the tokenizer.

    Args:
        text (str): The text to tokenize.
        tokenizer (tiktoken.Encoding): The tokenizer to use.

    Returns:
        int: The number of tokens in the text.
    """
    return len(tokenizer.encode(text))

def split_markdown_content(content: str, max_tokens: int, tokenizer) -> list:
    """
    Split the markdown content into smaller chunks based on code blocks, blockquotes, or HTML.

    Args:
        content (str): The markdown content to split.
        max_tokens (int): The maximum number of tokens allowed per chunk.
        tokenizer: The tokenizer to use for counting tokens.

    Returns:
        list: A list of markdown chunks.
    """
    chunks = []
    block_pattern = re.compile(r'(```[\s\S]*?```|<.*?>|(?:>\s+.*(?:\n>.*|\n(?!\n))*\n?)+)')
    parts = block_pattern.split(content)
    
    current_chunk = []
    current_length = 0

    for part in parts:
        part_tokens = count_tokens(part, tokenizer)
        
        if current_length + part_tokens <= max_tokens:
            current_chunk.append(part)
            current_length += part_tokens
        else:
            if block_pattern.match(part):
                if current_chunk:
                    chunks.append(''.join(current_chunk))
                chunks.append(part)
                current_chunk = []
                current_length = 0
            else:
                words = part.split()
                for word in words:
                    word_tokens = count_tokens(word + ' ', tokenizer)
                    if current_length + word_tokens > max_tokens:
                        chunks.append(''.join(current_chunk))
                        current_chunk = [word + ' ']
                        current_length = word_tokens
                    else:
                        current_chunk.append(word + ' ')
                        current_length += word_tokens

    if current_chunk:
        chunks.append(''.join(current_chunk))

    return chunks

def process_markdown(content: str, max_tokens=4096, encoding='o200k_base') -> list: # o200k_base is for GPT-4o, cl100k_base is for GPT-4 and GPT-3.5
    """
    Process the markdown content to split it into smaller chunks.

    Args:
        content (str): The markdown content to process.
        max_tokens (int): The maximum number of tokens allowed per chunk.
        encoding (str): The encoding to use for the tokenizer.

    Returns:
        list: A list of processed markdown chunks.
    """
    tokenizer = get_tokenizer(encoding)
    chunks = split_markdown_content(content, max_tokens, tokenizer)

    for i, chunk in enumerate(chunks):
        chunk_tokens = count_tokens(chunk, tokenizer)
        logger.info(f"Chunk {i+1}: Length = {chunk_tokens} tokens")
        if chunk_tokens == max_tokens:
            logger.warning("Warning: This chunk has reached the maximum token limit.")

    return chunks

def update_image_link(md_file_path: Path, markdown_string: str, language_code: str, root_dir: Path) -> str:
    logger.info("UPDATING IMAGE LINKS")
    pattern = r'!\[(.*?)\]\((.*?)\)'  # Capture both alt text and link
    matches = re.findall(pattern, markdown_string)

    translations_dir = root_dir / 'translations'
    translated_images_dir = root_dir / 'translated_images'

    for alt_text, link in matches:
        parsed_url = urlparse(link)
        if parsed_url.scheme in ('http', 'https'):
            logger.info(f"Skipped {link} as it is a URL")
            continue  # Skip web URLs

        # Extract the path without query parameters
        path = parsed_url.path
        original_filename, file_ext = os.path.splitext(os.path.basename(path))

        if file_ext in SUPPORTED_IMAGE_EXTENSIONS:
            logger.info("This is an image")

            # Get the actual image path based on the markdown file path and the image link
            actual_image_path = get_actual_image_path(link, md_file_path)
            logger.info(f"Actual image path resolved: {actual_image_path}")

            # Determine the translated markdown file's path and translated image path
            translated_md_dir = translations_dir / language_code / md_file_path.relative_to(root_dir).parent

            # Calculate the relative path between translated markdown file and translated image
            rel_path = os.path.relpath(translated_images_dir, translated_md_dir)

            # Construct the new image path
            new_filename = generate_translated_filename(actual_image_path, language_code, root_dir)
            updated_link = os.path.join(rel_path, new_filename).replace(os.path.sep, '/')

            # Replace the image link in the markdown
            old_image_markup = f'![{alt_text}]({link})'
            new_image_markup = f'![{alt_text}]({updated_link})'
            markdown_string = markdown_string.replace(old_image_markup, new_image_markup)

            logger.info(f"Updated markdown_string: {markdown_string}")
        else:
            logger.info(f"File {link} is not an image. Skipping...")

    return markdown_string
