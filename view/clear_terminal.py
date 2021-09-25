import os


class ClearTerminal:
    @classmethod
    def clear_terminal(cls):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
