# A script that prints the directory tree on terminal
# 
# Author: Indrajit Ghosh
# Created On: Aug 21, 2023
#

from template_generator import Directory
import sys
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        given_dir = Path.cwd()

    elif len(sys.argv) == 2:
        given_dir_path = Path(sys.argv[1])
        if given_dir_path.exists():
            given_dir = given_dir_path
        else:
            if not (Path.home() / given_dir_path).exists():
                print(f"`The path {given_dir_path}` doesn't exists!")
                sys.exit()
            else:
                given_dir = Path.home() / given_dir_path

    else:
        msg = f"""::: ERROR :::
        Script: {sys.argv[0]}

        USAGE: 1. python3 {sys.argv[0]}
               2. python3 {sys.argv[0]} <directory>
        """
        print(msg)
        sys.exit(1)


    given_dir_tree = "\n".join(Directory.get_tree_from_path(given_dir))

    print(given_dir_tree)
    

if __name__ == '__main__':
    main()