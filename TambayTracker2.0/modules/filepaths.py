from modules import utils

import pandas as pd

pd.set_option('display.max_rows', None)

# Data files
raw_data_filepath = r'C:\Users\verci\Documents\Python Code\Tambay-Tracker\TambayTracker2.0\data\raw_data.csv'
date_filepath     = r'C:\Users\verci\Documents\Python Code\Tambay-Tracker\TambayTracker2.0\data\date_list.csv'
score_filepath    = r'C:\Users\verci\Documents\Python Code\Tambay-Tracker\TambayTracker2.0\data\score_data.csv'
member_filepath   = r'C:\Users\verci\Documents\Python Code\Tambay-Tracker\TambayTracker2.0\data\member_list.csv'

raw_data_file   = pd.read_csv(raw_data_filepath, sep = ':')
date_file       = pd.read_csv(date_filepath)
score_file      = pd.read_csv(score_filepath)
member_file     = pd.read_csv(member_filepath)

# Text files
home_filepath           = r'C:\Users\verci\Documents\Python Code\Tambay-Tracker\TambayTracker2.0\textfiles\homepage.txt'
help_filepath           = r'C:\Users\verci\Documents\Python Code\Tambay-Tracker\TambayTracker2.0\textfiles\help_general.txt'
help_add_filepath       = r'C:\Users\verci\Documents\Python Code\Tambay-Tracker\TambayTracker2.0\textfiles\help_add.txt'
help_list_filepath      = r'C:\Users\verci\Documents\Python Code\Tambay-Tracker\TambayTracker2.0\textfiles\help_list.txt'
help_show_filepath      = r'C:\Users\verci\Documents\Python Code\Tambay-Tracker\TambayTracker2.0\textfiles\help_show.txt'
help_update_filepath    = r'C:\Users\verci\Documents\Python Code\Tambay-Tracker\TambayTracker2.0\textfiles\help_update.txt'
help_rm_filepath        = r'C:\Users\verci\Documents\Python Code\Tambay-Tracker\TambayTracker2.0\textfiles\help_remove.txt'

home_file           = utils.text_reader(home_filepath)
help_file           = utils.text_reader(help_filepath)
help_add_file       = utils.text_reader(help_add_filepath)
help_list_file      = utils.text_reader(help_list_filepath)
help_show_file      = utils.text_reader(help_show_filepath)
help_update_file    = utils.text_reader(help_update_filepath)
help_rm_file        = utils.text_reader(help_rm_filepath)
