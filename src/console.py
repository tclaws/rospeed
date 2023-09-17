
import os
import pyfiglet
import shutil
import ctypes
from datetime import datetime
from colorama import Fore, Style

def setTitle(title: str):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

def logo():
    columns, rows = shutil.get_terminal_size()
    ascii_text = pyfiglet.figlet_format("RoSpeed", font="fender")
    lines = ascii_text.split("\n")
    positions = []
    x = int(columns / 2 - len(max(lines, key=len)) / 2)
    for i in range(len(lines)):
        y = int(rows / 2 - len(lines) / 2 + i)
        positions.append(y)

    print("\033[1m\033[36m", end="")
    for i in range(len(lines)):
        print(f"\033[{positions[i]};{x}H{lines[i]}")

    print("\033[1m\033[33;7m", end="")
    made_by_text = "GitHub: github.com/novak5712"
    made_by_x = int(columns / 2 - len(made_by_text) / 2)
    made_by_y = positions[-1] + 2
    print(f"\033[{made_by_y};{made_by_x}H{made_by_text}")
    print("\033[0m", end="")
    print("\n")
    
def clear():
    if 'nt' in os.name:
        os.system('cls')
    else:
        os.system('clear')

def timet():
       return Style.BRIGHT + Fore.BLACK + f"[{datetime.now().strftime('%I:%M')}] "

def log(object):
    print(timet() + f"{Style.BRIGHT}{Fore.LIGHTMAGENTA_EX}INFO {Fore.WHITE}{object}")

def ok(object):
    print(timet() + f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}SUCCESS {Fore.WHITE}{object}")

def fatal(object):
    print(timet() + f"{Style.BRIGHT}{Fore.LIGHTRED_EX}ERROR {Fore.WHITE}{object}")

def warn(object):
    print(timet() + f"{Style.RESET_ALL}{Fore.LIGHTYELLOW_EX}WARN {Style.BRIGHT}{Fore.WHITE}{object}")

def boot(object):
    print(timet() + f"{Style.BRIGHT}{Fore.LIGHTCYAN_EX}BOOT {Fore.WHITE}{object}", end="\n")

def config(object):
    print(timet() + f"{Style.BRIGHT}{Fore.LIGHTBLUE_EX}CONFIG {Fore.WHITE}{object}", end="\n")
