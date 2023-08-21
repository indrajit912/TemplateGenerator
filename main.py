# ProjectGenerator - A python script that can generate various 
# project dir template!
#
# Author: Indrajit Ghosh
# Created on: Aug 20, 2023
#
import sys, os
from pathlib import Path
from template_generator import *

def main():
    proj = ProjectTemplate(
        project_name="test project",
        root_dir=Path.home() / "Desktop",
        template='pyproject'
    )

    proj.create_project()



if __name__ == '__main__':
    main()