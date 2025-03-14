import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import config

# PostgreSQL Configuration
POSTGRESQL_DATABASE_URL = f"postgresql://postgres:{config['DB_PASSWORD']}@{config['DB_HOST']}/{config['DB_NAME']}"
postgres_engine = create_engine(POSTGRESQL_DATABASE_URL)
PostgresSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=postgres_engine)

# MSSQL Configuration
MSSQL_DATABASE_URL = f"mssql+pyodbc://{config['MSSQL_USER']}:{config['MSSQL_PASSWORD']}@{config['MSSQL_SERVER']}/{config['MSSQL_DATABASE']}?driver={config['MSSQL_DRIVER']}&TrustServerCertificate=yes"
mssql_engine = create_engine(MSSQL_DATABASE_URL)
MSSQLSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=mssql_engine)

# Base for models
Base = declarative_base()

# Dependency for PostgreSQL
def get_postgres_db():
    db = PostgresSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency for MSSQL
def get_mssql_db():
    db = MSSQLSessionLocal()
    try:
        yield db
    finally:
        db.close()
