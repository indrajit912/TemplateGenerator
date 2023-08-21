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
    my_dir = Directory.instantiate_dir_from_path(Path.cwd())

    print(my_dir.tree)


if __name__ == '__main__':
    main()