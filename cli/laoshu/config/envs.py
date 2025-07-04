import os


REQUIRED_API_KEYS = ["SCRAPINGANT_API_KEY", "OPENAI_API_KEY"]

def read_env_vars() -> dict[str, str]:
    """
    Read environment variables from .env file and check if they are overridden by actual environment variables.

    Returns:
        dict[str, str]: Dictionary of environment variables and their values
    """
    env_vars = {}

    try:
        with open(".env", "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()

        for key in REQUIRED_API_KEYS:
            if key in os.environ:
                env_vars[key] = os.environ[key]
    except FileNotFoundError:
        # If .env file is not found, read all environment variables from os.environ
        for key in os.environ:
            env_vars[key] = os.environ[key]

    return env_vars
