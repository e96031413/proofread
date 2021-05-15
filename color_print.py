'''
#### add some colors to the output
example:
    print(color_blue("+++++++++*********************************************"))
'''

color_black = lambda text: '\033[0;30m' + text + '\033[0m'
color_red = lambda text: '\033[0;31m' + text + '\033[0m'
color_green = lambda text: '\033[0;32m' + text + '\033[0m'
color_yellow = lambda text: '\033[0;33m' + text + '\033[0m'
color_blue = lambda text: '\033[0;34m' + text + '\033[0m'
color_magenta = lambda text: '\033[0;35m' + text + '\033[0m'
color_cyan = lambda text: '\033[0;36m' + text + '\033[0m'
color_white = lambda text: '\033[0;37m' + text + '\033[0m'
