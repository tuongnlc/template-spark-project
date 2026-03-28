from argparse import Namespace
from typing import Optional
# from pyspark.sql import SparkSession
from spark.configlib.parser.silver_job import SilverJobConfig
from spark.utils.jobargs import job_args_utils
import os
from spark.sparklib.spark import start_spark

def main(
    args: Namespace,
    spark_session: Optional[SparkSession] = None
):  
    if not isinstance(args.job_config, SilverJobConfig): # Check job_config is of type SilverJobConfig  
        raise ValueError("job_config must be of type SilverJobConfig")

    spark_config: dict = {
        "spark.sql.parquet.compression.codec": "snappy",
    }

    # spark, logger = start_spark(spark_config)

    spark = start_spark(
        app_name="SilverJob",
        spark_config=spark_config,
        spark_session=spark_session
    )

    s3_extractor = S3Extractor(spark)

    # s3_extractor.extract()

    # s3_extractor.write()

if __name__ == "__main__":
    args = job_args_utils()

    if os.getenv("ENV", "") == "local":
        main(args=args)
    else:
        main(args=args)   
