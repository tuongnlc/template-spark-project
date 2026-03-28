from pyspark import SparkContext
from spark.logging import CustomLogger

class S3Extractor:
    def __init__(self, spark: SparkContext):
        self.spark = spark
        self.logger = CustomLogger(spark)
       