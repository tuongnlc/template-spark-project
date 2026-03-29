from argparse import Namespace
from typing import Optional
# from pyspark.sql import SparkSession
from spark.configlib.parser.silver_job import SilverJobConfig
from spark.utils.jobargs import job_args_utils
import os
from spark.sparklib.spark import start_spark
# from spark.extractors.s3_extractor import S3Extractor
from spark.sparklib.extractor.s3 import S3Extractor
from spark.sql import SparkSession

from spark.sparklib.loader.delta import DeltaLoader
from spark.template.silver_layer.silverr_job import SilverJob



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

    spark, logger = start_spark(
        app_name="SilverJob",
        spark_config=spark_config,
        spark_session=spark_session,
        enable_log4j=True,
        enable_hive_support=True,
    )

    s3_extractor = S3Extractor(
        spark=spark,
        logger=logger,
        s3_paths=args.job_config.s3_paths,
        s3_client_kwargs=args.job_config.s3_client_kwargs,
    )

    transform_class = [
        tf_config.python_class(logger=logger, **tf_config.kwargs)
        for tf_config in args.job_config.transform_configs
    ]

    delta_loader = DeltaLoader(
        spark=spark,
        logger=logger,
        write_mode='overwrite',
        hive_table_name=args.job_config.hive_table_name,
        delta_table_path=args.job_config.delta_table_path,
        overwrite_partition=True,
        options={
            "delta.columnMapping.mode": "name",
            "overwriteSchema": "true",
        }
    )

    job: SilverJob = SilverJob(
        spark=spark,
        logger=logger,
        s3_extractor=s3_extractor,
        transform_class=transform_class,
        delta_loader=delta_loader,
        cfg=args.job_config,
    )
    job.run()

if __name__ == "__main__":
    args = job_args_utils()

    if os.getenv("ENV", "") == "local":
        main(args=args)
    else:
        main(args=args)   
