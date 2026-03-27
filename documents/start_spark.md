# `start_spark` Function

## Overview

The `start_spark` function is a Python utility designed to initialize, configure, and return a `SparkSession` object. It simplifies the process of setting up a Spark session, supporting flexible configurations for both local development and production environments.

The function also includes built-in configurations for working with Delta Lake and Hive.

## Basic Usage

Below is an example of how to call the function to create a basic `SparkSession` for local development.

```python
from sparklib.spark import start_spark

# Initialize Spark Session with default configurations
spark, logger = start_spark(app_name="MySparkApp")

# Start using Spark
df = spark.createDataFrame([("Alice", 1), ("Bob", 2)], ["name", "id"])
df.show()

# Stop the Spark Session when done
spark.stop()
```

## Parameters

The `start_spark` function accepts the following parameters:

| Parameter | Type | Default Value | Description |
| --- | --- | --- | --- |
| `app_name` | `str` | (Required) | The name of the Spark application, which will be displayed in the Spark UI. |
| `master` | `str` | `"local[*]"` | The master URL for Spark to connect to. Defaults to `"local[*]"` to run locally using all available cores. This parameter is ignored if the code is run in a non-debug/REPL environment (e.g., via `spark-submit`). |
| `spark_session` | `Optional[SparkSession]` | `None` | Allows passing an existing `SparkSession`. If provided, the function will skip the creation process and return this session. |
| `jar_packages` | `Optional[list[str]]` | `None` | A list of Maven coordinates for JAR packages to be added to the Spark session (e.g., `['org.postgresql:postgresql:42.2.18']`). |
| `files` | `list[str]` | `[]` | A list of file paths to be sent to the Spark executors. |
| `spark_config` | `dict[str, Any]` | `{}` | A dictionary of custom Spark configuration key-value pairs (e.g., `{"spark.executor.memory": "2g"}`). |
| `configure_delta` | `bool` | `False` | If `True`, the function will automatically add the necessary configurations to enable Delta Lake support. |
| `enable_log4j` | `bool` | `False` | (Not yet implemented) This parameter is intended for configuring Log4j. |
| `enable_hive_support` | `bool` | `False` | If `True`, the function will enable Hive support, allowing Spark to interact with a Hive metastore. |

## Return Value

The function returns a tuple containing two elements:

1.  `spark_sess` (`SparkSession`): The initialized and configured `SparkSession` object.
2.  `spark_logger`: Currently always returns `None`. The logging functionality is not yet complete.

## Detailed Logic

### Environment Detection

The function includes a mechanism to distinguish between a development environment (local, debug, REPL) and a production environment (when run with `spark-submit`).

-   **Development/Debug Environment**: The function will use the provided `master` URL (defaulting to `local[*]`) and apply the `jar_packages` and `files` configurations. This is useful when running code directly from an IDE or notebook.
-   **Production Environment**: The function will **not** set the `master` URL, allowing the configuration from the `spark-submit` command line (e.g., `--master yarn`) to take precedence. This makes the code portable and deployable across different clusters without modification.

### Delta Lake Integration

When `configure_delta` is set to `True`, the function will automatically:
1.  Add the Delta Lake SQL extension to the Spark configuration.
2.  Set up the Delta Catalog.
3.  Call `configure_spark_with_delta_pip` to ensure the necessary Delta Lake JAR packages are added to the session.

## Notes and Warnings

*   **REPL Environment Detection**: The current logic `not(hasattr("__main__"), "__file__")` is likely syntactically incorrect. A more reliable approach is `not hasattr(__import__('__main__'), '__file__')`.
*   **DEBUG Environment Variable Check**: The logic `"DEBUG" in environ.key` will raise an error. The correct way to check for the existence of an environment variable is `"DEBUG" in environ`.
*   **Delta Catalog Configuration**: The line `spark_builder.builder.config(...)` is likely a mistake. `SparkSession.Builder` does not have a `.builder` attribute. The correct call should probably be `spark_builder.config(...)`.