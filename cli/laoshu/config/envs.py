import os


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

                    # Check if environment variable is overridden
                    if key in os.environ:
                        env_vars[key] = os.environ[key]
                    else:
                        env_vars[key] = value
    except FileNotFoundError:
        pass

    return env_vars
