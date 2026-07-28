import pandas as pd
import sys
import logging
from datetime import date
import json
from pathlib import Path

todays_date = date.today().strftime("%m%d%Y")
# Open the config file and parse its contents


try:    
    with open('C:\\Users\\jputhiamada3\\OneDrive - DXC Production\\Desktop\\SalesPipeline\\config\\config.json', 'r', encoding='utf-8') as config_file:
        config_data = json.load(config_file)
except Exception as e:
    sys.exit(1)
else:
    source_file_path = Path(config_data.get('source_file_path'))
    source_file_name = config_data.get('source_file_name')
    log_file_path = Path(config_data.get('logging_file_full_path') + f"{todays_date}.log")
    logging.basicConfig(
    filename= log_file_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filemode='w'
    )
    logger = logging.getLogger(__name__)
    logger.info("source_file_path: %s", source_file_path)
    logger.info("source_file_name: %s", source_file_name)
    logger.info("log_file_path: %s", log_file_path)
    try:
        source_file_full_path = source_file_path / source_file_name
        source_file_with_date = source_file_full_path.with_name(f"{source_file_full_path.stem}{todays_date}.csv")
        logger.info("Starting to load the CSV file.")
        file_path = source_file_with_date
        df = pd.read_csv(file_path)
        logger.info("CSV file loaded successfully.  Location of the file: %s", file_path)
    except FileNotFoundError:
        logger.exception("File not found: %s", file_path)
        sys.exit(1)
    except Exception as e:
        logger.exception("Error loading file: %s", e)
        sys.exit(1)
    else:
        required_columns = [
        "OrderID",
        "OrderDate",
        "CustomerID",
        "Product",
        "Qty",
        "UnitPrice",
        "State"
        ]

        missing_columns = set(required_columns) - set(df.columns)

        if missing_columns:
            logger.exception("Missing columns: %s", missing_columns)
            sys.exit(1)

        # View the first 5 rows
        logger.info("First 5 rows of the DataFrame:")
        logger.info(df.head())
        row_count = len(df)
        logger.info("Number of rows in the DataFrame: %d", row_count)
        logger.info("File loaded successfully with all required columns.")
        sys.exit(0)  # Graceful success exit