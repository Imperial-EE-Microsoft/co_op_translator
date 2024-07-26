import re
from openai import AzureOpenAI
from src.config.base import Config

def get_openai_client(api_base, api_key, deployment_name, api_version):
    return AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        base_url=f"{api_base}/openai/deployments/{deployment_name}"
    )

def gen_image_translation_prompt(text_data, language):
    prompt = f'''
    You are a translator that receives a batch of lines in an image. Given the following yaml file, please translate each line into {language}.
    For each line, fill it in with the translation, respecting the context of the text.
    Return only the yaml file, fully filled in.
    '''
    for line in text_data:
        prompt += f"- {line}\n"
    return prompt

def remove_code_backticks(message):
    match = re.match(r'```(?:\w+)?\n(.*?)\n```', message, re.DOTALL)
    return match.group(1) if match else message

def extract_yaml_lines(message):
    lines = message.split('\n')
    yaml_lines = [line[2:] for line in lines if line.startswith('- ')]
    return yaml_lines

def translate_text(client, text_data, language):
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
