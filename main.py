# ProjectGenerator - A python script that can generate various 
# project dir template!
#
# Author: Indrajit Ghosh
# Created on: Aug 20, 2023
#
from pathlib import Path
from template_generator import *
import click, sys, os

TEMPLATES = [
    "pyscript",
    "pyproject",
    "flaskapp",
    "quit"
]

def clear_terminal_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def choose_from_list(lst: list):
    clear_terminal_screen()
    for i, item in enumerate(lst, start=1):
        print(f"\033[96m  {i}. \033[0m\033[93m{item}\033[0m")
    
    while True:
        try:
            choice = int(input(f"\n{IndraStyle.TURQUOISE}Which option do you want to choose: \033[0m"))
            if 1 <= choice <= len(lst):
                return lst[choice - 1]
            else:
                print("\033[91mInvalid option. Please choose a valid number.\033[0m")
        except ValueError:
            print("\033[91mInvalid input. Please enter a number.\033[0m")

def pyscript_template():
    # Functionality for pyscript template
    _script_name = input("Enter the python script name (e.g. `main.py`): ")
    _auth = input("Enter the author: ")
    _script_name = (
        _script_name
        if _script_name.endswith('.py')
        else _script_name + ".py"
    )

    _auth = (
        "Indrajit Ghosh"
        if _auth == ''
        else _auth
    )

    _script = ProjectTemplate(
        project_name=_script_name,
        root_dir=Path.cwd(),
        template='pyscript'
    )

    _script.create_project()


def pyproject_template():
    # Functionality for pyproject template
    _proj_name = input("Enter the name of the project: ")

    _auth = input("Enter the author: ")
    _auth = (
        "Indrajit Ghosh"
        if _auth == ''
        else _auth
    )

    pyproj = ProjectTemplate(
        project_name=_proj_name,
        project_author=_auth,
        root_dir=Path.cwd(),
        template='pyproject'
    )

    pyproj.create_project()


def flaskapp_template():
    # Functionality for flaskapp template
    _app_name = input("Enter the name of the Flask app: ")

    _auth = input("Enter the author: ")
    _auth = (
        "Indrajit Ghosh"
        if _auth == ''
        else _auth
    )

    _app = ProjectTemplate(
        project_name=_app_name,
        project_author=_auth,
        root_dir=Path.cwd(),
        template='flaskapp'
    )

    _app.create_project()


def main():
    if len(sys.argv) < 2:
        template_choice = choose_from_list(TEMPLATES)
    elif len(sys.argv) == 2:
        template_choice = sys.argv[1]

    else:
        msg = r"""TemplateGenerator
Author: Indrajit Ghosh

Usages:
    1. python3 main.py
    2. python3 main.py pyproject
"""
        print(msg)

        sys.exit(1)

    if template_choice == 'pyscript':
        pyscript_template()
    elif template_choice == 'pyproject':
        pyproject_template()
    elif template_choice == 'flaskapp':
        flaskapp_template()
    elif template_choice == 'quit':
        sys.exit()
    else:
        print(f"ERROR: Unknown template '{template_choice}'.\n")



if __name__ == '__main__':
    main()
