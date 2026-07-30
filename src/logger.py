import sys
import logging
#from datetime import date

def setup_logger (log_file_path, caller_name):

    logging.basicConfig(
            filename=log_file_path,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            filemode='w'
    )
    logger = logging.getLogger(caller_name)    
    return logger