from modules import utils

import pandas as pd

pd.set_option('display.max_rows', None)

# File paths
raw_data_filepath = r'TambayTracker2.0\data\raw_data.csv'
date_filepath     = r'TambayTracker2.0\data\date_list.csv'
score_filepath    = r'TambayTracker2.0\data\score_data.csv'
member_filepath   = r'TambayTracker2.0\data\member_list.csv'

# Text files
home_filepath           = r'TambayTracker2.0\textfiles\homepage.txt'
help_filepath           = r'TambayTracker2.0\textfiles\help_general.txt'
help_add_filepath       = r'TambayTracker2.0\textfiles\help_add.txt'
help_list_filepath      = r'TambayTracker2.0\textfiles\help_list.txt'
help_show_filepath      = r'TambayTracker2.0\textfiles\help_show.txt'
help_update_filepath    = r'TambayTracker2.0\textfiles\help_update.txt'
help_rm_filepath        = r'TambayTracker2.0\textfiles\help_remove.txt'
help_color_filepath     = r'TambayTracker2.0\textfiles\help_color.txt'

# Text readers
home_file           = utils.text_reader(home_filepath)
help_file           = utils.text_reader(help_filepath)
help_add_file       = utils.text_reader(help_add_filepath)
help_list_file      = utils.text_reader(help_list_filepath)
help_show_file      = utils.text_reader(help_show_filepath)
help_update_file    = utils.text_reader(help_update_filepath)
help_rm_file        = utils.text_reader(help_rm_filepath)
help_color_file     = utils.text_reader(help_color_filepath)


# ✅ FUNCTIONS TO LOAD DATAFRAMES (ALWAYS UPDATED)
def load_raw_data():
    return pd.read_csv(raw_data_filepath)
def load_date_data():
    return pd.read_csv(date_filepath)
def load_score_data():
    return pd.read_csv(score_filepath)
def load_member_data():
    return pd.read_csv(member_filepath)
