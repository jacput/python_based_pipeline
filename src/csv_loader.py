import pandas as pd

def csv_loader(file_path, logger):
    try:
        logger.info("Starting to load the CSV file.")
        df = pd.read_csv(file_path)
        logger.info("CSV file loaded successfully.  Location of the file: %s", file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error loading csv file {file_path}: {e}") from e
    logger.info("First 5 rows of the DataFrame:")
    logger.info("\n%s", df.head())
    row_count = len(df)
    logger.info("Number of rows in the DataFrame: %d", row_count)
    return df