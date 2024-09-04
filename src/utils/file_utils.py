"""
This module contains utility functions for handling file operations.
Functions include reading from files, writing to files, and handling empty document scenarios.
"""
import hashlib
from pathlib import Path
import shutil

def read_input_file(input_file: Path) -> str:
    """
    Read the content of an input file and return it as a stripped string.

    Args:
        input_file (Path): The path to the input file.

    Returns:
        str: The stripped content of the file.
    """
    with input_file.open('r', encoding='utf-8') as file:
        return file.read().strip()

def handle_empty_document(input_file: Path, output_file: Path) -> None:
    """
    Copy the input file to the output location if the document is empty.

    Args:
        input_file (Path): The path to the input file.
        output_file (Path): The path to the output file.
    """
    shutil.copyfile(input_file, output_file)

def write_output_file(output_file: Path, results: list) -> None:
    """
    Write a list of results to the output file, each on a new line.

    Args:
        output_file (Path): The path to the output file.
        results (list): A list of strings to write to the file.
    """
    with output_file.open('w', encoding='utf-8') as text_file:
        for result in results:
            text_file.write(result)
            text_file.write("\n")

def get_unique_id(file_path: str) -> str:
    """
    Generate a unique identifier for a file path.

    Args:
        file_path (str): The file path to hash.

    Returns:
        str: The unique identifier.
    """
    file_path_bytes = file_path.encode('utf-8')
    hash_object = hashlib.sha256()
    hash_object.update(file_path_bytes)
    return hash_object.hexdigest()

def generate_translated_filename(original_filepath: str, language_code: str) -> str:
    """
    Generate a filename for a translated file, including a unique hash and language code.

    Args:
        original_filepath (str): The original file path.
        language_code (str): The language code for the translation (e.g., 'en', 'fr').

    Returns:
        str: The translated file's new filename.
    """
    # Extract original file components
    original_filename = Path(original_filepath).stem  # Get filename without extension
    file_ext = Path(original_filepath).suffix  # Get file extension
    
    # Generate unique hash based on the original file path
    unique_hash = get_unique_id(str(original_filepath))

    # Generate the new filename with the unique hash and language code
    new_filename = f"{original_filename}.{unique_hash}.{language_code}{file_ext}"

    return new_filename
