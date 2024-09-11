"""
This module contains utility functions for handling file operations.
Functions include reading from files, writing to files, and handling empty document scenarios.
"""

import hashlib
from pathlib import Path
import shutil
import os
import logging

logger = logging.getLogger(__name__)

def read_input_file(input_file: str | Path) -> str:
    """
    Read the content of an input file and return it as a stripped string.

    Args:
        input_file (str | Path): The path to the input file.

    Returns:
        str: The stripped content of the file.
    """
    input_file = Path(input_file)
    with input_file.open('r', encoding='utf-8') as file:
        return file.read().strip()

def handle_empty_document(input_file: str | Path, output_file: str | Path) -> None:
    """
    Copy the input file to the output location if the document is empty.

    Args:
        input_file (str | Path): The path to the input file.
        output_file (str | Path): The path to the output file.
    """
    input_file = Path(input_file)
    output_file = Path(output_file)
    shutil.copyfile(input_file, output_file)

def write_output_file(output_file: str | Path, results: list) -> None:
    """
    Write a list of results to the output file, each on a new line.

    Args:
        output_file (str | Path): The path to the output file.
        results (list): A list of strings to write to the file.
    """
    output_file = Path(output_file)
    with output_file.open('w', encoding='utf-8') as text_file:
        for result in results:
            text_file.write(result)
            text_file.write("\n")

def get_actual_image_path(image_relative_path: str | Path, markdown_file_path: str | Path) -> Path:
    """
    Given an image's relative path from the markdown file, return the actual file path
    by resolving the relative path against the markdown file's location.

    Args:
        image_relative_path (str | Path): The relative path of the image as found in the markdown file.
        markdown_file_path (str | Path): The path to the markdown file.

    Returns:
        Path: The resolved absolute path to the image file.
    """
    image_relative_path = Path(image_relative_path)
    markdown_file_path = Path(markdown_file_path).resolve()

    # Resolve the actual image path based on the markdown file's parent directory
    actual_image_path = (markdown_file_path.parent / image_relative_path).resolve()

    return actual_image_path

def get_unique_id(file_path: str | Path, root_dir: Path) -> str:
    """
    Generate a unique identifier (hash) for the given file path, relative to the root directory.

    Args:
        file_path (str | Path): The file path or string data to hash.
        root_dir (Path): The root directory to which the path should be made relative.

    Returns:
        str: A SHA-256 hash of the file path or string.
    """
    # Ensure file_path and root_dir are strings
    file_path = Path(file_path).resolve()

    # Normalize the path to remove redundant separators and up-level references
    normalized_path = os.path.normpath(file_path)

    # Convert backslashes to forward slashes for consistency
    normalized_path = normalized_path.replace('\\', '/')

    # Log the normalized path for debugging
    logger.info(f"Normalized file path for hashing: {normalized_path}")

    # Convert the normalized path to bytes and hash it
    file_path_bytes = normalized_path.encode('utf-8')
    hash_object = hashlib.sha256()
    hash_object.update(file_path_bytes)
    
    # Generate the hexadecimal digest
    unique_identifier = hash_object.hexdigest()
    
    logger.info(f"HASH in GET UNIQUE ID for: {normalized_path} HASH={unique_identifier}")
    
    return unique_identifier

def generate_translated_filename(original_filepath: str | Path, language_code: str, root_dir: Path) -> str:
    """
    Generate a filename for a translated file, including a unique hash and language code.

    Note:
    If the file path and the file name are identical, the same hash will be generated.
    This is because the hash is based on the entire file path.

    Args:
        original_filepath (str): The original file path.
        language_code (str): The language code for the translation (e.g., 'en', 'fr').

    Returns:
        str: The translated file's new filename.
    """

    original_filepath = Path(original_filepath)

    # Extract original file components
    original_filename, file_ext = get_filename_and_extension(original_filepath)

    # Extract filename and extension
    unique_hash = get_unique_id(str(original_filepath), root_dir)

    # Generate the new filename with the unique hash and language code
    new_filename = f"{original_filename}.{unique_hash}.{language_code}{file_ext}"

    return new_filename

def get_filename_and_extension(file_path: str | Path) -> tuple[str, str]:
    """
    Extract the filename without extension and the file extension from the given file path.

    Args:
        file_path (str | Path): The file path from which to extract the filename and extension.

    Returns:
        tuple[str, str]: A tuple containing the filename without extension and the file extension.
    """
    # Ensure the file_path is a string or Path object
    file_path = str(file_path)  # Convert to string if it's a Path object

    # Extract the base name (filename with extension) and split it into name and extension
    original_filename, file_ext = os.path.splitext(os.path.basename(file_path))

    # Return the filename without extension and the file extension in lowercase
    return original_filename, file_ext.lower()

def filter_files(directory: str | Path) -> list:
    """
    Filter and return only the files in the given directory, excluding directories.

    Args:
        directory (str | Path): The directory path to search for files.

    Returns:
        list: A list of Path objects representing only the files (excluding directories).
    """
    directory = Path(directory)
    return [file for file in directory.glob('**/*') if file.is_file()]

def reset_translation_directories(translations_dir: Path, image_dir: Path, language_codes: list):
    """
    Remove existing translation and translated_images directories if they exist,
    and then create new ones.
    
    Args:
        translations_dir (Path): The directory where translations are stored.
        image_dir (Path): The directory where translated images are stored.
        language_codes (list): A list of language codes for creating language-specific directories.
    """
    # Remove existing directories
    if translations_dir.exists():
        shutil.rmtree(translations_dir)
        logger.info(f"Removed existing translations directory: {translations_dir}")
    
    if image_dir.exists():
        shutil.rmtree(image_dir)
        logger.info(f"Removed existing translated_images directory: {image_dir}")

    # Create new directories
    for lang_code in language_codes:
        lang_dir = translations_dir / lang_code
        lang_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory for {lang_code}: {lang_dir}")
    
    image_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Created translated_images directory: {image_dir}")
