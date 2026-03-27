from spark.configlib.parser.delta import DeltaTableConfig


def test_delta_table_config_initialization():
    """
        Test initializing DeltaTableConfig.

        Input:
            s3_bucket: S3 bucket name.
            catalog_name: Catalog name.
            schema_name: Schema name.
            table_name: Table name.

        Output:
            config: DeltaTableConfig object.

        Expected:
            1: DeltaTableConfig object is initialized with correct attributes.
    """
    config = DeltaTableConfig(
        s3_bucket="test-bucket",
        catalog_name="test_catalog",
        schema_name="test_schema",
        table_name="test_table",
    )
    assert config.s3_bucket == "test-bucket"
    assert config.catalog_name == "test_catalog"
    assert config.schema_name == "test_schema"
    assert config.table_name == "test_table"
    assert config.date_partition_column is None
    assert config.optimize_compaction is False
    assert config.optimize_zorder_columns == []
    assert config.s3_path_prefix == ""


def test_databricks_table_name_property():
    """
        Test datab databricks_table_name property.

        Input:
            config: DeltaTableConfig object.

        Output:
            databricks_table_name: Databricks table name.

        Expected:
            1: databatabricks_table_name is correct.
    """
    config = DeltaTableConfig(
        s3_bucket="test-bucket",
        catalog_name="test_catalog",
        schema_name="test_schema",
        table_name="test_table",
    )
    assert config.databricks_table_name == "test_catalog.test_schema.test_table"


def test_delta_table_s3_path_property():
    """
        Test delta_table_s3_path property.

        Input:
            config: DeltaTableConfig object.

        Output:
            delta_table_s3_path: Delta table S3 path.

        Expected:
            1: delta_table_s3_path is correct.
    """
    config = DeltaTableConfig(
        s3_bucket="test-bucket",
        catalog_name="test_catalog",
        schema_name="test_schema",
        table_name="test_table",
    )
    expected_path = "s3://test-bucket/test_catalog/test_schema/test_table"
    assert config.delta_table_s3_path == expected_path


def test_delta_table_s3_path_property_with_prefix():
    """
        Test delta_table_s3_path property with prefix.

        Input:
            config: DeltaTableConfig object.

        Output:
            delta_table_s3_path: Delta table S3 path with prefix.

        Expected:
            1: delta_table_s3_path is correct with prefix.
    """
    config = DeltaTableConfig(
        s3_bucket="test-bucket",
        catalog_name="test_catalog",
        schema_name="test_schema",
        table_name="test_table",
        s3_path_prefix="my_prefix",
    )
    expected_path = "s3://test-bucket/my_prefix/test_catalog/test_schema/test_table"
    assert config.delta_table_s3_path == expected_path
