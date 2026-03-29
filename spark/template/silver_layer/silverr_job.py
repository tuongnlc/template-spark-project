from spark.sql import SparkSession
from spark.sparklib.loggeing import CustomLogger
from spark.sparklib.extractor.abstract import Extractor
from spark.sparklib.loader.abstract import Loader
from spark.sparklib.transform.abstract import Transform
from spark.configlib.parser.silver_job import SilverJobConfig
from datetime import datetime



class SilverJob:
    def __init__(
        self,
        spark: SparkSession,
        logger: CustomLogger,
        cfg: SilverJobConfig,
        s3_extractor: Extractor,
        loader: Loader,
        transforms: list[Transform]=[]
    ):
        self.spark = spark
        self.logger = logger
        self.cfg = cfg
        self.s3_extractor = s3_extractor
        self.loader = loader
        self.transforms = transforms

    def run_vacuum(self):
        today = datetime.now()
        today_weekday = today.weekday()

        if today_weekday == 0:
            self.spark.sql(
                f"ALTER TABLE {self.loader.hive_table_name} SET TBLPROPERTIES (delta.deletedFileRetentionDuration='interval 7 days)"
            )
            self.spark.sql(
                f"ALTER TABLE {self.loader.hive_table_name} SET TBLPROPERTIES (delta.logRetentionDuration='interval 7 days)"
            )
            self.spark.sql(f"VACUUM {self.loader.hive_table_name}")
            self.logger.info(f"Vacuum {self.loader.hive_table_name}")
        else:
            self.logger.info(f"Today is not monday. Skip vacuum {self.loader.hive_table_name}")

    def run(self):
        s3_paths = [
            f"s3a://{self.cfg.source_s3_bucket}/{self.cfg.scribe_database_name}/scribes/*/*/*.json"
        ]
        self.logger.info(f"Extract data from {s3_paths}")
       
        extracted_df = self.s3_extractor.read()

        transformed_df = extracted_df
        for tf in self.transforms:
            transformed_df = tf.transform(transformed_df)
        self.logger.info(f"Done transformed data from {s3_paths}")

        self.loader.write(transformed_df)
        self.loader.optimize()
        self.run_vacuum()

