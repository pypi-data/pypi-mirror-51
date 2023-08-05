![coolours-logo](https://github.com/Handmade-Studios/coolours-module/blob/master/coolours_logo.png?raw=true)

# **Coolours**
### A Python Module To Make Text Styling Easy
#### _Made By Alex Hawking_

# Installation

> ## With Pip

Install with:

    pip install coolours

or

    pip3 install coolours

> ## With wget

_Wget must be installed_

    cd ~/Library/Python/3.7/lib/python/site-packages && wget https://raw.githubusercontent.com/Handmade-Studios/coolours-module/master/coolours/coolours.py && cd ~

Probably easier to copy and paste that ^


# Usage

> ## Importing

Import coolours using:

    from coolours.colour import *

You can import with

    import coolours.colour

But that requires you to use `print(coolours.colour('style', 'textcolour', 'backgroundcolour'))`, so I think it is easier to use the first method.

> ## Colours

You use coolours within the `print` function as shown below:

    print(colour('style', 'text-colour', 'background-colour') + 'your text')

**Make sure you place the colours and styles within quotes**

> ## Alignment

- ## Center

To center text use:

    print(center('yourtext'))

- ## Right

To align text to the right use:

    print(right('yourtext'))

- ## With Colour

To use alignment with colour:

    print(colour('style', 'textcolour', 'bgcolour') + center('yourtext'))

> ## Default

To make the colours back to default after the coloured text add `default` to the end of the print function:

    print(colour('style', 'text-colour', 'background-colour') + 'your text' + default)

> ## Updating

To update use:

    pip install --upgrade coolours

# List of Colours

### Coolors contains the following colours:

> ## Styles

- none
- bold
- underline (not supported in all temrinals)
- blink (not supported in all terminals)



> ## Text Colours

- none
- black
- red
- green
- yellow
- blue
- purple
- cyan
- white
- brightblack
- brightred
- brightgreen
- brightyellow
- brightblue
- brightpurple
- brightcyan
- brightwhite

> ## Background Colours

- none
- black
- red
- green
- yellow
- blue
- purple
- cyan
- white
- brightblack
- brightred
- brightgreen
- brightyellow
- brightblue
- brightpurple
- brightcyan
- brightwhite


# Future

More colours and styles coming soon. Will add some sort of fancy text.

