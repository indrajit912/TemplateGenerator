# Classes required for the project

import subprocess, datetime, os, sys
from pathlib import Path
from constants import *

__all__ = [
    "File",
    "Directory"
]

class File:
    """
    A Python class to represent a File.

    Author: Indrajit Ghosh
    Created On: Aug 20, 2023
    """
    def __init__(self, content=None, binary_content=None, name=None):
        self._content = content
        self._binary_content = binary_content
        self._name = name if name else "untitled_file"

    @property
    def content(self):
        return self._content
    
    @content.setter
    def content(self, new):
        self._content = new

    @property
    def binary_content(self):
        return self._binary_content
    
    @binary_content.setter
    def binary_content(self, new):
        self._binary_content = new

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_name):
        self._name = new_name if new_name else "untitled_file"

    def create(self, path):
        path = Path(path) / self._name
        if self._binary_content:
            with path.open("wb") as f:
                f.write(self._binary_content)
        else:
            with path.open("w") as f:
                f.write(self._content)

class Directory:
    """
    A Python class to represent a directory.

    Author: Indrajit Ghosh
    Created On: Aug 20, 2023
    """
    def __init__(self, name=None):
        self._content = {}
        self._name = name if name else "untitled_directory"

    @property
    def content(self):
        return self._content
    
    @content.setter
    def content(self, new):
        self._content = new

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_name):
        self._name = new_name if new_name else "untitled_directory"

    def add_file(self, name, content=None, binary_content=None):
        self._content[name] = File(content, binary_content, name)

    def add_directory(self, name):
        self._content[name] = Directory(name)

    def create(self, path):
        root_path = Path(path) / self._name
        root_path.mkdir(parents=True)

        for name, entry in self._content.items():
            
            if isinstance(entry, File):
                entry.name = name
                entry.create(root_path)
            elif isinstance(entry, Directory):
                entry.create(root_path)

    def __str__(self, level=0):
        indent = "    "
        output = ""
        for name, entry in self._content.items():
            output += f"{indent * level}{name}"
            if isinstance(entry, File):
                output += " (File)\n"
            elif isinstance(entry, Directory):
                output += " (Directory)\n"
                output += entry.__str__(level + 1)
        return output


class ProjectTemplate:
    """
    A Python class to represent a project template such as `pyproject`
    `flaskapp` etc.

    Author: Indrajit Ghosh
    Created On: Aug 20, 2023
    """
    TODAY:str = datetime.datetime.strftime(datetime.datetime.now(), '%b %d, %Y')

    def __init__(
            self, 
            project_name:str, 
            template:str='pyproject', 
            project_author:str=None,
            root_dir:Path=None
    ):
        self._project_name:str = project_name
        self._template:str = template
        self._root_dir:Path = (
            Path.cwd()
            if root_dir is None
            else Path(root_dir)
        )
        self._author = (
            project_author
            if project_author
            else "Indrajit Ghosh"
        )

    def create_project(self):

        # Create the project_dir
        if self._template == 'pyproject':
            self.create_pyproject_template()
        elif self._template == 'flaskapp':
            pass
        elif self._template == 'pyscript':
            pass
        else:
            print("Invalid template name")

    def create_pyproject_template(self):
        """
        Creates a Python project
        """
        _proj_name = self._project_name.title().replace(' ', '_')
        project_dir = Directory(name=_proj_name)

        # Add .gitignore
        project_dir.add_file(
            name=".gitignore",
            content=PY_GITIGNORE
        )

        # Add `main.py`
        project_dir.add_file(
            name="main.py",
            content=MAIN_PY % (_proj_name, self._author, self.TODAY)
        )

        # Add `requirements.txt`
        project_dir.add_file(
            name="requirements.txt",
            content=REQUIREMENTS
        )

        # Create the project_dir
        project_dir.create(path=self._root_dir)
        project_dir_path = self._root_dir / _proj_name

        # Create venv
        self.create_virtualenv(
            venv_path=project_dir_path / "env",
            python_executable=sys.executable
        )


    def create_virtualenv(self, venv_path:Path, python_executable:Path):
        try:
            subprocess.run(
                [python_executable, "-m", 'virtualenv', '--version'], 
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
            )
            subprocess.run(
                [python_executable, "-m", "virtualenv", str(venv_path)],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
            )
        except subprocess.CalledProcessError:
            print("\nERROR: `virtualenv` is not installed. Use following cmd to install:\n\t `python3 -m pip install virtualenv`\n")
            

if __name__ == "__main__":
    # Create a root directory
    proj = ProjectTemplate(project_name="Testing", root_dir=Path.home() / "Desktop")

    proj.create_project()

