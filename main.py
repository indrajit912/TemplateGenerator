# ProjectGenerator - A python script that can generate various 
# project dir template!
#
# Author: Indrajit Ghosh
# Created on: Aug 20, 2023
#
import sys, os
from pathlib import Path
from template_generator import *

TEMPLATES = [
    "pyscript",
    "pyproject",
    "flaskapp"
]

def main():
    script = ProjectTemplate(
        project_name="fancy_scr.py",
        root_dir=Path.home() / "Desktop",
        template='pyscript'
    )

    script.create_project()



if __name__ == '__main__':
    main()