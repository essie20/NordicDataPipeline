"""Azure Blob Storage utilities for Medallion architecture."""
import json
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from src.config import (
    AZURE_STORAGE_CONNECTION_STRING,
    BRONZE_CONTAINER,
    SILVER_CONTAINER,
    GOLD_CONTAINER,
)


class AzureStorageClient:
    """Client for interacting with Azure Blob Storage."""

    def __init__(self):
        self.blob_service_client = BlobServiceClient.from_connection_string(
            AZURE_STORAGE_CONNECTION_STRING
        )

    def upload_to_bronze(self, data: dict, source_name: str, dataset_name: str) -> str:
        """
        Upload raw data to the Bronze (raw) layer.
        
        Args:
            data: Raw JSON data from API
            source_name: Name of the data source (e.g., 'fingrid', 'prh')
            dataset_name: Name of the specific dataset
            
        Returns:
            Blob path where data was stored
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        blob_name = f"{source_name}/{dataset_name}/{timestamp}.json"
        
        container_client = self.blob_service_client.get_container_client(BRONZE_CONTAINER)
        blob_client = container_client.get_blob_client(blob_name)
        
        blob_client.upload_blob(
            json.dumps(data, ensure_ascii=False, indent=2),
            overwrite=True
        )
        
        print(f"✅ Uploaded to bronze/{blob_name}")
        return blob_name

    def upload_to_silver(self, data: str, source_name: str, dataset_name: str, file_ext: str = "parquet") -> str:
        """
        Upload cleaned/validated data to the Silver layer.
        
        Args:
            data: Cleaned data (as bytes or string)
            source_name: Name of the data source
            dataset_name: Name of the dataset
            file_ext: File extension (default: parquet)
            
        Returns:
            Blob path where data was stored
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        blob_name = f"{source_name}/{dataset_name}/{timestamp}.{file_ext}"
        
        container_client = self.blob_service_client.get_container_client(SILVER_CONTAINER)
        blob_client = container_client.get_blob_client(blob_name)
        
        blob_client.upload_blob(data, overwrite=True)
        
        print(f"✅ Uploaded to silver/{blob_name}")
        return blob_name

    def upload_to_gold(self, data: str, entity_name: str, file_ext: str = "parquet") -> str:
        """
        Upload aggregated/final data to the Gold layer.
        
        Args:
            data: Final aggregated data
            entity_name: Name of the business entity
            file_ext: File extension
            
        Returns:
            Blob path where data was stored
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        blob_name = f"{entity_name}/{timestamp}.{file_ext}"
        
        container_client = self.blob_service_client.get_container_client(GOLD_CONTAINER)
        blob_client = container_client.get_blob_client(blob_name)
        
        blob_client.upload_blob(data, overwrite=True)
        
        print(f"✅ Uploaded to gold/{blob_name}")
        return blob_name

    def read_from_container(self, container: str, blob_name: str) -> bytes:
        """Read data from a specific container and blob."""
        container_client = self.blob_service_client.get_container_client(container)
        blob_client = container_client.get_blob_client(blob_name)
        return blob_client.download_blob().readall()

    def list_blobs(self, container: str, prefix: str = None) -> list:
        """List all blobs in a container with optional prefix filter."""
        container_client = self.blob_service_client.get_container_client(container)
        blobs = container_client.list_blobs(name_starts_with=prefix)
        return [blob.name for blob in blobs]
