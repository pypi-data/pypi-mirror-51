# designed by alex hawking

# usage: print(colour(style, textground colour, background colour) + 'your text')


def colour(style, text, bg):

    a = "\033[0;"
    b = "39;"
    c = "49m"

    # styles
    if style == "none":
        a = "\033[0;"
    if style == "bold":
        a = "\033[1;"
    if style == "underline":
        a = "\033[2;"
    if style == "blink":
        a = "\033[5;"

    # standard colours

    # text
    if text == "none":
        b = "39;"
    if text == "black":
        b = "30;"
    if text == "red":
        b = "31;"
    if text == "green":
        b = "32;"
    if text == "yellow":
        b = "33;"
    if text == "blue":
        b = "34;"
    if text == "purple":
        b = "35;"
    if text == "cyan":
        b = "36;"
    if text == "white":
        b = "37;"

    # background
    if bg == "none":
        c = "48m"
    if bg == "black":
        c = "40m"
    if bg == "red":
        c = "41m"
    if bg == "green":
        c = "42m"
    if bg == "yellow":
        c = "43m"
    if bg == "blue":
        c = "44m"
    if bg == "purple":
        c = "45m"
    if bg == "cyan":
        c = "46m"
    if bg == "white":
        c = "47m"

    # bright colours

    if text == "brightblack":
        b = "90;"
    if text == "brightred":
        b = "91;"
    if text == "brightgreen":
        b = "92;"
    if text == "brightyellow":
        b = "93;"
    if text == "brightblue":
        b = "94;"
    if text == "brightpurple":
        b = "95;"
    if text == "brightcyan":
        b = "96;"
    if text == "brightwhite":
        b = "97;"

    # background

    if bg == "brightblack":
        c = "100m"
    if bg == "brightred":
        c = "41m"
    if bg == "brightgreen":
        c = "42m"
    if bg == "brightyellow":
        c = "43m"
    if bg == "brightblue":
        c = "44m"
    if bg == "brightpurple":
        c = "45m"
    if bg == "brightcyan":
        c = "46m"
    if bg == "brightwhite":
        c = "47m"

    # finish
    return(a + b + c)


default = "\033[0;39;49m"
