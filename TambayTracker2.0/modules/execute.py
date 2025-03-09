from modules import process

def execute_command(verb, noun, flags):
    match verb:
        case '..'|',,': # edit this out later, this is for quick exits only
            exit()
        case None:
            process.p_none()
        case 'exit' | 'e' | '.':
            process.p_exit()
        case 'help' | 'h':
            process.p_help(noun, flags)
        case 'add'|'a':
            process.p_add(noun, flags)
        case 'list'|'l':
            process.p_list(noun, flags)
        case 'show'|'s':
            process.p_show(noun, flags)
        case 'update' | 'ud':
            process.p_update(noun, flags)
        case 'home' | 'hm':
            process.p_home()
        case 'quit' | 'qt':
            process.p_quit(noun, flags)
        case 'clearscreen' | 'cls':
            process.p_clearscreen()
        case 'git':
            process.p_git(noun, flags)
        case 'color'|'clr':
            process.p_color(noun, flags)
        case 'remove' | 'rm':
            process.p_remove(noun, flags)
        case 'note':
            process.p_note(noun, flags)
        case _:
            process.p_rest(verb, noun, flags)
    print()
    return