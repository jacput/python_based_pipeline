import urllib
import pandas as pd
from sqlalchemy import create_engine, text, Engine
from datetime import datetime, timezone

STAGING_TABLE = "SalesStaging"

def create_database_engine(database_config):    
    try:
        server = database_config["server"]
        database = database_config["database"]
        driver = database_config["driver"]

        # 'Trusted_Connection=yes' enforces Windows Authentication
        params = urllib.parse.quote_plus( # type: ignore
            f"DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
        )

        engine = create_engine(
            f"mssql+pyodbc:///?odbc_connect={params}", 
            fast_executemany=True  # Essential for fast staging uploads
        )
        return engine
    except Exception as e:
        raise Exception(f"Error creating database engine: {e}") from e

def upload_to_staging(df: pd.DataFrame, source_file_string: str, engine: Engine, batch_id: str) -> None:

    """"
    Loads the DataFrame into the SalesStaging table.

    Adds ETL metadata columns including:
    - source_file_name
    - inserted_at
    - batch_id
    """     

    try:    

        df["source_file_name"] = source_file_string  # Use the provided source file name
        df['inserted_at'] = pd.Timestamp.now()
        df['batch_id'] = batch_id  # Add a batch_id column for tracking

        with engine.begin() as connection:
            connection.execute(text(f"TRUNCATE TABLE dbo.{STAGING_TABLE}"))

            # --- 2. Load Existing DataFrame into Staging Table ---
            # Assuming 'your_existing_df' is your massive DataFrame
            df.to_sql(
            name=STAGING_TABLE,  # Target table in the database
            con=connection,
            if_exists="append",  # Clears and recreates the staging schema each run
            index=False,
            chunksize=25000       # Controls the number of rows written per batch
            )

    except Exception as e:
        raise Exception(f"Error uploading to staging table: {e}") from e


