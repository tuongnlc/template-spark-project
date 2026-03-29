from abc import ABC, abstractmethod
from spark.sparklib.logging import CustomLogger
from pyspark.sql import DataFrame, SparkSession


class Loader(ABC):
    def __init__(self, logger: CustomLogger, spark: SparkSession):
        self.logger = logger
        self.spark = spark

    @abstractmethod
    def load(self, df: DataFrame, *args, **kwargs) -> DataFrame:
        pass

    @abstractmethod
    def optimize(self) -> None:
        pass
