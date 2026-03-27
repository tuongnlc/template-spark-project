from argparse import Namespace
from typing import Optional
from pyspark.sql import SparkSession
from spark.configlib.parser.silver_job import SilverJobConfig
from spark.utils.jobargs import job_args_utils
import os

def main(
    args: Namespace,
    spark_session: Optional[SparkSession] = None
):
    if not isinstance(args.job_config, SilverJobConfig): # Check job_config is of type SilverJobConfig  
        raise ValueError("job_config must be of type SilverJobConfig")

if __name__ == "__main__":
    args = job_args_utils()

    if os.getenv("ENV", "") == "local":
        main(args=args)
    else:
        main(args=args, spark_session=spark)   
