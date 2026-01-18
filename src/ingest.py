"""Data ingestion from Nordic public APIs to Bronze layer."""
import requests
from datetime import datetime
from src.config import API_ENDPOINTS, FINGRID_API_KEY
from src.storage import AzureStorageClient


class DataIngester:
    """Ingests data from various Nordic public APIs."""

    def __init__(self):
        self.storage = AzureStorageClient()
        self.headers = {"User-Agent": "NordicDataFlow/1.0"}

    def ingest_stat_finland(self, category: str = None) -> dict:
        """
        Ingest data from Statistics Finland (StatFi).
        
        Args:
            category: Optional category path to fetch specific data
            
        Returns:
            Ingestion result with blob path
        """
        url = API_ENDPOINTS["stat_finland"]
        if category:
            url += category

        print(f"📥 Fetching from Statistics Finland: {url}")
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        data = response.json()

        # Add metadata
        payload = {
            "source": "statistics_finland",
            "ingested_at": datetime.utcnow().isoformat(),
            "category": category,
            "data": data
        }

        blob_path = self.storage.upload_to_bronze(
            data=payload,
            source_name="stat_finland",
            dataset_name=category or "catalog"
        )

        return {"status": "success", "blob_path": blob_path, "records": len(data)}

    def ingest_prh_companies(self, name: str = None, business_id: str = None) -> dict:
        """
        Ingest company data from PRH (Finnish Patent and Registration Office).
        
        Args:
            name: Company name to search
            business_id: Business ID (Y-tunnus) to search
            
        Returns:
            Ingestion result with blob path
        """
        url = API_ENDPOINTS["prh_ytj"]
        params = {}
        if name:
            params["name"] = name
        if business_id:
            params["businessId"] = business_id

        print(f"📥 Fetching from PRH YTJ: {url}")
        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()
        data = response.json()

        # Add metadata
        payload = {
            "source": "prh_ytj",
            "ingested_at": datetime.utcnow().isoformat(),
            "query": params,
            "data": data
        }

        query_id = name or business_id or "all"
        blob_path = self.storage.upload_to_bronze(
            data=payload,
            source_name="prh",
            dataset_name=f"companies_{query_id}"
        )

        results = data.get("results", [])
        return {"status": "success", "blob_path": blob_path, "records": len(results)}

    def ingest_eurostat(self, dataset_code: str, params: dict = None) -> dict:
        """
        Ingest data from Eurostat.
        
        Args:
            dataset_code: Eurostat dataset code (e.g., 'nama_10_gdp')
            params: Additional query parameters
            
        Returns:
            Ingestion result with blob path
        """
        url = f"{API_ENDPOINTS['eurostat']}{dataset_code}"
        query_params = {"format": "JSON", "lang": "EN"}
        if params:
            query_params.update(params)

        print(f"📥 Fetching from Eurostat: {dataset_code}")
        response = requests.get(url, params=query_params, headers=self.headers)
        response.raise_for_status()
        data = response.json()

        # Add metadata
        payload = {
            "source": "eurostat",
            "ingested_at": datetime.utcnow().isoformat(),
            "dataset_code": dataset_code,
            "data": data
        }

        blob_path = self.storage.upload_to_bronze(
            data=payload,
            source_name="eurostat",
            dataset_name=dataset_code
        )

        return {"status": "success", "blob_path": blob_path, "label": data.get("label")}

    def ingest_fingrid(self, dataset_id: int, page_size: int = 100) -> dict:
        """
        Ingest electricity data from Fingrid Open Data.
        
        Args:
            dataset_id: Fingrid dataset ID (e.g., 192 for production)
            page_size: Number of records to fetch
            
        Returns:
            Ingestion result with blob path
        """
        if not FINGRID_API_KEY:
            raise ValueError("FINGRID_API_KEY not set in environment")

        url = f"{API_ENDPOINTS['fingrid']}{dataset_id}/data"
        headers = {
            **self.headers,
            "x-api-key": FINGRID_API_KEY
        }
        params = {"pageSize": page_size}

        print(f"📥 Fetching from Fingrid: Dataset {dataset_id}")
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        # Add metadata
        payload = {
            "source": "fingrid",
            "ingested_at": datetime.utcnow().isoformat(),
            "dataset_id": dataset_id,
            "data": data
        }

        blob_path = self.storage.upload_to_bronze(
            data=payload,
            source_name="fingrid",
            dataset_name=f"dataset_{dataset_id}"
        )

        records = data.get("data", [])
        return {"status": "success", "blob_path": blob_path, "records": len(records)}


def run_full_ingestion():
    """Run a full ingestion cycle for all data sources."""
    ingester = DataIngester()
    results = {}

    print("\n🚀 Starting Full Data Ingestion\n" + "=" * 50)

    # 1. Statistics Finland - Categories catalog
    try:
        results["stat_finland"] = ingester.ingest_stat_finland()
        print(f"   ✅ StatFi: {results['stat_finland']['records']} categories")
    except Exception as e:
        results["stat_finland"] = {"status": "error", "error": str(e)}
        print(f"   ❌ StatFi: {e}")

    # 2. PRH - Sample companies (Tietoevry/Vivicta)
    try:
        results["prh_vivicta"] = ingester.ingest_prh_companies(name="Vivicta")
        print(f"   ✅ PRH (Vivicta): {results['prh_vivicta']['records']} companies")
    except Exception as e:
        results["prh_vivicta"] = {"status": "error", "error": str(e)}
        print(f"   ❌ PRH: {e}")

    # 3. Eurostat - GDP data
    try:
        results["eurostat"] = ingester.ingest_eurostat(
            "nama_10_gdp", 
            {"lastTimePeriod": "5"}
        )
        print(f"   ✅ Eurostat: {results['eurostat']['label']}")
    except Exception as e:
        results["eurostat"] = {"status": "error", "error": str(e)}
        print(f"   ❌ Eurostat: {e}")

    # 4. Fingrid - Electricity production
    try:
        results["fingrid"] = ingester.ingest_fingrid(192, page_size=10)
        print(f"   ✅ Fingrid: {results['fingrid']['records']} records")
    except Exception as e:
        results["fingrid"] = {"status": "error", "error": str(e)}
        print(f"   ❌ Fingrid: {e}")

    print("\n" + "=" * 50)
    print("📊 Ingestion Complete!")
    return results


if __name__ == "__main__":
    run_full_ingestion()
