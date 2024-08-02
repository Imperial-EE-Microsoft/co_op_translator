import os
from dotenv import load_dotenv

load_dotenv()

# Base configuration class with common settings for all environments
class Config:
    AZURE_SUBSCRIPTION_KEY = os.getenv("AZURE_SUBSCRIPTION_KEY")
    # Azure Computer vision Endpoint
    AZURE_VISION_ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT")
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
    DEPLOYMENT_NAME = 'gpt-4o'
    API_VERSION = '2024-05-13'

    @staticmethod
    def init_app(app):
        pass

# Ensure all necessary environment variables are set
required_vars = [
    Config.AZURE_SUBSCRIPTION_KEY,
    Config.AZURE_VISION_ENDPOINT,
    Config.AZURE_OPENAI_ENDPOINT,
    Config.AZURE_OPENAI_KEY,
]

for var in required_vars:
    if var is None:
        raise EnvironmentError("One or more environment variables are not set. Please check your .env file.")
