# Configlib Parser

The `configlib` library provides a standardized way to define, load, and parse configurations for various elements within the data pipeline. It leverages YAML for configuration files, Jinja2 for templating, and Python dataclasses for schema definition and validation.

## Configuration File Structure

Configuration files are written in YAML and must adhere to a specific structure. Each configuration file must contain a `kind` field and a `spec` field.

-   `kind`: A string that identifies the type of the configuration. This value is used to map the configuration to the appropriate Python dataclass for parsing.
-   `spec`: A dictionary containing the actual configuration parameters for the element. The structure of the `spec` dictionary must match the fields defined in the corresponding dataclass.

### Example

```yaml
kind: ExampleConfig
spec:
  example_param: "value1"
  example_param2: "value2"
  example_param3: "value3"
```

## Parsing Mechanism

The parsing process is handled by the `load_and_parse_config` function in `spark.configlib.config_loader` and involves the following steps:

1.  **Load File**: The YAML configuration file is loaded from the specified path into a string.
2.  **Render Jinja2 Templates**: The loaded string is treated as a Jinja2 template. This allows for dynamic values in the configuration. The rendering context includes:
    *   `timedelta`: For time calculations.
    *   `str`: For string conversions.
    *   `datetime`: For date and time objects.
3.  **Parse YAML**: The rendered string is parsed into a Python dictionary using `yaml.safe_load`.
4.  **Map to Dataclass**: The `kind` value from the dictionary is used to look up the corresponding dataclass in the `CONFIG_PARSER_MAP`.
5.  **Deserialize to Object**: The `spec` dictionary is deserialized into an instance of the matched dataclass using the `dacite` library. This step also validates that the `spec` dictionary conforms to the dataclass definition.

## How to Add a New Configuration Type

To support a new type of configuration, you need to:

1.  **Define a Dataclass**: Create a new Python dataclass that defines the schema for your configuration. This dataclass should be placed in the `spark.configlib.parser` directory.

    ```python
    # spark/configlib/parser/my_new_config.py
    from dataclasses import dataclass

    @dataclass
    class MyNewConfig:
        param1: str
        param2: int
    ```

2.  **Update `CONFIG_PARSER_MAP`**: Add your new dataclass to the `CONFIG_PARSER_MAP` in `spark/configlib/config_loader.py`.

    ```python
    # spark/configlib/config_loader.py
    from spark.configlib.parser.delta import DeltaTableConfig
    from spark.configlib.parser.example import ExampleConfig
    from spark.configlib.parser.my_new_config import MyNewConfig # Import new config

    CONFIG_PARSER_MAP = {
        DeltaTableConfig.__name__: DeltaTableConfig,
        ExampleConfig.__name__: ExampleConfig,
        MyNewConfig.__name__: MyNewConfig, # Add new config to map
    }
    ```

## Jinja2 Template Support

The configuration parser supports Jinja2 templating, which allows for more dynamic and reusable configurations. You can use Jinja2 expressions within your YAML files.

### Example with Jinja2

```yaml
kind: ExampleConfig
spec:
  example_param: "{{ str(1 + 1) }}" # This will be rendered as "2"
  example_param2: "b"
  example_param3: "c"
```

When `load_and_parse_config` is called with this file, the `example_param` will have the value `"2"` in the final parsed `ExampleConfig` object.
