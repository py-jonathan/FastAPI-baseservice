import tomli
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load configuration from secret.toml
with open("config/secret.toml", "rb") as f:
    app_config = tomli.load(f)

# Retrieve environment variables
SECRET_KEY = os.getenv("SECRET_KEY", app_config["secrets"]["SECRET_KEY"])
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", app_config["auth"]["ACCESS_TOKEN_EXPIRE_MINUTES"]))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", app_config["OPENAI"]["api_key"])
ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", app_config["ELASTICSEARCH"]["host"])
