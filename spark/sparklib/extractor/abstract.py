from abc import ABC, abstractmethod

from pyspark.sql import DataFrame, SparkSession

from spark.logging import CustomLogger


class Extractor(ABC):
    def __init__(self, logger: CustomLogger, spark: SparkSession):
        self.logger = logger
        self.spark = spark

    @abstractmethod
    def read(self, *args, **kwargs) -> DataFrame:
        pass