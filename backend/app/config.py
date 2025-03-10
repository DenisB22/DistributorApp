from dotenv import load_dotenv, dotenv_values
import os

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path, verbose=True)

config = dotenv_values(env_path)

config = {
    "DB_PASSWORD": os.getenv("POSTGRES_PASSWORD"),
    "DB_HOST": os.getenv("POSTGRES_HOST"),
    "DB_NAME": os.getenv("POSTGRES_NAME"),
    "SECRET_KEY": os.getenv("SECRET_KEY"),
    "ALGORITHM": os.getenv("ALGORITHM"),
    "ACCESS_TOKEN_EXPIRE_MINUTES": int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
}

