import os
import pandas as pd

pd.set_option('display.max_rows', None)

# Get absolute path of TambayTracker2.0 root, regardless of cwd
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Log Filepaths
cmdlog_path         = os.path.join(base_dir, "logs", "cmdlogs.csv")
note_path           = os.path.join(base_dir, "logs", "notes.csv")

# Data paths

# Text Filepaths

home_filepath           = os.path.join(base_dir, "textfiles", "home.txt")
help_filepath           = os.path.join(base_dir, "textfiles", "help.txt")
temp_output_filepath    = os.path.join(base_dir, "textfiles", "temp_output.txt")

# FUNCTIONS TO LOAD DATAFRAMES (ALWAYS UPDATED)
def load_raw_data():
    pass
    #return pd.read_csv(raw_data_filepath)
def text_reader(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing file: {filepath}")
    with open(filepath, "r") as file:
        return file.read()
    
home_file           = text_reader(home_filepath)
help_file           = text_reader(help_filepath)
temp_output_file    = text_reader(temp_output_filepath)

