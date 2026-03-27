#load_yaml_config_from_path_as_str
from spark.configlib.config_loader import load_yaml_config_from_path_as_str, load_and_parse_config

# EXAMPLE OF LOADING YAML CONFIG FILE
str_path = '/Users/tuongnguyen/Desktop/template/template-spark-project/configs/spark/test_config.yaml'
test_load_file = load_yaml_config_from_path_as_str(str_path)
print(type(test_load_file)) #RETURN STR

# EXAMPLE load_and_parse_config
str_path = '/Users/tuongnguyen/Desktop/template/template-spark-project/configs/spark/test_config.yaml'
test_load_and_parse_config = load_and_parse_config(str_path)
# print(type(test_load_and_parse_config))
