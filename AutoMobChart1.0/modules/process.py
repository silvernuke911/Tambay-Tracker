from modules import utilities
from modules import filepaths
from modules import notes 
from modules import validators
from modules import updater
from modules import valid_flags

import subprocess 
import os

def quick_exit():
    exit()

def p_none():
    return

def p_exit():
    tries = 5
    count = 0
    print('Confirm exit? [Y/N]')
    while count < tries:
        prompt = utilities.prompt(address=False)
        if prompt in ['y','.']:
            # updaters.update_all()
            print(utilities.sepline("="))
            print('Exiting...')
            print(utilities.sepline("="))
            exit()
        elif prompt == 'n':
            return
        else:
            print('Please enter a valid answer')
            count += 1
    print('Maximum tries exceeded. Returning to main program.')
    return

def p_note(noun, flags):
    # if not validators.validate_flags(flags, valid_flags.f_note, noun):
    #     return
    match noun:
        case None:
            print(f"Command 'note' cannot have empty argument. Here are some available commands")
            print(filepaths.help_note_file)
        case 'help' | 'h':
            print(filepaths.help_note_file)
        case 'add'  | 'a':
            notes.note_add(flags)
        case 'read' | 'r':
            notes.note_read(flags)
    return

def p_help(noun, flags):
    utilities.temporary_output()

def p_home(noun, flags):
    utilities.temporary_output()

def p_quit(noun, flags):
    utilities.temporary_output()

def p_clearscreen(noun, flags):
    print('\033c', end='')  
    utilities.set_color('g')
    return

def p_rest(verb, noun, flags):
    print(f"Command '{verb}' is not a valid command. Please type 'help' for more information.")
    return 

def p_update(noun, flags):
    utilities.temporary_output()

def p_git(noun, flags):
    match noun:
        case None:
            print("Missing git command. Available: add, commit, push, status, all")
        case 'status':
            subprocess.run(["git", "status"])
            utilities.set_color('g')
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
            print(utilities.sepline())
            print("Executing: git push")
            subprocess.run(["git", "push"])
            print(utilities.sepline())
            print("Succesfully pushed to remote repository") 
            print(utilities.sepline())
        case 'pull':
            print(utilities.sepline())
            print("Executing: git pull")
            subprocess.run(["git", "pull"])
            print(utilities.sepline())
            print("Succesfully pulled remote repository") 
            print(utilities.sepline())
        case "all":
            message = flags.get("m", None)  # Get the commit message
            print(utilities.sepline())
            print("Executing: git add .")
            subprocess.run(["git", "add", "."])
            print(f"Executing: git commit -m '{message}'")
            if message:
                subprocess.run(["git", "commit", "-m", message])
            else:
                print("Error: Commit message required. Use --m 'message'")
                return
            print("Executing: git push")
            subprocess.run(["git", "push"])
            print(utilities.sepline())
            print("Succesfully pushed to remote repository") 
            print(utilities.sepline())
            utilities.set_color('g')
        case _:
            print(f"Unknown git command: {noun}")

def p_home(noun, flags):
    if not validators.validate_flags(flags, valid_flags.f_home, noun):
        return
    print('Returning to home...')
    print('\033c', end='')
    utilities.set_color('g')
    print(filepaths.home_file)
    return

def p_system(noun, flags):
    print(utilities.sepline())
    print("Enter valid security code")
    print(utilities.sepline())
    code = utilities.prompt(address=False)
    
    if code in utilities.valid_credentials:
        print(utilities.sepline())
        print("Entering system shell... (type 'exit' to return)")
        shell = os.environ.get("COMSPEC") if os.name == "nt" else os.environ.get("SHELL", "/bin/bash")
        try:
            subprocess.run(shell, check=True)
            utilities.set_color('g')
            print("Returned from system shell")
            print(utilities.sepline())
            
        except subprocess.CalledProcessError as e:
            print(f"Shell exited with error: {e}")
        except Exception as e:
            print(f"Error launching system shell: {e}")
    else: 
        print("Security code invalid, returning to home")
        return