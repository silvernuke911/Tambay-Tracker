from modules import utils
from modules import validators
from modules import filepaths
from modules import lister
from modules import adder
from modules import shower
from modules import updaters
from modules import noter
from modules import valid_flags
import subprocess

def quick_exit():
    updaters.update_all(silent=True)
    exit()

def p_add(noun, flags):
    if not validators.validate_flags(flags, valid_flags.f_add, noun):
        return
    match noun:
        cMobChart1ase None:
            print(f"Command 'add' cannot have empty argument. Here are some available commands")
            print(filepaths.help_add_file)
        case 'help':
            print(filepaths.help_add_file)
        case 'entry' | 'new entry' | 'e':
            adder.add_entry()
        case 'member'| 'new member':
            adder.add_member()
        case 'special points' | 'special':
            adder.add_special_points()
        case 'note' | 'n':
            noter.note_add(flags)
        case _:
            print(f"'{noun}' is not a recognized noun for 'add'")

def p_list(noun, flags):
    if not validators.validate_flags(flags, valid_flags.f_list, noun):
        return
    match noun:
        case None:
            print(f"Command 'list' cannot have empty argument. Here are some available commands")
            print(filepaths.help_list_file)
        case 'help':
            print(filepaths.help_list_file)
        case 'members' | 'member':
            lister.list_members(flags)
        case 'raw points' | 'raw data' | 'raw':
            lister.list_raw_data(flags)
        case 'date frequency' | 'af' | 'df':
            lister.list_date_frequency(flags)
        case 'attendance proportion' | 'ap':
            lister.list_attendance_proportion(flags)
        case 'points' | 'point' |'p':
            if not flags:  # Empty dictionary or None
                lister.list_points()
            elif flags.get('order'):
                lister.list_point_order()
            elif flags.get('name'):
                lister.list_point_names()
        case 'individual attendance':
            lister.list_individual_attendance(flags)
        case _:
            print(f"'{noun}' is not a recognized noun for 'list'")

def p_show(noun, flags):
    if not validators.validate_flags(flags, valid_flags.f_show, noun):
        return
    match noun:
        case None:
            print(f"Command 'show' cannot have empty argument. Here are some available commands")
            print(filepaths.help_show_file)
        case 'help':
            print(filepaths.help_show_file)
        case 'point order' | 'points' | 'p':
            shower.show_point_order(flags)
        case 'attendance frequency' | 'af' | 'df' | 'date frequency':
            shower.show_attendance_frequency(flags)
        case 'attendance proportion' | 'ap':
            shower.show_attendance_proportion(flags)
        case 'individual attendance' | 'ia':
            shower.show_individual_attendance(flags)
        case _:
            print(f"'{noun}' is not a recognized noun for 'show'")

def p_update(noun, flags):
    if not validators.validate_flags(flags, valid_flags.f_update, noun):
        return
    match noun:
        case None:
            print(f"Command 'update' cannot have empty argument. Here are some available commands")
            print(filepaths.help_update_file)
        case 'help':
            print(filepaths.help_update_file)
        case 'all' | 'a':
            print(utils.sepline(65))
            updaters.update_all()
            print(utils.sepline(20))
            print('All systems updated')
            print(utils.sepline(65))
        case 'scores' | 's':
            updaters.update_scores()
        case 'date frequency'| 'df':
            updaters.update_date_frequency()
        case _:
            print(f"'{noun}' is not a recognized noun for 'update'")

def p_git(noun, flags):
    match noun:
        case None:
            print("Missing git command. Available: add, commit, push, status, all")
        case 'status':
            subprocess.run(["git", "status"])
            utils.set_color('g')
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
            print(utils.sepline(65))
            print("Executing: git push")
            subprocess.run(["git", "push"])
            print(utils.sepline(65))
            print("Succesfully pushed to remote repository") 
            print(utils.sepline(65))
        case 'pull':
            print(utils.sepline(65))
            print("Executing: git pull")
            subprocess.run(["git", "pull"])
            print(utils.sepline(65))
            print("Succesfully pulled remote repository") 
            print(utils.sepline(65))
        case "all":
            message = flags.get("m", None)  # Get the commit message
            print(utils.sepline(65))
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
            print(utils.sepline(65))
            print("Succesfully pushed to remote repository") 
            print(utils.sepline(65))
            utils.set_color('g')
        case _:
            print(f"Unknown git command: {noun}")

def p_color(noun, flags):
    if not validators.validate_flags(flags, valid_flags.f_color, noun):
        return
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
                
def p_remove(noun, flags):
    if not validators.validate_flags(flags, valid_flags.f_remove, noun):
        return
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

def p_exit():
    tries = 5
    count = 0
    print('Confirm exit? [Y/N]')
    while count < tries:
        prompt = input("> ").lower().strip()
        if prompt in ['y','.']:
            print('Updating all systems')
            print(utils.sepline(65))
            updaters.update_all()
            print(utils.sepline(65,char = '='))
            print('Exiting...')
            print(utils.sepline(65,char = '='))
            exit()
        elif prompt == 'n':
            return
        else:
            print('Please enter a valid answer')
            count += 1
    print('Maximum tries exceeded. Returning to main program.')
    return


def p_home(noun, flags):
    if not validators.validate_flags(flags, valid_flags.f_home, noun):
        return
    print('Returning to home...')
    print('\033c', end='')
    utils.set_color('g')
    print(filepaths.home_file)
    return

def p_help(noun, flags):
    if not validators.validate_flags(flags, valid_flags.f_help, noun):
        return
    help_files = {
                None    : filepaths.help_file,
                'add'   : filepaths.help_add_file,      'a'  : filepaths.help_add_file,
                'list'  : filepaths.help_list_file,     'l'  : filepaths.help_list_file,
                'show'  : filepaths.help_show_file,     's'  : filepaths.help_show_file,
                'update': filepaths.help_update_file,   'ud' : filepaths.help_update_file,
                'remove': filepaths.help_rm_file,       'rm' : filepaths.help_rm_file,
                'color' : filepaths.help_color_file,    'clr': filepaths.help_color_file,
                'note'  : filepaths.help_note_file
            }
    nosubcommand_nouns = {'exit', 'e', '.' 'home', 'cls', 'quit', 'qt', 'hm', 'clearscreen', 'help'}
    match noun:
        case _ if noun in nosubcommand_nouns:
            print(f"Command '{noun}' does not have subcommands.\nType 'help' for general command purpose.")
        case _:
            print(help_files.get(noun, f"Command '{noun}' is not a valid command"))
    return
            
def p_quit(noun, flags):
    print('Quitting entry and returning to home...')
    return

def p_clearscreen(noun, flags):
    if not validators.validate_flags(flags, valid_flags.f_cls, noun):
        return
    print('\033c', end='')  
    utils.set_color('g')
    return

def p_none():
    return 

def p_rest(verb, noun, flags):
    print(f"Command '{verb}' is not a valid command. Please type 'help' for more information.")
    return 

def p_note(noun, flags):
    if not validators.validate_flags(flags, valid_flags.f_note, noun):
        return
    match noun:
        case None:
            print(f"Command 'note' cannot have empty argument. Here are some available commands")
            print(filepaths.help_note_file)
        case 'help' | 'h':
            print(filepaths.help_note_file)
        case 'add'  | 'a':
            noter.note_add(flags)
        case 'read' | 'r':
            noter.note_read(flags)
        case _:
            print(f"'{noun}' is not a recognized noun for 'note'")
    return


