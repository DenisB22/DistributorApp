from dotenv import load_dotenv, dotenv_values
import os

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path, verbose=True)

config = dotenv_values(env_path)

config = {
    # PostgreSQL Config
    "DB_PASSWORD": os.getenv("POSTGRES_PASSWORD"),
    "DB_HOST": os.getenv("POSTGRES_HOST"),
    "DB_NAME": os.getenv("POSTGRES_NAME"),

    # MSSQL Config
    "MSSQL_SERVER": os.getenv("MSSQL_SERVER"),
    "MSSQL_DATABASE": os.getenv("MSSQL_DATABASE"),
    "MSSQL_USER": os.getenv("MSSQL_USER"),
    "MSSQL_PASSWORD": os.getenv("MSSQL_PASSWORD"),
    "MSSQL_DRIVER": os.getenv("MSSQL_DRIVER"),

    # JWT config
    "SECRET_KEY": os.getenv("SECRET_KEY"),
    "ALGORITHM": os.getenv("ALGORITHM"),
    "ACCESS_TOKEN_EXPIRE_MINUTES": int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
}

