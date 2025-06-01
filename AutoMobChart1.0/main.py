from modules import utilities
from modules import filepaths
from modules import execute

def main():
    
    print('\033c', end='')
    utilities.set_color('g')
    print(filepaths.home_file)
    while True:
        command = utilities.prompt()
        verb, noun, flags = utilities.parse_command(command)
        # utils.input_analyzer(verb, noun, flags)
        execute.execute_command(verb, noun, flags)
        
if __name__ == "__main__":
    main()