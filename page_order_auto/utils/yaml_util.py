import yaml


def read_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        value = yaml.safe_load(f)
        return value

def write_yaml(path, value):
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(value, f)


def clear_yaml(path):
    with open(path, "w", encoding="utf-8") as f:
        f.truncate()