import os

current_directory = os.getcwd()
config_path = os.path.join(current_directory, 'CompanyConfig')

if os.path.exists(config_path) and os.path.isdir(config_path):
    print(f"The config directory exists at: {config_path}")
else:
    print("The config directory does not exist in the current working directory.")

