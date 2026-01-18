"""Configuration management for NordicDataFlow pipeline."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Azure Storage Configuration
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_STORAGE_ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT_NAME", "nordicdataflow6121")

# Container names (Medallion Architecture)
BRONZE_CONTAINER = "bronze"
SILVER_CONTAINER = "silver"
GOLD_CONTAINER = "gold"

# Azure SQL Configuration
SQL_SERVER = os.getenv("SQL_SERVER", "nordicdataflow-sql-3288.database.windows.net")
SQL_DATABASE = os.getenv("SQL_DATABASE", "NordicDataDB")
SQL_USER = os.getenv("SQL_USER", "sqladmin")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")

# SQL Connection String for pyodbc
SQL_CONNECTION_STRING = (
    f"Driver={{ODBC Driver 17 for SQL Server}};"
    f"Server=tcp:{SQL_SERVER},1433;"
    f"Database={SQL_DATABASE};"
    f"Uid={SQL_USER};"
    f"Pwd={SQL_PASSWORD};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
    f"Connection Timeout=30;"
)

# API Keys
FINGRID_API_KEY = os.getenv("FINGRID_API_KEY")

# API Endpoints
API_ENDPOINTS = {
    "stat_finland": "https://statfin.stat.fi/PxWeb/api/v1/en/StatFin/",
    "prh_ytj": "https://avoindata.prh.fi/opendata-ytj-api/v3/companies",
    "eurostat": "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/",
    "fingrid": "https://data.fingrid.fi/api/datasets/",
}
