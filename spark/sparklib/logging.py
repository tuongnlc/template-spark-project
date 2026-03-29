import inspect
import logging
from pyspark.sql import SparkSession


class CustomLogger:
    """
        Custom logger for Spark jobs to improve logging information with app_id and app_name prefix

        Example:
            - INFO:DATABRICKS-LOGGER:read_data.read_data: <message>
            - ERROR:DATABRICKS-LOGGER:read_data.read_data: <message>
    """
    def __init__(self, 
        spark: SparkSession,
        enable_log4j: bool = False, 
        str_logger_name: str = "DATABRICKS-LOGGER"
    ):
        logging.basicConfig()
        logging.getLogger().setLevel(logging.INFO)

        app_id: str = spark.conf.get("spark.app.id") or "app_id_not_found"
        app_name: str = spark.conf.get("spark.app.name") or "app_name_not_found"
        
        self.log4j_enabled = enable_log4j

        if self.log4j_enabled:
            log4j = spark._jvm.org.apache.log4j
            message_prefix: str = f"{app_id} {app_name} "
            self.log4j_logger = log4j.getLogger(str_logger_name)
                  
        self.std_logger = logging.getLogger(str_logger_name)

    def log4j_error(self, message: str):
        if self.log4j_enabled:
            self.log4j_logger.error(message)
    
    def log4j_warn(self, message: str):
        if self.log4j_enabled:
            self.log4j_logger.warn(message)

    def log4j_info(self, message: str):
        if self.log4j_enabled:
            self.log4j_logger.info(message)

    def std_error(self, message: str):
        self.std_logger.error(message)

    def std_warn(self, message: str):
        self.std_logger.warning(message)

    def std_info(self, message: str):
        self.std_logger.info(message)

    def error(self, message: str):
        class_name, function_name = self._get_caller_info() 
        prefix_message = f"{class_name}.{function_name}: {message}"

        if self.log4j_enabled:
            self.log4j_logger.error(prefix_message)
        self.std_error(prefix_message)

    def warn(self, message: str):
        class_name, function_name = self._get_caller_info()
        prefix_message = f"{class_name}.{function_name}: {message}"

        if self.log4j_enabled:
            self.log4j_logger.warn(prefix_message)
        self.std_warn(prefix_message)

    def info(self, message: str):
        class_name, function_name = self._get_caller_info()
        prefix_message = f"{class_name}.{function_name}: {message}"

        if self.log4j_enabled:
            self.log4j_logger.info(prefix_message)
        self.std_info(prefix_message)
    
    def _get_caller_info(self):
        try:
            caller_frame = inspect.currentframe().f_back.f_back
            class_name = caller_frame.f_locals["self"].__class__.__name__ # Get class name from self object
            function_name = caller_frame.f_code.co_name # Get function name from frame code
        except Exception as e:
            self.std_error(f"Error in _get_caller_info: {e}")
            class_name = "unknown"
            function_name = "unknown"
        return class_name, function_name