import logging.config
import yaml

def setup_logging(config_path: str):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
        logging.config.dictConfig(config)

# Load logging configuration
setup_logging('config/log-config.yml')

logger = logging.getLogger("app")