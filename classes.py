# Classes required for the project

import subprocess, datetime, os
from pathlib import Path

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
            template:str, 
            root_dir:Path=None
    ):
        self.project_name:str = project_name.title().replace(' ', '_')
        self.template:str = template
        self.root_dir:Path = (
            Path.cwd()
            if root_dir is None
            else Path(root_dir)
        )

    def create_project(self):

        # Create the project_dir
        if self.template == 'pyproject':
            self.create_pyproject_template()
        elif self.template == 'flaskapp':
            pass
        elif self.template == 'pyscript':
            pass
        else:
            print("Invalid template name")

    def create_pyproject_template(self):
        """
        Creates a Python project
        """
        pass


    def create_virtualenv(self, venv_path:Path, python_executable:Path):
        try:
            subprocess.run(['virtualenv', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            subprocess.run([python_executable, "-m", "virtualenv", venv_path])

        except subprocess.CalledProcessError:
            import venv
            builder = venv.EnvBuilder(system_site_packages=False, with_pip=True, prompt='(my_venv) ')
            builder.create(venv_path, symlinks=False, clear=True, upgrade=True, python=python_executable)



if __name__ == "__main__":
    # Create a root directory
    root = Directory(
        name="fancy_dir",
    )

    # Add files and subdirectories
    root.add_file("file1.txt", content="Hello, world!")
    root.add_directory("subdir1")

    # Access and modify a subdirectory
    subdir1 = root._content["subdir1"]
    subdir1.add_file("file2.txt", content="This is a text file.")
    subdir1.add_file("binary.dat", binary_content=b"\x00\x01\x02\x03")

    # Create another subdirectory and add files
    root.add_directory("subdir2")
    subdir2 = root._content["subdir2"]
    subdir2.add_file("file3.txt", content="Another text file.")

    # Print the directory structure
    print(root)

