from .base import Config

# Development configuration class with settings specific to development environment
class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'

    @staticmethod
    def init_app(app):
        Config.init_app(app)
        print("Running in development mode")
