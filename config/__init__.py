import tomli

with open("config/secret.toml", "rb") as f:
    app_config = tomli.load(f)