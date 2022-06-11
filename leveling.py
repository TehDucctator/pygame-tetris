def level_up(level, lines_cleared):
    if level <= 9:
        min_lines = 5*(level*level) + 5*(level)
        lines_required = (level+1)*10 + min_lines

    elif level <= 15:
        lines_required = 550 + 100*(level-9)

    elif level <= 25:
        min_lines = 5*(level*level) - 55*(level) + 750
        lines_required = 100+(level - 15)*10 + min_lines
        
    else:
        lines_required = 2700 + 200*(level-25)

    if lines_cleared > lines_required:
        level += 1

    return level

def speed(level):
    if level <= 8:
        return 48 - 5*level
    elif level == 9:
        return 6
    elif level <= 12:
        return 5
    elif level <= 15:
        return 4
    elif level <= 18:
        return 3
    elif level <= 28:
        return 2
    else:
        return 1