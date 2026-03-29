# `CustomLogger` Class Documentation

## 1. Introduction

`CustomLogger` is a utility class designed to provide a custom, robust, and informative logging solution for PySpark applications.

The main purpose of this class is to standardize the log format and automatically inject important contextual information—such as the class and function name where the log was called—into each log message. This makes monitoring and debugging complex Spark applications much easier and more effective.

## 2. Key Features

- **Dual Log Integration**: Supports writing logs simultaneously to both the standard Python logger (displayed on the console) and Spark's `Log4j` (useful for viewing logs in the Databricks or YARN UI).
- **Automatic Context**: Automatically retrieves and prefixes each log message with `ClassName.FunctionName:`.
- **Simple Interface**: Provides the familiar `info()`, `warn()`, and `error()` methods.
- **Spark Integration**: Automatically fetches the `app_id` and `app_name` from the active `SparkSession`.

## 3. How to Use

### Initializing the Logger

You need to initialize `CustomLogger` by passing in a `SparkSession` object.

```python
from pyspark.sql import SparkSession
from spark.sparklib.logging import CustomLogger

# 1. Create a SparkSession
spark = SparkSession.builder.appName("MyETLApp").getOrCreate()

# 2. Initialize the logger
# Set enable_log4j=True if you want logs to be written to Spark's Log4j system
logger = CustomLogger(spark, enable_log4j=True)
```

### Logging in Your Application

Use the `info`, `warn`, and `error` methods just like a standard logger.

```python
class DataProcessor:
    def __init__(self, logger: CustomLogger):
        self.logger = logger

    def read_source_data(self):
        self.logger.info("Starting to read source data.")
        # ... data reading logic
        self.logger.warn("Optional config file not found, using defaults.")
        
    def process_data(self):
        try:
            self.logger.info("Starting data processing.")
            # ... processing logic
            x = 1 / 0 # Simulate an error
        except Exception as e:
            self.logger.error(f"Data processing failed. Error: {e}")

# Usage
processor = DataProcessor(logger)
processor.read_source_data()
processor.process_data()
```

## 4. Log Output Example

With the code above, your log output on the console will look like this:

```
INFO:DATABRICKS-LOGGER:read_source_data.read_source_data: Starting to read source data.
WARNING:DATABRICKS-LOGGER:read_source_data.read_source_data: Optional config file not found, using defaults.
INFO:DATABRICKS-LOGGER:process_data.process_data: Starting data processing.
ERROR:DATABRICKS-LOGGER:process_data.process_data: Data processing failed. Error: division by zero
```

**Note**: The prefix `read_source_data.read_source_data` is due to the known limitation described below.