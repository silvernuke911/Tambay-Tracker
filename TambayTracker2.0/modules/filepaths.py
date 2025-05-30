import os
import pandas as pd

pd.set_option('display.max_rows', None)

# Get absolute path of TambayTracker2.0 root, regardless of cwd
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# File paths
raw_data_filepath   = os.path.join(BASE_DIR, "data", "raw_data.csv")
date_filepath       = os.path.join(BASE_DIR, "data", "date_list.csv")
score_filepath      = os.path.join(BASE_DIR, "data", "score_data.csv")
member_filepath     = os.path.join(BASE_DIR, "data", "member_list.csv")

# Image Save paths
imsave_path         = os.path.join(BASE_DIR, "images")
notefile_path       = os.path.join(BASE_DIR, "notes", "note.csv")

# Command Log save path
cmdlog_path         = os.path.join(BASE_DIR, "cmdlogs", "cmdlogs.csv")

# Text files
home_filepath           = os.path.join(BASE_DIR, "textfiles", "homepage.txt")
help_filepath           = os.path.join(BASE_DIR, "textfiles", "help_general.txt")
help_add_filepath       = os.path.join(BASE_DIR, "textfiles", "help_add.txt")
help_list_filepath      = os.path.join(BASE_DIR, "textfiles", "help_list.txt")
help_show_filepath      = os.path.join(BASE_DIR, "textfiles", "help_show.txt")
help_update_filepath    = os.path.join(BASE_DIR, "textfiles", "help_update.txt")
help_rm_filepath        = os.path.join(BASE_DIR, "textfiles", "help_remove.txt")
help_color_filepath     = os.path.join(BASE_DIR, "textfiles", "help_color.txt")
help_note_filepath      = os.path.join(BASE_DIR, "textfiles", "help_note.txt")
help_sys_filepath       = os.path.join(BASE_DIR, "textfiles", "help_sys.txt")
temp_output_filepath    = os.path.join(BASE_DIR, "textfiles", "temp_output.txt")

shorcut_filepath        = os.path.join(BASE_DIR, "textfiles", "shortcut.txt")

# FUNCTIONS TO LOAD DATAFRAMES (ALWAYS UPDATED)
def load_raw_data():
    return pd.read_csv(raw_data_filepath)
def load_date_data():
    return pd.read_csv(date_filepath)
def load_score_data():
    return pd.read_csv(score_filepath)
def load_member_data():
    return pd.read_csv(member_filepath)
def text_reader(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing file: {filepath}")
    with open(filepath, "r") as file:
        return file.read()

# Text readers
home_file           = text_reader(home_filepath)
help_file           = text_reader(help_filepath)
help_add_file       = text_reader(help_add_filepath)
help_list_file      = text_reader(help_list_filepath)
help_show_file      = text_reader(help_show_filepath)
help_update_file    = text_reader(help_update_filepath)
help_rm_file        = text_reader(help_rm_filepath)
help_color_file     = text_reader(help_color_filepath)
help_note_file      = text_reader(help_note_filepath)
help_sys_file       = text_reader(help_sys_filepath)
temp_output_file    = text_reader(temp_output_filepath)
