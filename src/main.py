import pandas as pd
import sys
from datetime import date
from pathlib import Path

from config import load_config
from csv_loader import csv_loader
from logger import setup_logger
import logger
from validator import validate_required_columns
from database import create_database_engine, upload_to_staging  

todays_date = date.today().strftime("%m%d%Y")
# Open the config file and parse its contents

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "config.json"

REQUIRED_COLUMNS = [
    "OrderID",
    "OrderDate",
    "CustomerID",
    "Product",
    "Qty",
    "UnitPrice",
    "State"
]

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

    try:
        df = csv_loader(source_file_with_date, logger)
    except Exception as e:
        logger.error("Error loading CSV file: %s", e)
        sys.exit(1)

    try:
        validate_required_columns(df, REQUIRED_COLUMNS, logger)
    except ValueError as e:
        logger.error("Validation failed: %s", e)
        sys.exit(1)

    logger.info("File loaded successfully with all required columns.")

    engine = None

    try:
        engine = create_database_engine(config_data["database_config"])
        upload_to_staging(df, source_file_with_date_str, engine)
        logger.info("Data uploaded to staging table successfully.")
    except Exception as e:
        logger.error("Error uploading data to staging table: %s", e)
        sys.exit(1)
    finally:
        if engine:
            engine.dispose()  # Ensure the database connection is closed

    sys.exit(0)  # Graceful success exit

if __name__ == "__main__":
    main()