"""
This module contains utility functions for handling file operations.
Functions include reading from files, writing to files, and handling empty document scenarios.
"""

import hashlib
from pathlib import Path
import shutil

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

def get_unique_id(file_path: str | Path) -> str:
    """
    Generate a unique identifier (hash) for the given file path.

    Args:
        file_path (str | Path): The file path or string data to hash.

    Returns:
        str: A SHA-256 hash of the file path or string.
    """
    file_path = str(file_path)  # Ensure it's a string for encoding
    file_path_bytes = file_path.encode('utf-8')
    hash_object = hashlib.sha256()
    hash_object.update(file_path_bytes)
    return hash_object.hexdigest()

def generate_translated_filename(original_filepath: str | Path, language_code: str) -> str:
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
    # Extract original file components
    original_filename = get_filename_without_extension(original_filepath)  # Get filename without extension
    file_ext = get_file_extension(original_filepath)  # Get file extension
    
    # Generate unique hash based on the original file path
    unique_hash = get_unique_id(str(original_filepath))

    # Generate the new filename with the unique hash and language code
    new_filename = f"{original_filename}.{unique_hash}.{language_code}{file_ext}"

    return new_filename

def get_file_extension(file_path: str) -> str:
    """
    Extract the file extension from the given file path and return it in lowercase.
    If no extension is found, return an empty string.

    Args:
        file_path (str): The file path from which to extract the extension.

    Returns:
        str: The file extension in lowercase, or an empty string if no extension is present.

    Raises:
        ValueError: If the input path is invalid or not a file.
    """
    # Ensure the file_path is a Path object
    file_path = Path(file_path)

    # Validate that the provided path is a file, not a directory
    if not file_path.is_file():
        raise ValueError(f"Invalid file path: {file_path}")
    
    if file_path.is_file():
        return file_path.suffix or ""
    else:
        return ""


def get_filename_without_extension(file_path: str | Path) -> str:
    """
    Extract and return the filename without the extension.

    Args:
        file_path (str | Path): The file path from which to extract the filename.

    Returns:
        str: The filename without its extension.
    """
    file_path = Path(file_path)
    return file_path.stem

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