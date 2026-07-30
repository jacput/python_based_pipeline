import sys

def validate_required_columns(df, required_columns, logger):
    missing_columns = set(required_columns) - set(df.columns)

    if missing_columns:
        logger.error("Missing columns: %s", missing_columns)
        raise ValueError(f"Missing required columns: {missing_columns}")
