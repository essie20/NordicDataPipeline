# NordicDataFlow 🌊

A real-time data pipeline for Nordic economic and company data, demonstrating core data engineering skills with Azure cloud services.

[![Azure Static Web App](https://img.shields.io/badge/Azure-Dashboard-0078D4?logo=azure)](https://salmon-glacier-0eba51103.4.azurestaticapps.net) [![CI Status](https://github.com/essie20/NordicDataPipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/essie20/NordicDataPipeline/actions/workflows/ci.yml)

## 🏗️ Architecture (Medallion)

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     INGEST      │───▶│    TRANSFORM    │───▶│      LOAD       │───▶│    CONSUME      │
│    (Bronze)     │    │    (Silver)     │    │     (Gold)      │    │   (Dashboard)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
       │                      │                      │                      │
   Raw JSON              Cleaned Parquet        Azure SQL DB           React App
  Azure Blob               Azure Blob           Star Schema          (Azure SWA)
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
| **Language** | Python 3.11 | ETL processing |
| **Frontend** | React 19 + Vite | Interactive Dashboard |
| **Styling** | TailwindCSS v4 | Premium UI Design |
| **Storage** | Azure Blob Storage | Data lake (Bronze/Silver) |
| **Database** | Azure SQL (Serverless) | Gold layer warehouse |
| **ETL** | Pandas, PyODBC, PyArrow | Data transformation |
| **Orchestration** | GitHub Actions | CI/CD & Scheduling |
| **Deployment** | Azure Static Web Apps | Frontend Hosting |

## 🚀 Quick Start

### Prerequisites

- Python 3.10+ (or UV package manager)
- Node.js 20+ (for dashboard)
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

### Frontend Setup

```bash
cd nordic-data-dashboard
npm install
npm run dev
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
├── .github/
│   └── workflows/
│       ├── ci.yml                 # CI Pipeline (Lint + Build)
│       └── azure-static-web-apps* # Azure Deployment
├── nordic-data-dashboard/    # React Frontend
│   ├── src/
│   │   ├── components/       # Dashboard widgets
│   │   ├── lib/              # Utilities
│   │   └── App.tsx           # Main entry
│   └── vite.config.ts        # Build config
├── src/                      # Python ETL Pipeline
│   ├── __init__.py
│   ├── config.py             # Configuration & env vars
│   ├── storage.py            # Azure Blob Storage client
│   ├── ingest.py             # Data ingestion (Bronze)
│   ├── transform.py          # Data transformation (Silver)
│   ├── database.py           # SQL Database operations (Gold)
│   └── pipeline.py           # Main orchestrator
├── test_apis.py              # API connectivity tests
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
└── SETUP.md                  # Infrastructure setup guide
```

## 🔧 Azure Resources

| Resource | Name | Purpose |
|----------|------|---------|
| **Resource Group** | `NordicDataFlow-RG` | Container for all resources |
| **Storage Account** | `nordicdataflow6121` | Data lake storage |
| **SQL Server** | `nordicdataflow-sql-3288` | Database server |
| **SQL Database** | `NordicDataDB` | Gold layer warehouse |
| **Static Web App** | `NordicDataDashboard` | React Frontend Hosting |

## 📚 Skills Demonstrated

- ✅ **Python & SQL** - Core data engineering
- ✅ **React & TypeScript** - Full-stack visualization
- ✅ **Azure Cloud** - Blob, SQL, Static Web Apps
- ✅ **ETL/ELT Pipelines** - Medallion architecture
- ✅ **CI/CD** - GitHub Actions workflow
- ✅ **DevOps** - Infrastructure management

## 📄 License

MIT License - Built for Vivicta Data Engineer application.
