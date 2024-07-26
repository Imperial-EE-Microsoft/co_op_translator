from .base import Config

# Production configuration class with settings specific to production environment
class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'

    @staticmethod
    def init_app(app):
        Config.init_app(app)
        print("Running in production mode")
