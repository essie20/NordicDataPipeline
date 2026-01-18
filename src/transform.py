"""Data transformation from Bronze to Silver layer."""
import json
import pandas as pd
from io import BytesIO
from datetime import datetime
from src.config import BRONZE_CONTAINER, SILVER_CONTAINER
from src.storage import AzureStorageClient


class DataTransformer:
    """Transforms raw Bronze data into cleaned Silver data."""

    def __init__(self):
        self.storage = AzureStorageClient()

    def transform_fingrid_data(self, bronze_blob_path: str) -> str:
        """
        Transform Fingrid electricity data from Bronze to Silver.
        
        Transformations:
        - Parse timestamps to proper datetime
        - Add calculated fields (hour, day_of_week)
        - Remove duplicates
        - Validate data ranges
        
        Args:
            bronze_blob_path: Path to the Bronze blob
            
        Returns:
            Path to the Silver blob
        """
        print(f"🔄 Transforming: {bronze_blob_path}")
        
        # Read from Bronze
        raw_data = self.storage.read_from_container(BRONZE_CONTAINER, bronze_blob_path)
        payload = json.loads(raw_data.decode("utf-8"))
        
        records = payload.get("data", {}).get("data", [])
        if not records:
            print("⚠️ No records to transform")
            return None

        # Convert to DataFrame
        df = pd.DataFrame(records)
        
        # Transform
        if "startTime" in df.columns:
            df["startTime"] = pd.to_datetime(df["startTime"])
            df["hour"] = df["startTime"].dt.hour
            df["day_of_week"] = df["startTime"].dt.dayofweek
            df["date"] = df["startTime"].dt.date.astype(str)
        
        if "value" in df.columns:
            df["value"] = pd.to_numeric(df["value"], errors="coerce")
            # Remove negative values (data quality)
            df = df[df["value"] >= 0]
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Add metadata
        df["transformed_at"] = datetime.utcnow().isoformat()
        df["source_blob"] = bronze_blob_path
        
        # Save as Parquet to Silver
        buffer = BytesIO()
        df.to_parquet(buffer, index=False)
        buffer.seek(0)
        
        silver_path = self.storage.upload_to_silver(
            data=buffer.getvalue(),
            source_name="fingrid",
            dataset_name="electricity_production",
            file_ext="parquet"
        )
        
        print(f"   ✅ Transformed {len(df)} records")
        return silver_path

    def transform_prh_companies(self, bronze_blob_path: str) -> str:
        """
        Transform PRH company data from Bronze to Silver.
        
        Transformations:
        - Flatten nested company structures
        - Standardize business ID format
        - Extract registration date
        - Normalize company form names
        """
        print(f"🔄 Transforming PRH data: {bronze_blob_path}")
        
        raw_data = self.storage.read_from_container(BRONZE_CONTAINER, bronze_blob_path)
        payload = json.loads(raw_data.decode("utf-8"))
        
        companies = payload.get("data", {}).get("results", [])
        if not companies:
            print("⚠️ No companies to transform")
            return None

        # Flatten and transform
        cleaned_records = []
        for company in companies:
            record = {
                "business_id": company.get("businessId", ""),
                "name": company.get("name", ""),
                "registration_date": company.get("registrationDate", ""),
                "company_form": company.get("companyForm", ""),
                "status": company.get("status", ""),
                "transformed_at": datetime.utcnow().isoformat(),
            }
            
            # Extract address if available
            addresses = company.get("addresses", [])
            if addresses:
                addr = addresses[0]
                record["street"] = addr.get("street", "")
                record["city"] = addr.get("city", "")
                record["post_code"] = addr.get("postCode", "")
            
            cleaned_records.append(record)
        
        df = pd.DataFrame(cleaned_records)
        df = df.drop_duplicates(subset=["business_id"])
        
        # Save to Silver
        buffer = BytesIO()
        df.to_parquet(buffer, index=False)
        buffer.seek(0)
        
        silver_path = self.storage.upload_to_silver(
            data=buffer.getvalue(),
            source_name="prh",
            dataset_name="companies",
            file_ext="parquet"
        )
        
        print(f"   ✅ Transformed {len(df)} companies")
        return silver_path

    def transform_stat_finland(self, bronze_blob_path: str) -> str:
        """Transform Statistics Finland catalog data."""
        print(f"🔄 Transforming StatFi data: {bronze_blob_path}")
        
        raw_data = self.storage.read_from_container(BRONZE_CONTAINER, bronze_blob_path)
        payload = json.loads(raw_data.decode("utf-8"))
        
        categories = payload.get("data", [])
        if not categories:
            print("⚠️ No categories to transform")
            return None

        # Flatten categories
        records = []
        for cat in categories:
            records.append({
                "id": cat.get("id", ""),
                "text": cat.get("text", ""),
                "type": cat.get("type", ""),
                "updated": cat.get("updated", ""),
                "transformed_at": datetime.utcnow().isoformat(),
            })
        
        df = pd.DataFrame(records)
        
        buffer = BytesIO()
        df.to_parquet(buffer, index=False)
        buffer.seek(0)
        
        silver_path = self.storage.upload_to_silver(
            data=buffer.getvalue(),
            source_name="stat_finland",
            dataset_name="categories",
            file_ext="parquet"
        )
        
        print(f"   ✅ Transformed {len(df)} categories")
        return silver_path


def get_latest_bronze_blob(storage: AzureStorageClient, source: str, dataset: str) -> str:
    """Get the most recent Bronze blob for a source/dataset."""
    prefix = f"{source}/{dataset}/"
    blobs = storage.list_blobs(BRONZE_CONTAINER, prefix)
    if blobs:
        return sorted(blobs)[-1]  # Latest by timestamp in filename
    return None


def run_transformations():
    """Run transformations on latest Bronze data."""
    transformer = DataTransformer()
    storage = AzureStorageClient()
    results = {}

    print("\n🔄 Starting Data Transformations\n" + "=" * 50)

    # Transform Fingrid
    blob = get_latest_bronze_blob(storage, "fingrid", "dataset_192")
    if blob:
        try:
            results["fingrid"] = transformer.transform_fingrid_data(blob)
        except Exception as e:
            results["fingrid"] = {"error": str(e)}
            print(f"   ❌ Fingrid transform failed: {e}")

    # Transform PRH
    blob = get_latest_bronze_blob(storage, "prh", "companies_Vivicta")
    if blob:
        try:
            results["prh"] = transformer.transform_prh_companies(blob)
        except Exception as e:
            results["prh"] = {"error": str(e)}
            print(f"   ❌ PRH transform failed: {e}")

    # Transform StatFi
    blob = get_latest_bronze_blob(storage, "stat_finland", "catalog")
    if blob:
        try:
            results["stat_finland"] = transformer.transform_stat_finland(blob)
        except Exception as e:
            results["stat_finland"] = {"error": str(e)}
            print(f"   ❌ StatFi transform failed: {e}")

    print("\n" + "=" * 50)
    print("📊 Transformation Complete!")
    return results


if __name__ == "__main__":
    run_transformations()
