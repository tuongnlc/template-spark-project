from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DeltaTableConfig:
    s3_bucket: str
    catalog_name: str
    schema_name: str
    table_name: str
    date_partition_column: Optional[str] = None
    optimize_compaction: bool = False
    optimize_zorder_columns: list[str] = field(default_factory=list)
    s3_path_prefix: str = ""

    @property
    def databricks_table_name(self) -> str:
        return f"{self.catalog_name}.{self.schema_name}.{self.table_name}"

    @property
    def delta_table_s3_path(self) -> str:
        prefix: str = ""
        if self.s3_path_prefix:
            prefix = f"{self.s3_path_prefix}/"
        return (
            f"s3://{self.s3_bucket}/{prefix}{self.catalog_name}/{self.schema_name}/{self.table_name}"
        )