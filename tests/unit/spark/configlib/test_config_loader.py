import pytest

from spark.configlib.config_loader import (
    load_and_parse_config,
    load_yaml_config_from_path_as_str,
    parse_config,
)
from spark.configlib.parser.example import ExampleConfig


def test_load_yaml_config_from_path_as_str_reads_file(config_factory):
    """
        Test loading config file from path as string.

        Input:
            config_path: Path to config file.
        Output:
            content: Content of config file as string.

        Expected:
            1: Load successfully and content is not None
            2: Content contains ExampleConfig kind
            3: Content contains ExampleConfig spec
        """
    config_path = config_factory(
        kind="ExampleConfig",
        spec={"example_param": "a", "example_param2": "b", "example_param3": "c"},
    )
    content = load_yaml_config_from_path_as_str(str(config_path))
    assert content is not None
    assert "kind: ExampleConfig" in content
    assert "example_param: a" in content
    assert "example_param2: b" in content
    assert "example_param3: c" in content


def test_parse_config_with_example_kind(config_dict):
    """
        Test parsing ExampleConfig.

        Input:
            config_dict: Config dictionary.

        Output:
            parsed: Parsed ExampleConfig.

        Expected:
            1: Parsed ExampleConfig successfully return ExampleConfig object.
            2: Parsed ExampleConfig has correct attributes.

    """
    parsed = parse_config(config_dict)

    assert isinstance(parsed, ExampleConfig)
    assert parsed.example_param == "a"
    assert parsed.example_param2 == "b"
    assert parsed.example_param3 == "c"


def test_parse_config_without_kind(config_dict_without_kind):
    """
        Test parsing ExampleConfig.

        Input:
            config_dict: Config dictionary without kind.

        Output:
            parsed: parse failed

        Expected:
            1: Raises ValueError with message " ValueError: Config kind is required."
    """
    with pytest.raises(ValueError):
        parse_config(config_dict_without_kind)

        
def test_parse_config_unknown_kind(config_dict_with_unknown_kind):
    """
        Test parsing ExampleConfig.

        Input:
            config_dict: Config dictionary with unknown kind.

        Output:
            parsed: parse failed

        Expected:
            1: Raises ValueError with message " ValueError: Unknown config kind: UnknownConfig."
    """
    with pytest.raises(ValueError):
        parse_config(config_dict_with_unknown_kind)


def test_load_yaml_config_from_path_as_str_missing_file(tmp_path):
    """
        Test loading config file from path as string when file is missing.

        Input:
            config_path: Path to config file.
        Output:
            content: Content of config file as string.

        Expected:
            1: Raises FileNotFoundError with message " Config file not found: /missing.yaml"
    """
    with pytest.raises(FileNotFoundError):
        load_yaml_config_from_path_as_str(str(tmp_path / "missing.yaml"))


def test_load_and_parse_config_renders_jinja(config_factory):
    """
        Test loading and parsing config file from path as string when jinja template is used.

        Input:
            config_path: Path to config file.
        Output:
            parsed: Parsed ExampleConfig.

        Expected:
            1: Parsed ExampleConfig successfully return ExampleConfig object.
            2: Parsed ExampleConfig has correct attributes.
    """
    config_path = config_factory({"example_param": "{{ str(1 + 1) }}", "example_param2": "b", "example_param3": "c"})
    parsed = load_and_parse_config(str(config_path))

    assert isinstance(parsed, ExampleConfig) #parse successfully
    assert parsed.example_param == "2" #jinja tempalte render successfully
