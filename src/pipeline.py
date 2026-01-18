"""Main ETL pipeline orchestrator."""
from datetime import datetime
from src.ingest import run_full_ingestion
from src.transform import run_transformations
from src.database import initialize_database, GoldLoader, DatabaseManager
from src.storage import AzureStorageClient
from src.config import SILVER_CONTAINER


def run_pipeline(skip_ingest: bool = False, skip_transform: bool = False, skip_load: bool = False):
    """
    Run the complete ETL pipeline.
    
    Args:
        skip_ingest: Skip the ingestion phase (use existing Bronze data)
        skip_transform: Skip transformation phase (use existing Silver data)
        skip_load: Skip loading to Gold/SQL
    """
    print("\n" + "=" * 60)
    print("🌊 NordicDataFlow Pipeline - Starting")
    print(f"⏰ Run Time: {datetime.utcnow().isoformat()}")
    print("=" * 60)

    results = {
        "ingest": None,
        "transform": None,
        "load": None,
        "status": "started"
    }

    # Phase 1: Ingest (APIs -> Bronze)
    if not skip_ingest:
        print("\n📥 PHASE 1: INGESTION (Bronze Layer)")
        print("-" * 40)
        try:
            results["ingest"] = run_full_ingestion()
        except Exception as e:
            print(f"❌ Ingestion failed: {e}")
            results["ingest"] = {"error": str(e)}
    else:
        print("\n⏭️ Skipping ingestion phase")

    # Phase 2: Transform (Bronze -> Silver)
    if not skip_transform:
        print("\n🔄 PHASE 2: TRANSFORMATION (Silver Layer)")
        print("-" * 40)
        try:
            results["transform"] = run_transformations()
        except Exception as e:
            print(f"❌ Transformation failed: {e}")
            results["transform"] = {"error": str(e)}
    else:
        print("\n⏭️ Skipping transformation phase")

    # Phase 3: Load (Silver -> Gold/SQL)
    if not skip_load:
        print("\n📤 PHASE 3: LOADING (Gold Layer)")
        print("-" * 40)
        try:
            loader = GoldLoader()
            storage = AzureStorageClient()
            load_results = {}
            
            # Find latest Silver blobs and load
            silver_blobs = storage.list_blobs(SILVER_CONTAINER)
            
            for blob in silver_blobs:
                if "companies" in blob:
                    load_results["companies"] = loader.load_companies(blob)
                elif "electricity" in blob:
                    load_results["electricity"] = loader.load_electricity(blob)
            
            results["load"] = load_results
        except Exception as e:
            print(f"❌ Loading failed: {e}")
            results["load"] = {"error": str(e)}
    else:
        print("\n⏭️ Skipping load phase")

    results["status"] = "completed"
    
    print("\n" + "=" * 60)
    print("🏁 Pipeline Complete!")
    print("=" * 60)
    
    return results


def setup():
    """Initialize the database schema."""
    print("🔧 Initializing NordicDataFlow...")
    initialize_database()
    print("✅ Setup complete!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "setup":
        setup()
    else:
        # Run full pipeline
        run_pipeline()
