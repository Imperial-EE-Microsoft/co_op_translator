"""
This module contains utility functions for handling Markdown content.
Functions include loading language mappings, generating translation prompts,
and processing specific Markdown structures such as comments and URLs.
"""

import yaml
from pathlib import Path

def load_mappings(root_dir: Path) -> dict:
    """
    Load language mappings from a YAML file.

    Args:
        root_dir (Path): The root directory containing the YAML file.

    Returns:
        dict: A dictionary of language mappings.
    """
    repo_root = root_dir.parent.parent
    with open(repo_root / "font_language_mappings.yml", "r", encoding='utf-8') as file:
        return yaml.safe_load(file)

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
    if len(document_chunk.split("\n")) == 1:
        prompt = f"Translate the following text to {output_lang}. NEVER ADD ANY EXTRA CONTENT OUTSIDE THE TRANSLATION. TRANSLATE ONLY WHAT IS GIVEN TO YOU."
    else:
        prompt = f"""
        Translate the following markdown file to {output_lang}.
        Make sure the translation does not sound too literal. Make sure you translate comments as well.
        Do not translate any entities, such as variable names, function names, or class names, but keep them in the file.
        Do not translate any urls or paths, but keep them in the file.
        """

    if is_rtl:
        prompt += "Please write the output from right to left, respecting that this is a right-to-left language.\n"
    else:
        prompt += "Please write the output from left to right.\n"

    prompt += "\n" + document_chunk
    return prompt
