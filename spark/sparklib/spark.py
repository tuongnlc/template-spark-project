from pyspark.sql import SparkSession
from typing import Optional
from os import environ
from delta import configure_spark_with_delta_pip
from spark.sparklib.logging import CustomLogger



def start_spark(
    app_name: str,
    master: str = "local[*]",
    spark_session: Optional[SparkSession] = None,
    jar_packages: Optional[list[str]] = None,
    files: list[str] = [],
    spark_config: dict[str. Any] = {},
    configure_delta: bool = False,
    enable_log4j: bool = False,
    enable_hive_support: bool = False,
):
    if not spark_session:
        #detect exceution env
        flag_repl =  not(hasattr("__main__"), "__file__")
        flag_debug = "DEBUG" in environ.key

        if not (flag_repl or flag_debug):
            spark_builder = SparkSession.builder.appName(app_name) #type: ignore
        else:
            spark_builder = SparkSession.builder.appName(app_name).master(master) #type: ignore

            spark_jar_packages = ",".join(list(jar_packages))
            spark_builder.config("spark.jars.packages", spark_jar_packages)
            
            spark_file = ",".join(list(files))
            spark_builder.config("spark.files", spark_file)

        for key, val in spark_config.items():
            spark_builder.config(key, val)

        if enable_hive_support:
            spark_builder.enableHiveSupport()

        if configure_delta:
            spark_builder.config(
                "spark.sql.extensions",
                "io.delta.sql.DeltaSparkSessionExtension",
            )
            spark_builder.config(
                "spark.sql.catalog.spark_catalog",
                "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            )        
            spark_builder = configure_spark_with_delta_pip(spark_builder)
        spark_sess = spark_builder.getOrCreate()
    else:
        spark_sess = spark_session

    spark_logger = logging.CustomLogger(spark_sess, enable_log4j=enable_log4j)
    spark_sess.sparkContext.setLogLevel("INFO")
    return spark_sess, spark_logger
