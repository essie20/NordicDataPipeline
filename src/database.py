"""Database operations for Azure SQL (Gold layer)."""
import pyodbc
import pandas as pd
from io import BytesIO
from src.config import SQL_CONNECTION_STRING, SILVER_CONTAINER
from src.storage import AzureStorageClient


class DatabaseManager:
    """Manages connections and operations for Azure SQL Database."""

    def __init__(self):
        self.connection_string = SQL_CONNECTION_STRING

    def get_connection(self):
        """Get a new database connection."""
        return pyodbc.connect(self.connection_string)

    def execute_query(self, query: str, params: tuple = None) -> None:
        """Execute a query without returning results."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()

    def fetch_all(self, query: str, params: tuple = None) -> list:
        """Execute a query and return all results."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def create_schema(self) -> None:
        """Create the database schema for the Gold layer."""
        print("🏗️ Creating database schema...")

        # Companies dimension table
        create_companies = """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='dim_companies' AND xtype='U')
        CREATE TABLE dim_companies (
            company_id INT IDENTITY(1,1) PRIMARY KEY,
            business_id NVARCHAR(50) UNIQUE NOT NULL,
            name NVARCHAR(255) NOT NULL,
            registration_date DATE,
            company_form NVARCHAR(100),
            status NVARCHAR(50),
            city NVARCHAR(100),
            post_code NVARCHAR(20),
            loaded_at DATETIME2 DEFAULT GETUTCDATE()
        );
        """

        # Electricity production fact table
        create_electricity = """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='fact_electricity_production' AND xtype='U')
        CREATE TABLE fact_electricity_production (
            record_id INT IDENTITY(1,1) PRIMARY KEY,
            start_time DATETIME2 NOT NULL,
            end_time DATETIME2,
            value_mw DECIMAL(10,2) NOT NULL,
            dataset_id INT,
            hour_of_day INT,
            day_of_week INT,
            date_key DATE,
            loaded_at DATETIME2 DEFAULT GETUTCDATE()
        );
        """

        # Statistics catalog dimension
        create_stat_categories = """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='dim_stat_categories' AND xtype='U')
        CREATE TABLE dim_stat_categories (
            category_id INT IDENTITY(1,1) PRIMARY KEY,
            external_id NVARCHAR(100) UNIQUE NOT NULL,
            name NVARCHAR(255) NOT NULL,
            category_type NVARCHAR(50),
            last_updated DATETIME2,
            loaded_at DATETIME2 DEFAULT GETUTCDATE()
        );
        """

        # Pipeline run log
        create_pipeline_log = """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='pipeline_runs' AND xtype='U')
        CREATE TABLE pipeline_runs (
            run_id INT IDENTITY(1,1) PRIMARY KEY,
            run_timestamp DATETIME2 DEFAULT GETUTCDATE(),
            source_name NVARCHAR(50),
            records_processed INT,
            status NVARCHAR(20),
            error_message NVARCHAR(MAX)
        );
        """

        self.execute_query(create_companies)
        self.execute_query(create_electricity)
        self.execute_query(create_stat_categories)
        self.execute_query(create_pipeline_log)
        
        print("✅ Schema created successfully!")

    def log_pipeline_run(self, source: str, records: int, status: str, error: str = None):
        """Log a pipeline run to the database."""
        query = """
        INSERT INTO pipeline_runs (source_name, records_processed, status, error_message)
        VALUES (?, ?, ?, ?)
        """
        self.execute_query(query, (source, records, status, error))


class GoldLoader:
    """Loads data from Silver to Gold (SQL Database)."""

    def __init__(self):
        self.storage = AzureStorageClient()
        self.db = DatabaseManager()

    def load_companies(self, silver_blob_path: str) -> int:
        """Load company data from Silver Parquet to Gold SQL table."""
        print(f"📤 Loading companies from: {silver_blob_path}")
        
        # Read Parquet from Silver
        data = self.storage.read_from_container(SILVER_CONTAINER, silver_blob_path)
        df = pd.read_parquet(BytesIO(data))
        
        loaded = 0
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            for _, row in df.iterrows():
                # Upsert logic (insert or update)
                query = """
                MERGE dim_companies AS target
                USING (SELECT ? AS business_id) AS source
                ON target.business_id = source.business_id
                WHEN MATCHED THEN
                    UPDATE SET 
                        name = ?,
                        registration_date = ?,
                        company_form = ?,
                        status = ?,
                        city = ?,
                        post_code = ?,
                        loaded_at = GETUTCDATE()
                WHEN NOT MATCHED THEN
                    INSERT (business_id, name, registration_date, company_form, status, city, post_code)
                    VALUES (?, ?, ?, ?, ?, ?, ?);
                """
                
                reg_date = row.get("registration_date") if pd.notna(row.get("registration_date")) else None
                
                cursor.execute(query, (
                    row["business_id"],
                    row["name"], reg_date, row.get("company_form"), row.get("status"),
                    row.get("city"), row.get("post_code"),
                    row["business_id"], row["name"], reg_date, row.get("company_form"),
                    row.get("status"), row.get("city"), row.get("post_code")
                ))
                loaded += 1
            
            conn.commit()
        
        self.db.log_pipeline_run("prh_companies", loaded, "success")
        print(f"   ✅ Loaded {loaded} companies to Gold")
        return loaded

    def load_electricity(self, silver_blob_path: str) -> int:
        """Load electricity data from Silver to Gold."""
        print(f"📤 Loading electricity data from: {silver_blob_path}")
        
        data = self.storage.read_from_container(SILVER_CONTAINER, silver_blob_path)
        df = pd.read_parquet(BytesIO(data))
        
        loaded = 0
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            for _, row in df.iterrows():
                query = """
                INSERT INTO fact_electricity_production 
                (start_time, end_time, value_mw, dataset_id, hour_of_day, day_of_week, date_key)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """
                
                cursor.execute(query, (
                    row.get("startTime"),
                    row.get("endTime"),
                    row.get("value"),
                    row.get("datasetId", 192),
                    row.get("hour"),
                    row.get("day_of_week"),
                    row.get("date")
                ))
                loaded += 1
            
            conn.commit()
        
        self.db.log_pipeline_run("fingrid_electricity", loaded, "success")
        print(f"   ✅ Loaded {loaded} electricity records to Gold")
        return loaded


def initialize_database():
    """Initialize the database schema."""
    db = DatabaseManager()
    db.create_schema()


if __name__ == "__main__":
    initialize_database()
