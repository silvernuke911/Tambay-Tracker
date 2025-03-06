from modules import utils
from modules import filepaths
from modules import process

        # utils.input_analyzer(verb, noun, flags)

def main():
    print('\033c', end='')
    utils.set_color('g')
    print(filepaths.home_file)
    while True:
        command = utils.prompt()
        verb, noun, flags = utils.parse_command(command)
        process.execute_command(verb, noun, flags)
        
if __name__ == "__main__":
    main()