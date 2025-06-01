import os
import csv
import shlex 

from datetime import datetime
from modules import filepaths

def clearscreen():
    print('\033c', end='')
    return

def sepline(char = "-", length = 70):
    output = char*length
    return output

def aligntext(text, length=70, align='center'):
    if align not in ('center', 'left', 'right'):
        raise ValueError("Wrong alignment text, accepted: center, left, right")
    if align == 'center':
        output = f"{text:^{length}}"
    elif align == 'left':
        output = f"{text:<{length}}"
    elif align == 'right':
        output = f"{text:>{length}}"
    return output

def bordertext(text, char='-', length=70, align='center'):
    lines = str(text).split('\n')
    print(sepline(char=char, length=length))
    for line in lines:
        print(aligntext(line, length=length, align=align))
    print(sepline(char=char, length=length))

def text_reader(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing file: {filepath}")
    with open(filepath, "r") as file:
        return file.read()

def text_writer(filepath, entry):
    with open(filepath, 'a') as file:
        file.write(entry + '\n')
    print("Entry added successfully.")

def clearline():
    print('\033[F\033[K', end='')

def yes_no_query(prompt, limit=5):
    count = 0
    while count < limit:
        query = input(prompt).strip().lower()
        if query in ['y', ""]:
            clearline()
            print('> Y')
            return True 
        elif query in ['n', '..']:
            return False
        else:
            print(f'{query} is not a valid answer, please enter [Y/N]')
            count += 1
    print('Exceeded invalid answer limit, returning to main program')
    return True 

valid_credentials = ['299792458', 
                     '2718281828', 
                     '3141592654', 
                     '1414213562', 
                     '091103'
                     'Inuke', 
                     'Jieru',
                     "...", 
                     "Fratres!",
                     "Usque@dFinem"
                    ]
quit_list = ['quit', 
             'qt',
             ".."
            ]

# Dictionary mapping color names to ANSI codes
color_codes = {
    # Basic colors
    'black'  : '30',
    'red'    : '31',
    'green'  : '32',
    'yellow' : '33',
    'blue'   : '34',
    'magenta': '35',
    'cyan'   : '36',
    'white'  : '37',
    # Shortcuts
    '0a': '32',
    'g' : '32',
    'r' : '31',
    'b' : '34',
    'bg': '92',
    'c' : '36',
    'm' : '35',
    'y' : '33',
    'k' : '30',
    'w' : '37',
    # Bright colors
    'bright black'  : '90',
    'bright red'    : '91',
    'bright green'  : '92',
    'bright yellow' : '93',
    'bright blue'   : '94',
    'bright magenta': '95',
    'bright cyan'   : '96',
    'bright white'  : '97',
    # Reset
    # 'reset': '0',s
    'reset'         : '32'
}
    
def set_color(color):
    """
    Set the terminal text color using ANSI escape codes.
    
    Parameters:
        color (str): The color name or ANSI code (e.g., 'red', '32', '1;31').
    """
    # Check if the input is a color name or a raw ANSI code
    if color in color_codes:
        ansi_code = color_codes[color]
    else:
        # Assume the input is a raw ANSI code (e.g., '1;31' for bold red)
        ansi_code = color
    # Print the ANSI escape sequence
    print(f"\033[{ansi_code}m", end="")

def log_to_cmdlog(text):
    date = datetime.now().strftime("%m/%d/%Y")
    time = datetime.now().strftime("%I:%M:%S %p")
    cmdlog = filepaths.cmdlog_path
    os.makedirs(os.path.dirname(cmdlog), exist_ok=True)
    try:
        with open(cmdlog, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([date, time, text if text else " "])
    except Exception as e:
        print(f"[LOGGING ERROR] Could not write to cmdlogs: {e}")

def prompt(address=True, address_content=r'UPPSF:\AutoMobChart1.0', lower=True, yes_no=False):
    if address:
        print(address_content)
    if yes_no:
        result = yes_no_query('> ')
        log_to_cmdlog('Y' if result else 'N')
        return result  # Boolean
    user_input = input('> ').strip()
    log_to_cmdlog(user_input)
    if lower:
        user_input = user_input.lower()
    return user_input

def input_analyzer(verb, noun, flags):
    print('verb  : ', verb)
    print('noun  : ', noun)
    print('flags : ', flags)
    
def temporary_output():
    output = filepaths.temp_output_file
    print(output)

def parse_command(command):
    try:
        tokens = shlex.split(command)  # Split but preserve quoted strings
    except Exception as e:  # Catch ANY exception and print it
        print(f"Error: {e}.")
        return None, None, {}
    if not tokens:
        return None, None, {}
    verb = tokens[0]
    noun_parts = []
    flags = {}
    i = 1
    while i < len(tokens):
        if tokens[i].startswith("--"):  # It's a flag
            flag = tokens[i][2:]  # Remove '--'
            value = True  # Default for boolean flags
            if i + 1 < len(tokens) and not tokens[i + 1].startswith("--"):
                value = tokens[i + 1]  # Assign value
                i += 1
            flags[flag] = value
        else:
            noun_parts.append(tokens[i])  # Collect noun parts
        i += 1
    noun = " ".join(noun_parts) if noun_parts else None
    return verb, noun, flags