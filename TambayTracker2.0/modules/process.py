from modules import utils
from modules import filepaths
from modules import lister
from modules import adder
from modules import shower

import subprocess
import pandas as pd

def process_add(noun, flags):
    match noun:
        case None:
            print(f"Command 'add' cannot have empty argument. Here are some available commands")
            print(filepaths.help_add_file)
        case 'help':
            print(filepaths.help_add_file)
        case 'entry' | 'new entry' | 'e':
            utils.temporary_output()
        case 'member'| 'new member':
            utils.temporary_output()
        case 'special points':
            utils.temporary_output()
        case _:
            print(f"'{noun}' is not a recognized noun for 'add'")

def process_list(noun, flags):
    match noun:
        case None:
            print(f"Command 'list' cannot have empty argument. Here are some available commands")
            print(filepaths.help_list_file)
        case 'help':
            print(filepaths.help_list_file)
        case 'raw points' | 'raw data':
            lister.list_raw_data()
        case 'date frequency':
            lister.list_date_frequency()
        case 'attendance proportion':
            utils.temporary_output()
        case 'point order':
            utils.temporary_output()
        case 'individual attendance':
            utils.temporary_output()
        case _:
            print(f"'{noun}' is not a recognized noun for 'list'")

def process_show(noun, flags):
    match noun:
        case None:
            print(f"Command 'show' cannot have empty argument. Here are some available commands")
            print(filepaths.help_show_file)
        case 'help':
            print(filepaths.help_show_file)
        case 'point order':
            utils.temporary_output()
        case 'attendance frequency':
            utils.temporary_output()
        case 'attendance proportion':
            utils.temporary_output()
        case 'individual attendance':
            utils.temporary_output()
        case _:
            print(f"'{noun}' is not a recognized noun for 'show'")

def process_update(noun, flags):
    match noun:
        case None:
            print(f"Command 'update' cannot have empty argument. Here are some available commands")
            print(filepaths.help_update_file)
        case 'help':
            print(filepaths.help_update_file)
        case 'scores':
            utils.temporary_output()
        case _:
            print(f"'{noun}' is not a recognized noun for 'update'")

def process_git(noun, flags):
    match noun:
        case None:
            print("Missing git command. Available: add, commit, push, status")
        case 'status':
            subprocess.run(["git", "status"])
        case "add":
            print("Executing: git add .")
            subprocess.run(["git", "add", "."])
        case "commit":
            message = flags.get("m", None)  # Get the commit message
            if message:
                print(f'Executing: git commit -m "{message}"')
                subprocess.run(["git", "commit", "-m", message])
            else:
                print("Error: Commit message required. Use -m 'message'")
        case "push":
            print("Executing: git push")
            subprocess.run(["git", "push"])
        case _:
            print(f"Unknown git command: {noun}")

def process_color(noun, flags):
    match noun:
        case None:
            print("No color specified. Available commands are:")
            print(filepaths.help_color_file)
        case 'help':
            print(filepaths.help_color_file)
        case _:
            if noun in utils.color_codes:
                utils.set_color(noun)
            else:
                print(f"'{noun}' is not a recognized color.")
                print("Available colors are:")
                print(filepaths.help_color_file)
                
def process_remove(noun, flags):
    match noun:
        case None:
            print(f"Command 'remove' cannot have empty argument. Here are some available commands")
            print(filepaths.help_rm_file)
        case 'help':
            print(filepaths.help_rm_file)
        case 'new member':
            utils.temporary_output()
        case 'special points':
            utils.temporary_output()
        case _:
            print(f"'{noun}' is not a recognized noun for 'remove'")

def process_exit():
    tries = 5
    count = 0
    
    print('Confirm exit? [Y/N]')
    while count < tries:
        prompt = input("> ").lower().strip()
        if prompt in ['y','.']:
            print('Exiting...')
            exit()
        elif prompt == 'n':
            return
        else:
            print('Please enter a valid answer')
            count += 1
    print('Maximum tries exceeded. Returning to main program.')

def process_note(noun, flags):
    ## enters a note in a text file written in a different folder
    ## nouns : help, entry, read
    pass 

def process_help(noun, flags):
    help_files = {
                None    : filepaths.help_file,
                'add'   : filepaths.help_add_file,      'a'  : filepaths.help_add_file,
                'list'  : filepaths.help_list_file,     'l'  : filepaths.help_list_file,
                'show'  : filepaths.help_show_file,     's'  : filepaths.help_show_file,
                'update': filepaths.help_update_file,   'ud' : filepaths.help_update_file,
                'remove': filepaths.help_rm_file,       'rm' : filepaths.help_rm_file,
                'color' : filepaths.help_color_file,    'clr': filepaths.help_color_file
            }
    nosubcommand_nouns = {'exit', 'e', '.' 'home', 'cls', 'quit', 'qt', 'hm', 'clearscreen'}
    match noun:
        case _ if noun in nosubcommand_nouns:
            print(f"Command '{noun}' does not have subcommands.\nType 'help' for general command purpose")
        case _:
            print(help_files.get(noun, f"Command '{noun}' is not a valid command"))
            
def execute_command(verb, noun, flags):
    match verb:
        case None:
            print()
            return 
        case 'exit' | 'e' | '.':
            process_exit()
        case '..'|',,': # edit this out later, this is for quick exits only
            exit()
        case 'help' | 'h':
            process_help(noun, flags)
        case 'add'|'a':
            process_add(noun, flags)
        case 'list'|'l':
            process_list(noun, flags)
        case 'show'|'s':
            process_show(noun, flags)
        case 'update' | 'ud':
            process_update(noun, flags)
        case 'home' | 'hm':
            print('Returning to home...')
            print('\033c', end='')
            utils.set_color('g')
            print(filepaths.home_file)
            return
        case 'quit' | 'qt':
            print('Quitting entry and returning to home...')
            return
        case 'clearscreen' | 'cls':
            print('\033c', end='')  
            utils.set_color('g')
            return
        case 'git':
            process_git(noun, flags)
        case 'color'|'clr':
            process_color(noun, flags)
        case 'remove' | 'rm':
            process_remove(noun, flags)
        case 'note':
            process_note(noun, flags)
        case _:
            print(f"Command '{verb}' is not a valid command. Please type 'help' for more information.")
    print()
    return