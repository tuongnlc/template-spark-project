import pytest
import yaml


@pytest.fixture
def config_dict():
    return {
        "kind": "ExampleConfig",
        "spec": {
            "example_param": "a",
            "example_param2": "b",
            "example_param3": "c",
        }
    }

@pytest.fixture
def config_dict_without_kind():
    return {
        "spec": {
            "example_param": "a",
            "example_param2": "b",
            "example_param3": "c",
        },
}


@pytest.fixture
def config_dict_with_unknown_kind():
    return {
        "kind": "UnknownConfig",
        "spec": {},
    }



@pytest.fixture
def config_factory(tmp_path):
    """
        Create a factory function to temporarily generate config files.
    """
    def _config_factory(spec: dict, kind: str = "ExampleConfig") -> str:
        config = {"kind": kind, "spec": spec}
        config_path = tmp_path / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)
        return str(config_path)

    return _config_factory