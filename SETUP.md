# Infrastructure Setup Guide 🛠️

Complete guide to recreate the Azure infrastructure for NordicDataFlow from scratch.

## 📋 Current Status (Last Updated: 2026-01-18)

| Resource | Status | Name |
|----------|--------|------|
| **Resource Group** | ✅ Created | `NordicDataFlow-RG` |
| **Storage Account** | ✅ Created | `nordicdataflow6121` |
| **Bronze Container** | ✅ Created | `bronze` |
| **Silver Container** | ✅ Created | `silver` |
| **Gold Container** | ✅ Created | `gold` |
| **SQL Server** | ✅ Created | `nordicdataflow-sql-3288` |
| **SQL Database** | ✅ Created | `NordicDataDB` (Free tier) |
| **Firewall Rules** | ✅ Configured | Azure IPs + Local Client |
| **Python Environment** | ✅ Working | Python 3.11 via UV |
| **Pipeline** | ✅ Tested | Full ETL cycle verified |

---

## 🔐 Prerequisites

### 1. Azure CLI Installation
Download and install from: https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows

### 2. Azure Login
```powershell
az login --use-device-code
```

### 3. Verify Subscription
```powershell
az account show --query "{name:name, subscriptionId:id}" -o table
```

### 4. ODBC Driver for SQL Server
Download **ODBC Driver 17**: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

Check installed drivers:
```powershell
Get-OdbcDriver | Where-Object {$_.Name -like "*SQL*"} | Select-Object Name
```

### 5. UV Package Manager (Recommended)
Install UV for fast Python package management:
```powershell
# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex

# Or with pip
pip install uv
```

---

## 🏗️ Infrastructure Provisioning (Step by Step)

### Step 1: Create Resource Group

```powershell
az group create --name NordicDataFlow-RG --location northeurope --output table
```

**Result:**
```
Location     Name
-----------  -----------------
northeurope  NordicDataFlow-RG
```

### Step 2: Create Storage Account

```powershell
az storage account create `
  --name nordicdataflow6121 `
  --resource-group NordicDataFlow-RG `
  --location northeurope `
  --sku Standard_LRS `
  --kind StorageV2 `
  --output table
```

**Notes:**
- `Standard_LRS` = Locally Redundant Storage (cheapest)
- Account name must be globally unique (lowercase, 3-24 chars)
- For your own deployment, generate a unique name:
  ```powershell
  $rand = Get-Random -Minimum 1000 -Maximum 9999
  az storage account create --name nordicdataflow$rand ...
  ```

### Step 3: Create Medallion Containers

```powershell
# Bronze - Raw data
az storage container create --name bronze --account-name nordicdataflow6121 --auth-mode login

# Silver - Cleaned data
az storage container create --name silver --account-name nordicdataflow6121 --auth-mode login

# Gold - Aggregated data
az storage container create --name gold --account-name nordicdataflow6121 --auth-mode login
```

### Step 4: Get Storage Connection String

```powershell
az storage account show-connection-string `
  --name nordicdataflow6121 `
  --resource-group NordicDataFlow-RG `
  --query connectionString -o tsv
```

**Save this in your `.env` file as `AZURE_STORAGE_CONNECTION_STRING`**

### Step 5: Create SQL Server

```powershell
az sql server create `
  --name nordicdataflow-sql-3288 `
  --resource-group NordicDataFlow-RG `
  --location northeurope `
  --admin-user sqladmin `
  --admin-password "YourSecurePassword123!" `
  --output table
```

**Notes:**
- Server name must be globally unique
- Password must meet complexity requirements (uppercase, lowercase, number, special char, 8+ chars)

### Step 6: Configure Firewall Rules

```powershell
# Allow Azure services
az sql server firewall-rule create `
  --resource-group NordicDataFlow-RG `
  --server nordicdataflow-sql-3288 `
  --name AllowAllAzureIPs `
  --start-ip-address 0.0.0.0 `
  --end-ip-address 0.0.0.0

# Allow your local IP
$myIp = (Invoke-WebRequest -Uri "https://api.ipify.org" -UseBasicParsing).Content
az sql server firewall-rule create `
  --resource-group NordicDataFlow-RG `
  --server nordicdataflow-sql-3288 `
  --name AllowLocalClient `
  --start-ip-address $myIp `
  --end-ip-address $myIp
