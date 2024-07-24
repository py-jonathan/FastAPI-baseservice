import tomli

with open("config/secret.toml", "rb") as f:
    app_config = tomli.load(f)

SECRET_KEY = app_config["secrets"]["SECRET_KEY"]
ACCESS_TOKEN_EXPIRE_MINUTES = app_config["auth"]["ACCESS_TOKEN_EXPIRE_MINUTES"]
OPENAI_API_KEY = app_config["OPENAI"]["api_key"]