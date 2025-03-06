from modules import utils
from modules import filepaths

import subprocess

def process_add(noun, flags):
    match noun:
        case None:
            print(f"Command 'add' cannot have empty argument. Here are some available commands")
            print(filepaths.help_add_file)
        case 'help':
            print(filepaths.help_add_file)
        case 'entry':
            utils.temporary_output()
        case 'new member':
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
        case 'raw points':
            utils.temporary_output()
        case 'date frequency':
            utils.temporary_output()
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
            print("Missing git command. Available: add, commit, push")
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
            
def execute_command(verb, noun, flags):
    match verb:
        case None:
            print()
            return 
        case 'exit' | 'e':
            print('Exiting...')
            exit()
        case 'help' | 'h':
            match noun:
                case None:
                    print(filepaths.help_file)
                case 'add' :
                    print(filepaths.help_add_file)
                case 'list':
                    print(filepaths.help_list_file)
                case 'show':
                    print(filepaths.help_show_file)
                case 'update':
                    print(filepaths.help_update_file)
                case _:
                    print(f"Command '{noun}' does not have subcommands.\nType 'help' for general command purpose" )
        case 'add':
            process_add(noun, flags)
        case 'list':
            process_list(noun, flags)
        case 'show':
            process_show(noun, flags)
        case 'update':
            process_update(flags)
        case 'home' | 'hm':
            print('Returning to home...')
            print('\033c', end='')
            utils.set_color('g')
            print(filepaths.home_file)
        case 'quit' | 'qt':
            print('Quitting entry and returning to home...')
        case 'clearscreen' | 'cls':
            print('\033c', end='')  
            utils.set_color('g')
        case 'git':
            process_git(noun, flags)
        case _:
            print(f"Command '{verb}' is not a valid command. Please type 'help' for more information.")
    print()
    return 