```

### Step 7: Create SQL Database (Free Tier)

```powershell
az sql db create `
  --resource-group NordicDataFlow-RG `
  --server nordicdataflow-sql-3288 `
  --name NordicDataDB `
  --edition GeneralPurpose `
  --family Gen5 `
  --compute-model Serverless `
  --capacity 1 `
  --use-free-limit `
  --free-limit-exhaustion-behavior AutoPause `
  --output table
```

**Result:**
```
Name          Tier            Family    Capacity    MaxSize
------------  --------------  --------  ----------  ---------
NordicDataDB  GeneralPurpose  Gen5      1           32GB
```

---

## � Python Environment Setup

### Option A: Using UV (Recommended - Fast!)

```powershell
# Create virtual environment with Python 3.11
uv venv --python 3.11

# Activate
.\.venv\Scripts\activate

# Install all dependencies (takes ~5 seconds)
uv pip install -r requirements.txt
```

### Option B: Traditional pip

```powershell
# Create virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

---

## 🔑 Environment Configuration

Create a `.env` file in the project root:

```env
# Azure Storage
AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=nordicdataflow6121;AccountKey=YOUR_KEY_HERE"
AZURE_STORAGE_ACCOUNT_NAME="nordicdataflow6121"

# Azure SQL Database
SQL_SERVER="nordicdataflow-sql-3288.database.windows.net"
SQL_DATABASE="NordicDataDB"
SQL_USER="sqladmin"
SQL_PASSWORD="YourPasswordHere"

# API Keys
FINGRID_API_KEY="your-fingrid-api-key"
```

Get your Fingrid API key from: https://data.fingrid.fi/

---

## 🚀 Running the Pipeline

```powershell
# 1. Initialize database schema (first time only)
python -m src.pipeline setup

# 2. Run full ETL pipeline
python -m src.pipeline

# Individual phases
python -m src.ingest      # APIs → Bronze
python -m src.transform   # Bronze → Silver  
python -m src.database    # Initialize DB

# Test API connectivity
python test_apis.py
```

---

## ✅ Verification Commands

### Check Resource Group
```powershell
az group show --name NordicDataFlow-RG --query "{name:name, location:location}" -o table
```

### Check Storage Account
```powershell
az storage account show --name nordicdataflow6121 --query "{name:name, sku:sku.name}" -o table
```

### List Containers
```powershell
az storage container list --account-name nordicdataflow6121 --auth-mode login --query "[].name" -o table
```

### Check SQL Database Status
```powershell
az sql db show --resource-group NordicDataFlow-RG --server nordicdataflow-sql-3288 --name NordicDataDB --query "status" -o tsv
```

### Check ODBC Drivers
```powershell
Get-OdbcDriver | Where-Object {$_.Name -like "*SQL*"} | Select-Object Name
```

---

## 🗑️ Cleanup (If Needed)

**⚠️ WARNING: This deletes ALL resources in the resource group!**

```powershell
az group delete --name NordicDataFlow-RG --yes --no-wait
```

---

## 📊 Cost Estimation

| Resource | Tier | Estimated Cost |
|----------|------|----------------|
| Storage Account | Standard LRS | ~$0.02/GB/month |
| SQL Database | Free Tier | **$0** (100K vCore-seconds/month) |
| **Total** | | **< $1/month** for dev usage |

The Azure SQL Free Tier includes:
- 100,000 vCore-seconds per month
- 32 GB storage
- Auto-pause when idle (saves compute costs)

---

## 🔗 Useful Links

- [Azure CLI Documentation](https://learn.microsoft.com/en-us/cli/azure/)
- [Azure SQL Free Offer](https://learn.microsoft.com/en-us/azure/azure-sql/database/free-offer)
- [Azure Blob Storage](https://learn.microsoft.com/en-us/azure/storage/blobs/)
- [ODBC Driver for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
- [UV Package Manager](https://github.com/astral-sh/uv)
- [Fingrid Open Data](https://data.fingrid.fi/)
- [Statistics Finland API](https://statfin.stat.fi/PxWeb/api/v1/en/StatFin/)
