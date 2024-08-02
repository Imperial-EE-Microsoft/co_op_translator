"""
This module contains functions to interact with the Azure OpenAI API.
It provides functionalities to generate translation prompts and process the responses.
"""
import sys
import os
from openai import AzureOpenAI
from src.config.base import Config
from utils.text_utils import gen_image_translation_prompt, remove_code_backticks, extract_yaml_lines

# Add the src directory to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

def get_openai_client():
    """
    Initialize and return an OpenAI client.
    
    Returns:
        AzureOpenAI: The initialized OpenAI client.
    """
    return AzureOpenAI(
        api_key=Config.AZURE_OPENAI_KEY,
        api_version=Config.API_VERSION,
        base_url=f"{Config.AZURE_OPENAI_ENDPOINT}/openai/deployments/{Config.DEPLOYMENT_NAME}"
    )

def translate_text(text_data, language):
    """
    Translate text data using the Azure OpenAI API.
    
    Args:
        text_data (list): List of text lines to be translated.
        language (str): Target language for translation.
    
    Returns:
        list: List of translated text lines.
    """
    client = get_openai_client()
    prompt = gen_image_translation_prompt(text_data, language)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            { "role": "system", "content": "You are a helpful assistant." },
            { "role": "user", "content": prompt }
        ],
        max_tokens=2000
    )
    return extract_yaml_lines(remove_code_backticks(response.choices[0].message.content))
