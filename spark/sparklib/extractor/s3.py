from pyspark import SparkContext
from spark.logging import CustomLogger
from typing import Optional, Any
from pyspark.sql import DataFrame
from spark.sparklib.extractor.abstract import Extractor



class S3Extractor(Extractor):
    def __init__(
            self, 
            spark: SparkContext,
            s3_paths: list[str] = [],
            s3_client_kwargs: Optional[dict[str, Any]] = {},
        ):
        self.spark = spark
        self.logger = CustomLogger(spark)
        self.s3_paths = s3_paths
        self.s3_client_kwargs = s3_client_kwargs

    def read(self, s3_paths: list[str], *args, **kwargs) -> DataFrame:
        """
            Read data from S3
        """
        try:
            df = self.spark.read().format("parquet").load(s3_paths)
        except Exception as e:
            self.logger.error(f"Error reading data from S3: {e}")
            raise e
        return df

