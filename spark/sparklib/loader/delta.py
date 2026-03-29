from spark.sparklib.loader.abstract import Loader
from spark.sparklib.logging import CustomLogger
from pyspark.sql import DataFrame, SparkSession

from typing import Optional
from pyspark.sql import DataFrameWriter
from delta.tables import DeltaTable, DeltaMergeBuilder



class DeltaLoader(Loader):
    def __init__(self, 
        logger: CustomLogger, 
        spark: SparkSession,
        delta_table_path: str,
        write_mode: str = "overwrite",
        hive_table_name: Optional[str] = "",
        partition_by: Optional[list[str]] = None,
        overwrite_partition: bool = False,
        overwrite_schema: bool = False,
        merge_schema: bool = False,
        fail_if_df_empty: bool = False,
    ):
        super().__init__(logger, spark)
        self.delta_table_path = delta_table_path
        self.write_mode = write_mode
        self.hive_table_name = hive_table_name
        self.partition_by = partition_by
        self.overwrite_partition = overwrite_partition
        self.overwrite_schema = overwrite_schema
        self.merge_schema = merge_schema
        self.fail_if_df_empty = fail_if_df_empty

    def write(
        self, 
        df: DataFrame,
        extra_options: dict[str, str] = {},
        *args,
        **kwargs,
    ):
        if self.fail_if_df_empty and df.empty:
            raise ValueError("DataFrame is empty")

        writer: DataFrameWriter = (
            df.write.format("delta")
            .mode(self.write_mode)
            .option("encoding", "utf-8")
            .option("path", self.delta_table_path)
        )

        if self.partition_by:
            writer = writer.partitionBy(*self.partition_by)

        if self.merge_schema:
            writer = writer.option("mergeSchema", "true")

        if self.overwrite_partition: #Only append specific partition
            writer = writer.option("partitionOverwriteMode", "dynamic")
        else:
            if self.overwrite_schema: #Allow write override schema
                writer = writer.option("overwriteSchema", "true")

        for key, value in (self.options | extra_options).items():
            writer = writer.option(key, value)

        if self.hive_table_name:
            self.logger.info(f"Writing to Hive table: {self.hive_table_name}")
            # writer = writer.option("hiveTable", self.hive_table_name)
            writer.saveAsTable(self.hive_table_name)
            return

        self.logger.info(f"Writing to Delta table: {self.delta_table_path}")
        writer.save()

    def optimize(self):
        self.logger.info(f"Optimizing Delta table: {self.delta_table_path}")

        delta_table = DeltaTable.forPath(self.spark, self.delta_table_path)
        delta_table.optimize().executeZOrderBy("start_at")        
        delta_table.optimize().executeCompaction()


class DeltaMergeLoader(Loader):
    pass #Update here