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

def audit_start(engine, logger, filename, batch_id, pipeline_name):

    query_audit_start = text("""
        SET NOCOUNT ON;
        DECLARE @out_audit_id INT;
        EXEC [dbo].[usp_AuditStart] @p_SourceFileName = :filename, @p_BatchId = :batch_id, @p_PipelineName = :pipeline_name, @o_NewAuditId = @out_audit_id OUTPUT;
        SELECT @out_audit_id AS new_audit_id;
        """)
    
    try:    
        with engine.begin() as conn:
            result = conn.execute(query_audit_start, {"filename": filename, "batch_id": batch_id, "pipeline_name": pipeline_name})
            new_audit_id = result.scalar()
            logger.info(f"Stored procedure usp_AuditStart executed successfully for batch_id: {batch_id}, new_audit_id: {new_audit_id}")
        return new_audit_id
    except Exception as e:
        raise Exception(f"Error executing audit start stored procedure: {e}") from e


def audit_end(engine, logger, audit_id, rows_read, rows_staged, rows_loaded, rows_failed, status, error_message):

    query_audit_end = text("""
        SET NOCOUNT ON;
        DECLARE @out_audit_id INT;
        EXEC [dbo].[usp_AuditUpdate] @p_AuditId = :audit_id, @p_RowsRead = :rows_read, @p_RowsStaged = :rows_staged, @p_RowsLoaded = :rows_loaded, @p_RowsFailed = :rows_failed, @p_Status = :status, @p_ErrorMessage = :error_message;
        """)
    
    try:    
        with engine.begin() as conn:
            result = conn.execute(query_audit_end, {"audit_id": audit_id, "rows_read": rows_read, "rows_staged": rows_staged, "rows_loaded": rows_loaded, "rows_failed": rows_failed, "status": status, "error_message": error_message})
            logger.info(f"Stored procedure usp_AuditEnd executed successfully for audit_id: {audit_id}")
    except Exception as e:
        raise Exception(f"Error executing audit end stored procedure: {e}") from e
    
