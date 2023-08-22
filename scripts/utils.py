# Utility Functions
# Author: Indrajit Ghosh
# Created On: Aug 22, 2023

import os

def clear_terminal_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def choose_from_list(lst: list):
    """
    Display a list of items and prompt the user to choose an option from the list.

    Args:
        lst (list): A list of items to choose from.

    Returns:
        Any: The selected item from the list.

    This function presents the user with a numbered list of items, each displayed
    with an index and corresponding text. The user is prompted to input the index
    of their desired option. The input is validated to ensure it is a valid number
    within the range of available options. If the input is invalid, appropriate error
    messages are displayed.

    Note:
        This function uses the 'clear_terminal_screen' and 'IndraStyle.TURQUOISE'
        (assumed to be defined elsewhere) to enhance the display.

    Example:
        options = ["Option A", "Option B", "Option C"]
        chosen_option = choose_from_list(options)
        print("You chose:", chosen_option)
    """
    clear_terminal_screen()
    for i, item in enumerate(lst, start=1):
        print(f"\033[96m  {i}. \033[0m\033[93m{item}\033[0m")

    while True:
        try:
            choice = int(input("\n\x1b[38;2;64;224;208m" + "Which option do you want to choose: \033[0m"))
            if 1 <= choice <= len(lst):
                return lst[choice - 1]
            else:
                print("\033[91mInvalid option. Please choose a valid number.\033[0m")
        except ValueError:
            print("\033[91mInvalid input. Please enter a number.\033[0m")
