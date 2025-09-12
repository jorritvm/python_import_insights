import os
import yaml

if __name__ == "__main__":
    file_path = os.path.join("config","parameters.yaml")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            config = yaml.safe_load(file)
        print(config)
    else:
        print(f"File {file_path} does not exist.")