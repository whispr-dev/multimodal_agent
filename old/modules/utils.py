import yaml

def load_identity_profile(path="config/identity.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
