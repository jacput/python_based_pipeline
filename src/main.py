import pandas as pd
import sys
from datetime import date
from pathlib import Path
from datetime import datetime, timezone

from config import load_config
from csv_loader import csv_loader
from logger import setup_logger
from validator import validate_required_columns
from database import create_database_engine, upload_to_staging, generic_sql_count_method
from execute_stored_proc import validate_staging_batch, load_sales, audit_start, audit_end

todays_date = date.today().strftime("%m%d%Y")
# Open the config file and parse its contents

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "config.json"
PIPELINE_NAME = "SalesPipeline"

REQUIRED_COLUMNS = [
    "OrderID",
    "OrderDate",
    "CustomerID",
    "Product",
    "Qty",
    "UnitPrice",
    "State"
]

VALIDATION_SUCCESS = 0


def main():   

    try:
        config_data = load_config(CONFIG_FILE)
    except Exception as e:  
        print(f"Error loading config: {e}")
        sys.exit(1)

    source_file_path = Path(config_data['source_file_path'])
    source_file_name = config_data['source_file_name']
    log_file_path = Path(config_data['logging_file_full_path'] + f"{todays_date}.log")

    try:
        logger = setup_logger(log_file_path, __name__)
    except Exception as e:
        print(f"Error setting up logger: {e}")
        sys.exit(1)

    logger.info("source_file_path: %s", source_file_path)
    logger.info("source_file_name: %s", source_file_name)
    logger.info("log_file_path: %s", log_file_path)

    source_file_full_path = source_file_path / source_file_name
    source_file_with_date = source_file_full_path.with_name(f"{source_file_full_path.stem}{todays_date}.csv")

    source_file_with_date_str = str(source_file_with_date)  # Convert Path object to string for logging

    batch_id = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")

    engine = None

    try:
        engine = create_database_engine(config_data["database_config"])       
    except Exception as e:
        logger.error("Error creating database engine: %s", e)
        sys.exit(1)

    new_audit_id = audit_start(engine, logger, source_file_with_date_str, batch_id, PIPELINE_NAME)

    try:
        df = csv_loader(source_file_with_date, logger)
    except Exception as e:
        logger.error("Error loading CSV file: %s", e)
        sys.exit(1)

    rows_read = len(df)

    audit_end(engine, logger, new_audit_id, rows_read, None, None, None, None, None)  # You can replace None with actual values if available


    try:
        validate_required_columns(df, REQUIRED_COLUMNS, logger)
    except ValueError as e:
        logger.error("Validation failed: %s", e)
        sys.exit(1)

    logger.info("File loaded successfully with all required columns.")

    

    try:
        upload_to_staging(df, source_file_with_date_str, engine, batch_id)
        rows_staged = generic_sql_count_method(engine, "SalesStaging", batch_id)
        audit_end(engine, logger, new_audit_id, None, rows_staged, None, None, None, None)  # You can replace None with actual values if available
        logger.info("Data uploaded to staging table successfully.")
        logger.info("Current batch_id: %s", batch_id)
        return_value = validate_staging_batch(engine, batch_id, logger)  # Pass the first batch_id to the stored procedure
        if return_value == VALIDATION_SUCCESS:
            logger.info("Stored procedure executed successfully.")
            load_sales(engine, batch_id, logger)
            rows_loaded = generic_sql_count_method(engine, "Sales", batch_id)
            audit_end(engine, logger, new_audit_id, None, None, rows_loaded, None, "Success", None)  # You can replace None with actual values if available                    
        if return_value > 0:
            logger.error("All rows could not be validated:, please check the data in batch %s, in SalesStagingValidation", batch_id)
            logger.info("Number of failed rows: %d", return_value)
            audit_end(engine, logger, new_audit_id, None, None, None, return_value, "ValidationFailed", "All rows could not be validated")  # You can replace None with actual values if available
            sys.exit(1)
    except Exception as e:
        logger.error("Error in data pipeline: %s", e)
        audit_end(engine, logger, new_audit_id, None, None, None, None, "Failed", str(e))
        sys.exit(1)
    finally:
        if engine:
            engine.dispose()  # Ensure the database connection is closed

    sys.exit(0)  # Graceful success exit

if __name__ == "__main__":
    main()