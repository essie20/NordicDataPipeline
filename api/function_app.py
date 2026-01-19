import azure.functions as func
import logging
import json
import os
import pyodbc

app = func.FunctionApp()

def get_db_connection():
    # Use the same connection string from environment variables
    conn_str = os.environ.get('SQL_CONNECTION_STRING')
    if not conn_str:
        # Fallback construction if full string not provided (unlikely in SWA env if configured right)
        server = os.environ.get('SQL_SERVER')
        database = os.environ.get('SQL_DATABASE')
        user = os.environ.get('SQL_USER')
        password = os.environ.get('SQL_PASSWORD')
        driver = '{ODBC Driver 18 for SQL Server}'
        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={user};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    
    return pyodbc.connect(conn_str)

@app.route(route="stats", auth_level=func.AuthLevel.ANONYMOUS)
def get_stats(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing request for stats.')

    try:
        # Connect to DB (In a real app, use a connection pool or Context Manager)
        # Note: This requires the SQL ENV VARS to be set in Azure Static Web App settings!
        
        # For this demo, we'll try to connect. If no env vars, we return error.
        if not os.environ.get('SQL_SERVER') and not os.environ.get('SQL_CONNECTION_STRING'):
             return func.HttpResponse(
                json.dumps({"error": "Database configuration missing", "mock": True}),
                mimetype="application/json",
                status_code=500
            )

        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # 1. Fetch latest electricity consumption (Simulated query for now as we need to know exact table state)
            # We'll just try to count rows or get the latest record
            cursor.execute("SELECT COUNT(*) FROM fact_electricity_production")
            count = cursor.fetchone()[0]

            cursor.execute("SELECT TOP 1 value_mw, start_time FROM fact_electricity_production ORDER BY start_time DESC")
            latest = cursor.fetchone()
            
            latest_val = latest[0] if latest else 0
            
            # 2. Fetch companies count
            cursor.execute("SELECT COUNT(*) FROM dim_companies")
            companies = cursor.fetchone()[0]

            data = {
                "electricity": {
                    "latest_mw": float(latest_val),
                    "total_records": int(count)
                },
                "companies": {
                    "total": int(companies)
                },
                "source": "Azure SQL Database"
            }

            return func.HttpResponse(
                json.dumps(data),
                mimetype="application/json",
                status_code=200
            )

    except Exception as e:
        logging.error(f"Error connecting to DB: {str(e)}")
        
        # Debug info: Check available drivers
        drivers = [d for d in pyodbc.drivers()]
        
        return func.HttpResponse(
            json.dumps({
                "error": str(e), 
                "drivers": drivers,
                "note": "Ensure Azure IP firewall is open and Env Vars are set"
            }),
            mimetype="application/json",
            status_code=500
        )
