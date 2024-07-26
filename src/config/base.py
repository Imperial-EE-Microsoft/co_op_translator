import os
from dotenv import load_dotenv

load_dotenv()

# Base configuration class with common settings for all environments
class Config:
    AZURE_SUBSCRIPTION_KEY = os.getenv("AZURE_SUBSCRIPTION_KEY")
    AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
    OPENAI_BASE = os.getenv("OPENAI_BASE")
    OPENAI_KEY = os.getenv("OPENAI_KEY")
    DEPLOYMENT_NAME = 'gpt-4o'
    API_VERSION = '2023-12-01-preview'

    @staticmethod
    def init_app(app):
        pass

# Ensure all necessary environment variables are set
required_vars = [
    Config.AZURE_SUBSCRIPTION_KEY,
    Config.AZURE_ENDPOINT,
    Config.OPENAI_BASE,
    Config.OPENAI_KEY,
]

for var in required_vars:
    if var is None:
        raise EnvironmentError("One or more environment variables are not set. Please check your .env file.")
