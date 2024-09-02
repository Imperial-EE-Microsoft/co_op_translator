"""
This module contains utility functions for handling file operations.
Functions include reading from files, writing to files, and handling empty document scenarios.
"""

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
