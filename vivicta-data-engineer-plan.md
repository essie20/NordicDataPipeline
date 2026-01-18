# Vivicta Junior Consultant - Data Engineer Project Plan

## 📋 Position Overview

| Field | Details |
|-------|---------|
| **Company** | Vivicta (formerly Tietoevry Tech Services) |
| **Position** | Junior Consultant - Data Engineer |
| **Location** | Finland, Espoo (Hybrid) |
| **Type** | Full-time, Permanent |
| **Start Date** | April 1, 2026 |
| **Salary** | €3,500/month |
| **Application Deadline** | January 18, 2025 |
| **Apply** | [Workday Application](https://tieto.wd3.myworkdayjobs.com/Tieto_Careers_External_Site/job/Finland-Espoo/Junior-Consultant_R125224) |

---

## 🎯 Required Skills for Data Engineer Role

Based on the job posting, these are the key technical skills:

### Core Programming
- [x] **Python** - Primary language for data engineering
- [x] **SQL** - Essential for database operations

### Databases
- [x] **SQL Databases** - Relational database fundamentals
- [ ] **PostgreSQL** - Specific RDBMS experience

### Cloud Platforms
- [x] **Azure** - Microsoft cloud services
- [ ] **AWS** - Amazon Web Services (alternative)

### DevOps & Development
- [ ] **DevOps practices** - CI/CD pipelines, automation
- [ ] **CI/CD** - Continuous integration/deployment

### Data Platforms & Tools
- [ ] **Microsoft Fabric** - Microsoft's unified analytics platform
- [ ] **Databricks** - Unified data analytics platform
- [x] **ETL/ELT Pipelines** - Data extraction, transformation, loading
- [x] **Data Models** - Designing and implementing data structures

---

## ✅ Skills Alignment with Existing Projects

### Strong Matches (Already Demonstrated)
| Skill | Your Experience | Project |
|-------|-----------------|---------|
| **SQL/Azure SQL** | ✅ Strong | NordicDataFlow (Star Schema on Azure SQL) |
| **Python** | ✅ Expert | NordicDataFlow (Modular ETL pipeline) |
| **CI/CD** | ✅ Demonstrated | AI-Powered Feedback Collector (CI/CD pipeline) |
| **Cloud (Azure)** | ✅ Hands-on | NordicDataFlow (Blob Storage, SQL Database, CLI) |
| **ETL/ELT** | ✅ Complete | NordicDataFlow (Bronze/Silver/Gold Medallion) |
| **API Development** | ✅ Strong | Multiple REST API implementations |

### Gaps to Address
| Skill | Priority | Status |
|-------|----------|---------------|
| **Microsoft Fabric** | 🔴 High | Learning next (Integration with Azure SQL) |
| **Databricks** | 🟡 Medium | Exploring basics |
| **Real-time Ingestion** | � Medium | Expanding Fingrid real-time logic |
| **Power BI** | 🟡 Medium | Planning for Gold layer visualization |

---

## 🚀 Project Proposal: Nordic Data Pipeline

### Project Overview
Build a **real-time data pipeline** that demonstrates core data engineering skills relevant to Vivicta's requirements.

### Project Name: `NordicDataFlow`

**Concept:** A data pipeline that ingests, transforms, and visualizes Nordic company/economic data, demonstrating the complete data engineering lifecycle.

### Architecture (Implemented)

```
┌───────────────┐    ┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   Inbound     │───▶│    Bronze     │───▶│    Silver     │───▶│     Gold      │
│  (REST APIs)  │    │  (Raw JSON)   │    │  (Parquet)    │    │  (Azure SQL)  │
└───────────────┘    └───────────────┘    └───────────────┘    └───────────────┘
      │                  │                  │                  │
   Fingrid/PRH          Blob Storage       Pandas/PyArrow      Star Schema
```

### Tech Stack (Aligned with Vivicta Requirements)

| Layer | Technology | Vivicta Alignment |
|-------|------------|-------------------|
| **Data Ingestion** | Python (requests, pandas) | ✅ Python |
| **ETL Processing** | Python + SQL scripts | ✅ ETL/ELT Pipelines |
| **Data Storage** | PostgreSQL (Supabase) | ✅ SQL, PostgreSQL |
| **Data Modeling** | Star Schema design | ✅ Data Models |
| **Orchestration** | GitHub Actions / Azure Functions | ✅ DevOps, CI/CD, Azure |
| **Visualization** | React Dashboard | ✅ Shows full-stack capability |
| **Cloud** | Azure (or AWS fallback) | ✅ Cloud Platforms |

### Core Features

1. **Data Ingestion Layer**
   - Connect to public APIs (e.g., Statistics Finland, Eurostat)
   - CSV/JSON file processing
   - Scheduled data pulls

2. **ETL/ELT Pipeline**
   - Data cleaning and validation
   - Transformation logic (aggregations, joins)
   - Incremental loading strategies
   - Error handling and logging

3. **Data Warehouse**
   - Dimensional modeling (fact/dimension tables)
   - PostgreSQL schema design
   - Query optimization

4. **CI/CD Pipeline**
   - Automated testing for data quality
   - GitHub Actions for deployment
   - Environment management (dev/prod)

5. **Monitoring Dashboard**
   - React frontend
   - Data quality metrics
   - Pipeline run history

---

## 📅 Implementation Timeline

### Phase 1: Foundation (Days 1-2) - COMPLETED ✅
- [x] Set up project repository
- [x] Configure Azure SQL Database (Serverless)
- [x] Design initial data model (star schema)
- [x] Create basic Python ingestion scripts

### Phase 2: Core Pipeline (Days 3-4) - COMPLETED ✅
- [x] Build ETL pipeline with Python
- [x] Implement data transformations (Bronze to Silver)
- [x] Add error handling and logging
- [x] Write SQL queries for data loading (Silver to Gold)

### Phase 3: Automation & Documentation (Days 5-6) - IN PROGRESS 🏗️
- [ ] Set up GitHub Actions for CI/CD
- [x] Add automated local orchestration (pipeline.py)
- [x] Document infrastructure setup (SETUP.md)
- [x] Document pipeline architecture (README.md)

### Phase 4: Visualization & Polish (Days 7-8) - PENDING ⏳
- [ ] Build React dashboard (Azure static web app)
- [ ] Add data visualization components
- [ ] Finalize comprehensive documentation
- [x] Create implementation diagrams

---

## 📝 Application Strategy

### Key Points to Highlight in Application

1. **Existing Data Experience**
   - SQL database work in AI Invoice Analyzer and Flight Crew Management
   - API integrations across multiple projects
   - Data extraction from invoices (AI Invoice Analyzer)

2. **Full-Stack Capability**
   - Strong foundation for understanding end-to-end data flows
   - Experience with both frontend and backend
   - CI/CD and DevOps practices

3. **Learning Agility**
   - Diverse tech stack across projects shows adaptability
   - Interest in data engineering specifically
   - Ready to learn Azure and MS Fabric

### Cover Letter Focus Areas
- [ ] Emphasize Python & SQL proficiency
- [ ] Highlight database design experience
- [ ] Mention CI/CD and automation skills
- [ ] Express specific interest in Data Engineer role
- [ ] Show enthusiasm for learning Azure/Fabric/Databricks
- [ ] Mention readiness to start April 1, 2026

---

## 🔗 Resources

### Azure Data Services (Priority Learning)
- [Azure Fundamentals](https://learn.microsoft.com/en-us/training/paths/azure-fundamentals/)
- [Azure Data Factory](https://learn.microsoft.com/en-us/azure/data-factory/)
- [Microsoft Fabric Overview](https://learn.microsoft.com/en-us/fabric/)

### Databricks
- [Databricks Academy](https://www.databricks.com/learn)
- [PySpark Basics](https://spark.apache.org/docs/latest/api/python/)

### ETL/ELT Best Practices
- Data pipeline design patterns
- Dimensional modeling fundamentals
- Data quality frameworks

---

## 📌 Quick Links

- **Job Posting:** [Vivicta Junior Consultant](https://tieto.wd3.myworkdayjobs.com/Tieto_Careers_External_Site/job/Finland-Espoo/Junior-Consultant_R125224)
- **Company Site:** [vivicta.com](https://www.vivicta.com)
- **Junior Stories:** [Meet Our People](https://www.vivicta.com/en/meet-our-people/24/junior-talent-tech-services-FI/)

---

## 📊 Application Checklist

- [ ] Complete CV update with data engineering focus
- [ ] Write tailored cover letter mentioning Data Engineer role
- [ ] Highlight relevant SQL/Python experience
- [ ] Mention interest in Azure/Fabric/Databricks
- [ ] State availability for April 1, 2026 start
- [ ] Submit via Workday by **January 18, 2025**
- [ ] Confirm Finnish and English language proficiency
- [ ] Mention hybrid work readiness (Espoo office)
