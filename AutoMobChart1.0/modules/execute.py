from modules import process

def execute_command(verb, noun, flags):
    match verb:
        case '..'|',,': # edit this out later, this is for quick exits only
            process.quick_exit()
        case None | '':
            process.p_none()
        case 'exit' | 'e' | '.':
            process.p_exit()
        case 'help' | 'h':
            process.p_help(noun, flags)
        case 'home' | 'hm':
            process.p_home(noun, flags)
        case 'quit' | 'qt':
            process.p_quit(noun, flags)
        case 'clearscreen' | 'cls':
            process.p_clearscreen(noun, flags)
        case 'git':
            process.p_git(noun, flags)
        case 'color'|'clr':
            process.p_color(noun, flags)
        case 'note' | 'nt' | 'n':
            process.p_note(noun, flags)
        case 'time' | 'date':
            process.p_time(noun, flags)
        case 'sys' | 'system':
            process.p_system(noun, flags)
        case 'cmdlog':
            process.p_list('cmdlog',flags)
        case 'shortcut' | 'sc':
            process.shortcut(noun,flags)
        case _:
            process.p_rest(verb, noun, flags)
    print()
    return

    
