"""
This module contains utility functions for handling text and generating prompts.
Functions include generating translation prompts, processing responses from OpenAI, 
and updating image links in Markdown content.
"""

import re
import logging
import hashlib
from pathlib import Path
from urllib.parse import urlparse
from src.config.constants import SUPPORTED_IMAGE_EXTENSIONS

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) 

def gen_image_translation_prompt(text_data, language):
    """
    Generate a translation prompt for the given text data.
    
    Args:
        text_data (list): List of text lines to be translated.
        language (str): Target language for translation.
    
    Returns:
        str: Generated translation prompt.
    """
    prompt = f'''
    You are a translator that receives a batch of lines in an image. Given the following yaml file, please translate each line into {language}.
    For each line, fill it in with the translation, respecting the context of the text.
    Return only the yaml file, fully filled in.
    '''
    for line in text_data:
        prompt += f"- {line}\n"
    return prompt

def remove_code_backticks(message):
    """
    Remove code block backticks from a message.
    
    Args:
        message (str): The message containing code block backticks.
    
    Returns:
        str: The message without code block backticks.
    """
    match = re.match(r'```(?:\w+)?\n(.*?)\n```', message, re.DOTALL)
    return match.group(1) if match else message

def extract_yaml_lines(message):
    """
    Extract YAML lines from a message.
    
    Args:
        message (str): The message containing YAML lines.
    
    Returns:
        list: List of extracted YAML lines.
    """
    lines = message.split('\n')
    yaml_lines = [line[2:] for line in lines if line.startswith('- ')]
    return yaml_lines

def update_image_link(md_file_path, markdown_string, language_code, docs_dir):
    """
    Update image links in a Markdown string to point to translated images.

    This function scans through a Markdown string to find all image links and updates them
    to point to the corresponding translated images. The function generates a unique filename 
    for each image based on its original path, language code, and the hash of the image path.

    Args:
        md_file_path (Path): The file path of the Markdown file being processed. This is used to determine the relative paths for images.
        markdown_string (str): The content of the Markdown file as a string, where the image links need to be updated.
        language_code (str): The target language code (e.g., 'fr' for French) used to generate the translated image filenames.
        docs_dir (Path): The directory containing documentation files. This helps in determining if an image is part of the documentation.

    Returns:
        str: The updated Markdown content with modified image links pointing to the translated images.

    Example:
        Given a Markdown string containing an image link like:
        `![example](./images/sample.png)`, this function would update the link to point to 
        a translated version, such as `![example](../translated_images/sample.<hash>.fr.png)`.
    """
    logger.info("UPDATING IMAGE LINKS")
    pattern = r'!\[(.*?)\]\((.*?)\)'  # Capture both alt text and link
    matches = re.findall(pattern, markdown_string)

    for alt_text, link in matches:
        parsed_url = urlparse(link)
        if parsed_url.scheme in ('http', 'https'):
            logger.info(f"skipped {link} as it is a URL")
            continue  # Skip web URLs

        # Extract the path without query parameters
        path = Path(parsed_url.path)
        original_filename = path.stem
        file_ext = path.suffix

        logger.info(f"link: {link}, original_filename: {original_filename}, file_ext: {file_ext}")
        logger.info(f"#docs_dir: {docs_dir}, Doc? {md_file_path.is_relative_to(docs_dir)}")

        if file_ext in SUPPORTED_IMAGE_EXTENSIONS:
            logger.info("this is an image file")

            if md_file_path.is_relative_to(docs_dir):
                logger.info(f"this is a docs image for {md_file_path}")
                rel_levels = len(md_file_path.relative_to(docs_dir).parts) + 2
                translated_folder = Path('../' * rel_levels) / 'translated_images'
            else:  # is a readme image
                translated_folder = Path('./translated_images')

            md_file_dir = md_file_path.parent
            actual_image_path = (md_file_dir / path).resolve()
            hash = get_unique_id(actual_image_path)
            new_filename = f"{original_filename}.{hash}.{language_code}{file_ext}"
            updated_link = translated_folder / new_filename

            if not updated_link.is_absolute():
                updated_link = Path("/") / updated_link

            logger.info(f"updated_link: {updated_link}")
            new_image_markup = f'![{alt_text}]({updated_link})'
            markdown_string = re.sub(
                rf'!\[{re.escape(alt_text)}\]\({re.escape(link)}\)', 
                new_image_markup, 
                markdown_string
            )
            logger.info(f"markdown_string: {markdown_string}")
        else:
            logger.info(f"file {link} is not an image. Skipping...")

    return markdown_string

def get_unique_id(file_path):
    """
    Generate a unique SHA-256 hash for a given file path.

    Args:
        file_path (Path): The path of the file to hash.

    Returns:
        str: The SHA-256 hash of the file path.
    """
    file_path_bytes = str(file_path).encode('utf-8')
    hash_object = hashlib.sha256()
    hash_object.update(file_path_bytes)
    unique_identifier = hash_object.hexdigest()
    logger.info(f"Generated hash for {file_path}: {unique_identifier}")
    return unique_identifier
