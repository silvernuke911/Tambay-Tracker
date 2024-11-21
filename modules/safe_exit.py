from modules import updaters

def safe_exit(raw_data_file, score_file, date_file, valid_names):
    updaters.update_scores(raw_data_file, score_file)
    updaters.update_date_freq(raw_data_file, date_file, valid_names)
    print('Exiting...')
    exit()