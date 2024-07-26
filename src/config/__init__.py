from .base import Config
from .development import DevelopmentConfig
from .production import ProductionConfig

# Dictionary to map configuration names to configuration classes
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# Function to configure the app with the specified configuration
def configure_app(app, config_name='default'):
    app_config = config.get(config_name)
    if app_config is None:
        raise ValueError(f"Invalid config name: {config_name}")
    app.config.from_object(app_config)
    app_config.init_app(app)
