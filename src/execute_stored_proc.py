from sqlalchemy import text

def validate_staging_batch(engine, batch_id, logger):

    return_code = None  # Initialize return_value to None

    query_validate = text("""
    DECLARE @RC INT;
    EXECUTE @RC = [dbo].[usp_SalesStagingValidate] @BatchId = :val1;
    SELECT @RC AS return_code;
    """)

    try:

        with engine.begin() as conn:
            result = conn.execute(query_validate, {"val1": batch_id})
            # Fetch the scalar result from the final SELECT statement
            return_code = result.scalar()
            logger.info(f"Return code from usp_SalesStagingValidate: {return_code}")

        if return_code is None:
            raise Exception("All rows could not be validated in usp_SalesStagingValidate.")
        else:
            return return_code
    except Exception as e:
        raise Exception(f"Error executing stored procedure: {e}") from e


def load_sales(engine, batch_id, logger):

    query_load = text("""
        DECLARE @out_val INT;
        EXEC [dbo].[ups_LoadSales];
        SELECT @out_val AS return_value;
        """)
    
    try:
        with engine.begin() as conn:
            conn.execute(query_load)
            logger.info(f"Stored procedure ups_LoadSales executed successfully for batch_id: {batch_id}")
    except Exception as e:
        raise Exception(f"Error executing stored procedure: {e}") from e

def audit_start(engine, batch_id, logger):

    query_load = text("""
        EXEC [dbo].[ups_AuditStart];
        """)
    
    try:
        with engine.begin() as conn:
            conn.execute(query_load)
            logger.info(f"Stored procedure ups_AuditStart executed successfully for batch_id: {batch_id}")
    except Exception as e:
        raise Exception(f"Error executing stored procedure: {e}") from e
