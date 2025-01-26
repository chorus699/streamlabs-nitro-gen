import datetime
from colorama import Fore, Style, init
import os

class Console:
    def __init__(self) -> None:
        init(autoreset=True)
        self.colors = {
            "green": Fore.GREEN,
            "red": Fore.RED,
            "yellow": Fore.YELLOW,
            "blue": Fore.BLUE,
            "magenta": Fore.MAGENTA,
            "cyan": Fore.CYAN,
            "white": Fore.WHITE,
            "black": Fore.BLACK,
            "reset": Style.RESET_ALL,
            "lightblack": Fore.LIGHTBLACK_EX,
            "lightred": Fore.LIGHTRED_EX,
            "lightgreen": Fore.LIGHTGREEN_EX,
            "lightyellow": Fore.LIGHTYELLOW_EX,
            "lightblue": Fore.LIGHTBLUE_EX,
            "lightmagenta": Fore.LIGHTMAGENTA_EX,
            "lightcyan": Fore.LIGHTCYAN_EX,
            "lightwhite": Fore.LIGHTWHITE_EX,
            "darkblue": Fore.BLUE  # Added dark blue color
        }

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def timestamp(self):
        return datetime.datetime.now().strftime(f"{Fore.BLUE}%H:%M:%S{Style.RESET_ALL}")  # Dark Blue Timestamp

    def purchased(self, message, obj=""):
        print(f"{self.colors['lightblack']}{self.timestamp()} --> {self.colors['magenta']}bought {self.colors['lightblack']}➜ {self.colors['white']}{message} [{self.colors['lightgreen']}{obj}{self.colors['white']}] {self.colors['reset']}")

    def promo(self, message, obj=""):
        print(f"{self.colors['lightblue']}{self.timestamp()} --> {self.colors['darkblue']}promo fetched {self.colors['lightblack']}➜ {self.colors['white']}{message} [{self.colors['lightgreen']}{obj}{self.colors['white']}] {self.colors['reset']}")

    def success(self, message, obj=""):
        print(f"{self.colors['lightblack']}{self.timestamp()} --> {self.colors['green']}success {self.colors['lightblack']}➜ {self.colors['white']}{message} [{self.colors['lightgreen']}{obj}{self.colors['white']}] {self.colors['reset']}")

    def error(self, message, obj=""):
        print(f"{self.colors['lightblack']}{self.timestamp()} --> {self.colors['red']}error   {self.colors['lightblack']}➜ {self.colors['white']}{message} [{self.colors['lightred']}{obj}{self.colors['white']}] {self.colors['reset']}")

    def info(self, message, obj=""):
        print(f"{self.colors['lightblack']}{self.timestamp()} --> {self.colors['lightgreen']}info    {self.colors['lightblack']}➜ {self.colors['white']}{message} [{self.colors['lightgreen']}{obj}{self.colors['white']}] {self.colors['reset']}")
