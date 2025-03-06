from modules import utils
from modules import filepaths
from modules import process

def main():
    print('\033c', end='')
    utils.set_color('bg')
    print(filepaths.home_file)
    while True:
        command = utils.prompt()
        verb, noun, flags = utils.parse_command(command)
        # utils.input_analyzer(verb, noun, flags)
        process.execute_command(verb, noun, flags)
if __name__ == "__main__":
    main()