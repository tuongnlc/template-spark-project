from abc import ABC, abstractmethod
from pyspark.sql import DataFrame, SparkSession
from spark.sparklib.logging import CustomLogger



class Transform(ABC):
    def __init__(
        self, 
        spark: SparkSession,
        logger: CustomLogger,
    ):
        self.spark = spark
        self.logger = logger

    @abstractmethod
    def transform(self, df: DataFrame) -> DataFrame:
        raise NotImplementedError("transform method must be implemented")