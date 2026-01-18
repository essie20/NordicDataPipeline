# NordicDataFlow 🌊

A real-time data pipeline for Nordic economic and company data, demonstrating core data engineering skills with Azure cloud services.

[![Azure Static Web App](https://img.shields.io/badge/Azure-Dashboard-0078D4?logo=azure)](https://salmon-glacier-0eba51103.4.azurestaticapps.net)

## 🏗️ Architecture (Medallion)

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     INGEST      │───▶│    TRANSFORM    │───▶│      LOAD       │───▶│    CONSUME      │
│    (Bronze)     │    │    (Silver)     │    │     (Gold)      │    │   (Dashboard)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
       │                      │                      │                      │
   Raw JSON              Cleaned Parquet        Azure SQL DB           React App
  Azure Blob               Azure Blob           Star Schema            (Planned)
```

### Data Layers

| Layer | Storage | Format | Purpose |
|-------|---------|--------|---------|
| **Bronze** | Azure Blob (`bronze/`) | JSON | Raw API data, unchanged |
| **Silver** | Azure Blob (`silver/`) | Parquet | Cleaned, validated, typed |
| **Gold** | Azure SQL Database | Tables | Aggregated, query-optimized |

## 📊 Data Sources

| Source | API | Data Type |
|--------|-----|-----------|
| **Statistics Finland** | StatFi PxWeb | Economic indicators |
| **PRH (YTJ)** | Business Register | Finnish company data |
| **Eurostat** | JSON API | EU GDP & statistics |
| **Fingrid** | Open Data API | Real-time electricity production |

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Language** | Python 3.10+ | ETL processing |
| **Storage** | Azure Blob Storage | Data lake (Bronze/Silver) |
| **Database** | Azure SQL (Serverless) | Gold layer warehouse |
| **ETL** | Pandas, PyODBC, PyArrow | Data transformation |
| **Orchestration** | Python Scripts / GitHub Actions | Pipeline scheduling |

## 🚀 Quick Start

### Prerequisites

- Python 3.10+ (or UV package manager)
- Azure CLI (signed in)
- ODBC Driver 17 for SQL Server

### Installation (with UV - Recommended)

[UV](https://github.com/astral-sh/uv) is an extremely fast Python package manager.

```bash
# Clone the repository
git clone https://github.com/yourusername/NordicDataPipeline.git
cd NordicDataPipeline

# Create virtual environment with Python 3.11
uv venv --python 3.11

# Activate (Windows PowerShell)
.\.venv\Scripts\activate

# Install dependencies (fast!)
uv pip install -r requirements.txt
```

### Installation (Traditional pip)

```bash
# Create virtual environment
python -m venv .venv
.\.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file (see `.env.example`):

```env
AZURE_STORAGE_CONNECTION_STRING="<your-connection-string>"
SQL_SERVER="nordicdataflow-sql-3288.database.windows.net"
SQL_DATABASE="NordicDataDB"
SQL_USER="sqladmin"
SQL_PASSWORD="<your-password>"
FINGRID_API_KEY="<your-api-key>"
```

### Running the Pipeline

```bash
# Initialize database schema (first time only)
python -m src.pipeline setup

# Run full ETL pipeline
python -m src.pipeline

# Run individual phases
python -m src.ingest      # APIs → Bronze
python -m src.transform   # Bronze → Silver
python -m src.database    # Silver → Gold

# Test API connectivity
python test_apis.py
```

## 📁 Project Structure

```
NordicDataPipeline/
├── src/
│   ├── __init__.py
│   ├── config.py       # Configuration & env vars
│   ├── storage.py      # Azure Blob Storage client
│   ├── ingest.py       # Data ingestion (Bronze)
│   ├── transform.py    # Data transformation (Silver)
│   ├── database.py     # SQL Database operations (Gold)
│   └── pipeline.py     # Main orchestrator
├── test_apis.py        # API connectivity tests
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (not in git)
├── SETUP.md            # Infrastructure setup guide
└── README.md           # This file
```

## 📐 Database Schema (Gold Layer)

```sql
-- Dimension: Companies
dim_companies (
    company_id, business_id, name, registration_date,
    company_form, status, city, post_code, loaded_at
)

-- Fact: Electricity Production
fact_electricity_production (
    record_id, start_time, end_time, value_mw,
    dataset_id, hour_of_day, day_of_week, date_key, loaded_at
)

-- Dimension: Statistics Categories
dim_stat_categories (
    category_id, external_id, name, category_type,
    last_updated, loaded_at
)

-- Logging: Pipeline Runs
pipeline_runs (
    run_id, run_timestamp, source_name, records_processed,
    status, error_message
)
```

## 🔧 Azure Resources

| Resource | Name | Purpose |
|----------|------|---------|
| **Resource Group** | `NordicDataFlow-RG` | Container for all resources |
| **Storage Account** | `nordicdataflow6121` | Data lake storage |
| **SQL Server** | `nordicdataflow-sql-3288` | Database server |
| **SQL Database** | `NordicDataDB` | Gold layer warehouse |

## 📊 Pipeline Output Example

```
============================================================
🌊 NordicDataFlow Pipeline - Starting
⏰ Run Time: 2026-01-18T20:58:01
============================================================

📥 PHASE 1: INGESTION (Bronze Layer)
   ✅ StatFi: 149 categories
   ✅ PRH (Vivicta): 0 companies
   ✅ Eurostat: GDP data
   ✅ Fingrid: 10 records

🔄 PHASE 2: TRANSFORMATION (Silver Layer)
   ✅ Transformed 10 electricity records
   ✅ Transformed 149 categories

📤 PHASE 3: LOADING (Gold Layer)
   ✅ Loaded 20 electricity records to Gold

============================================================
🏁 Pipeline Complete!
============================================================
```

## 📚 Skills Demonstrated

- ✅ **Python** - ETL processing, API integration
- ✅ **SQL** - Schema design, query optimization
- ✅ **Azure** - Blob Storage, SQL Database, CLI
- ✅ **ETL/ELT Pipelines** - Medallion architecture
- ✅ **Data Modeling** - Star schema (fact/dimension)
- ✅ **DevOps** - Git, environment management

## 📄 License

MIT License - Built for Vivicta Data Engineer application.
