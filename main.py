import os
import sys
from src.custom_exception import CustomException
from src.logger import auto_logger

logger = auto_logger(__name__)




if __name__ == "__main__":
    try:
        logger.info("This a test run of logger and main.py")
    
    except Exception as e:
        logger.error("Facing error in logger file")
        raise CustomException(e,sys)