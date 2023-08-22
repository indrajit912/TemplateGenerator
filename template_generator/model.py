# Classes required for the project
#
# Author: Indrajit Ghosh
# Created On: Aug 20, 2023
#

import subprocess, datetime, sys
from pathlib import Path
from .constants import *
from .terminal_style import IndraStyle

__all__ = [
    "File",
    "Directory",
    "ProjectTemplate"
]

class File:
    """
    A Python class to represent a File.

    Author: Indrajit Ghosh
    Created On: Aug 20, 2023

    :param `content`: Text content of the file.
    :param `binary_content`: Binary content of the file.
    :param `name`: Name of the file.
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

    @classmethod
    def instantiate_from_file_path(cls, filepath: Path):
        filepath = Path(filepath)
        with filepath.open("rb") as f:
            binary_content = f.read()
        return cls(binary_content=binary_content, name=filepath.name)

    def create(self, path):
        path = Path(path) / self._name
        if self._binary_content:
            with path.open("wb") as f:
                f.write(self._binary_content)
        elif self._content:
            with path.open("w") as f:
                f.write(self._content)
        else:
            with path.open("w") as f:
                f.write("")

class Directory:
    """
    A Python class to represent a directory.

    Author: Indrajit Ghosh
    Created On: Aug 20, 2023
    """
    IGNORE = (
        '.git', 
        '__pycache__',
        'env',
        'venv'
    )

    STYLE = {
        "dir": IndraStyle.AQUA + IndraStyle.BOLD,
        "file": IndraStyle.ORANGE,
        "image": IndraStyle.CRIMSON,
        "txt": IndraStyle.MEDIUM_ORCHID,
        "pdf": IndraStyle.AQUA_MARINE,
        "video": IndraStyle.PURPLE,
        "py": IndraStyle.PINK,
        "ipynb": IndraStyle.CADET_BLUE,
        "json": IndraStyle.PALE_TURQUOISE,
        "md": IndraStyle.GREEN_YELLOW,
        "reset": IndraStyle.END,
        "tex": IndraStyle.BLUE_VIOLET,
        "bib": IndraStyle.CRIMSON
    }

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


    def _generate_entry_strings(self, level=0):
        indent = "    "
        for name, entry in self._content.items():
            entry_string = f"{indent * level}{name}"
            if isinstance(entry, File):
                entry_string += " (File)"
            elif isinstance(entry, Directory):
                entry_string += " (Directory)"
            yield entry_string
            if isinstance(entry, Directory):
                yield from entry._generate_entry_strings(level + 1)

    @classmethod
    def _colored_entry(cls, entry_name, entry_type):
        if entry_type == "File":
            fileobj = Path(entry_name)

            if fileobj.suffix == '.py':
                color_code = cls.STYLE['py']

            elif fileobj.suffix == '.pdf':
                color_code = cls.STYLE['pdf']

            elif fileobj.suffix == '.tex':
                color_code = cls.STYLE['tex']

            elif fileobj.suffix == '.txt':
                color_code = cls.STYLE['txt']

            elif fileobj.suffix in ['.jpg', '.png', '.jpeg', '.JPG', '.PNG', 'JPEG']:
                color_code = cls.STYLE['image']

            elif fileobj.suffix in ['.mp4', '.mkv', '.mov', '.MOV']:
                color_code = cls.STYLE['video']

            elif fileobj.suffix == '.bib':
                color_code = cls.STYLE['bib']

            else:
                color_code = cls.STYLE['file']

        else:
            color_code = IndraStyle.AQUA + IndraStyle.BOLD  # Green color for directories

        reset_code = "\033[0m"  # Reset color

        return f"{color_code}{entry_name}{reset_code}"

    def _tree(self, prefix:str=''):
        # prefixes:
        space =  '    '
        branch = '│   '

        # pointers:
        tee =    '├── '
        last =   '└── '

        contents = list(self._content)
        pointers = [tee] * (len(self._content) - 1) + [last]

        for pointer, entry in zip(pointers, contents):
            if entry in self.IGNORE:
                continue

            yield prefix + pointer + self._colored_entry(entry, "File" if isinstance(self._content[entry], File) else "Directory")

            if isinstance(self._content[entry], Directory):
                extension = branch if pointer == tee else space
                subdir: Directory = self._content[entry]
                yield from subdir._tree(prefix=prefix + extension)

    @property
    def tree(self):
        return "\n".join(self._tree())

    def __str__(self):
        return ANSI_ESCAPE.sub('', "\n".join(self._tree()))
    

    @classmethod
    def instantiate_dir_from_path(cls, dir_path: Path):
        """
        Create a Directory instance by instantiating it from a directory path.

        :param `dir_path`: Path to the directory.
        :return: A Directory instance representing the directory contents.
        """
        dir_path = Path(dir_path)
        directory = cls(name=dir_path.name)  # Create a Directory instance with the directory name
        
        for entry_path in dir_path.iterdir():
            entry_name = entry_path.name

            if entry_name in cls.IGNORE:
                continue  # Skip specific directories

            if entry_path.is_file():
                def read_file_content(file_path):
                    with file_path.open("rb") as f:
                        return f.read()
                directory.add_file(entry_name, binary_content=read_file_content(entry_path))
            elif entry_path.is_dir():
                sub_directory = cls.instantiate_dir_from_path(entry_path)
                directory.add_directory(entry_name)
                directory._content[entry_name] = sub_directory
        
        return directory
    
    @classmethod
    def get_tree_from_path(cls, dir_path: Path, prefix: str=''):
        """A recursive generator, given a directory Path object
        will yield a visual tree structure line by line
        with each line prefixed by the same characters
        """
        # prefixes:
        space =  '    '
        branch = '│   '

        # pointers:
        tee =    '├── '
        last =   '└── ' 
        contents = list(dir_path.iterdir())
        # contents each get pointers that are ├── with a final └── :
        pointers = [tee] * (len(contents) - 1) + [last]
        for pointer, path in zip(pointers, contents):
            if path.name in Directory.IGNORE:
                continue  # Skip specific directories
            yield prefix + pointer + cls._colored_entry(
                entry_name=path.name,
                entry_type='File' if path.is_file() else 'Directory'
            )
            if path.is_dir(): # extend the prefix and recurse:
                extension = branch if pointer == tee else space 
                # i.e. space because last, └── , above so no more |
                yield from cls.get_tree_from_path(path, prefix=prefix+extension)


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
            project_author:str="Indrajit Ghosh",
            root_dir:Path=None
    ):
        self._project_name:str = project_name
        self._template:str = template
        self._root_dir:Path = (
            Path.cwd()
            if root_dir is None
            else Path(root_dir)
        )
        self._author = project_author

    def create_project(self):

        # Create the project_dir
        if self._template == 'pyproject':
            proj_dir: Path = self._create_pyproject_template()
        elif self._template == 'flaskapp':
            proj_dir: Path = self._create_flaskapp_template()
        elif self._template == 'pyscript':
            _script_name = self._project_name.lower().replace(' ', '_')

            # Create `_script_name.py`
            script = File(
                name=_script_name + ".py",
                content=SCRIPT_MAIN_PY % (_script_name, self._author, self.TODAY)
            )
            script.create(path=self._root_dir)
            
        else:
            print("Invalid template name")
            sys.exit(1)
        
        # Print necessary info
        if self._template != 'pyscript':
            msg = (
                f"\n1. A `{self._template}` has been created at the following dir:"
                + f"\n\t`{proj_dir}`"
                + "\n\n2. A virtualenv has been created too. You can use the following cmds to activate it:"
                + f"\n\t- cd {proj_dir}"
                + "\n\t- source env/bin/activate\n"
            )

            if self._template == 'flaskapp':
                msg += (
                    "\n3. You can run the flaskapp by the following cmd:"
                    + "\n\t- source env/bin/activate"
                    + "\n\t- pip install -r requirements.txt"
                    + "\n\t- env/bin/python run.py\n"
                )

            print(msg)

        else:
            print("\nA `pyscript` has been created at the following path:")
            print(f"\t{self._root_dir}/{_script_name}\n")


    def _create_pyproject_template(self):
        """
        Creates a Python project.

        Returns:
        --------
            `project_dir_path`: Path
        """
        _proj_name = self._project_name.title().replace(' ', '_')
        _proj_dir_name = _proj_name.lower()
        project_dir = Directory(name=_proj_name)

        # Add `_proj_name` dir
        project_dir.add_directory(
            name=_proj_dir_name
        )

        # Add `_proj_name/__init__.py`
        project_dir._content[_proj_dir_name].add_file(
            name="__init__.py",
            content=PYPROJ_INIT_PY % _proj_name
        )

        # Add `_proj_name/model.py`
        project_dir._content[_proj_dir_name].add_file(
            name="model.py",
            content=MODEL_PY % (_proj_name, self._author, self.TODAY)
        )

        # Add .gitignore
        project_dir.add_file(
            name=".gitignore",
            content=PY_GITIGNORE
        )

        # Add `main.py`
        project_dir.add_file(
            name="main.py",
            content=MAIN_PY % (_proj_name, self._author, self.TODAY, _proj_name)
        )

        # Add `requirements.txt`
        project_dir.add_file(
            name="requirements.txt",
            content=REQUIREMENTS
        )

        # Add `README.md`
        project_dir.add_file(
            name="README.md",
            content=README_MD
        )

        # Add `setup.py`
        project_dir.add_file(
            name="setup.py"
        )


        # Create the project_dir
        project_dir.create(path=self._root_dir)
        project_dir_path: Path = self._root_dir / _proj_name

        # Create venv
        self.create_virtualenv(
            venv_path=project_dir_path / "env",
            python_executable=sys.executable
        )

        return project_dir_path
    
    def _create_flaskapp_template(self):
        """
        Creates a Flask App project.

        Returns:
        --------
            `project_dir_path`: Path
        """
        _proj_name = self._project_name.title().replace(' ', '_')
        project_dir = Directory(name=_proj_name)

        # Add `app` directory
        project_dir.add_directory(name='app')

        # Add `app/routes.py`
        project_dir._content['app'].add_file(
            name='routes.py',
            content=ROUTES_PY
        )

        # Add `app/__init__.py`
        project_dir._content['app'].add_file(
            name="__init__.py",
            content=FLASK_INIT
        )

        # Add `app/templates`
        project_dir._content['app'].add_directory(
            name="templates"
        )

        # Add `app/templates/index.html`
        project_dir._content['app']._content['templates'].add_file(
            name="index.html",
            content=FLASK_APP_INDEX_HTML
        )

        # Add `app/static/`
        project_dir._content['app'].add_directory(
            name="static"
        )

        # Add `app/static/css`
        project_dir._content['app']._content['static'].add_directory(
            name="css"
        )

        # Add `app/static/css/style.css`
        project_dir._content['app']._content['static']._content['css'].add_file(
            name="style.css",
            content=FLASK_STYLE_CSS
        )

        # Add `app/static/images`
        project_dir._content['app']._content['static'].add_directory(
            name="images"
        )
        

        # Add .gitignore
        project_dir.add_file(
            name=".gitignore",
            content=PY_GITIGNORE
        )

        # Add `run.py`
        project_dir.add_file(
            name="run.py",
            content=RUN_PY % (_proj_name, self._author, self.TODAY)
        )

        # Add `requirements.txt`
        project_dir.add_file(
            name="requirements.txt",
            content=FLASK_REQU
        )

        # Add `config.py`
        project_dir.add_file(
            name="config.py",
            content=FLASK_APP_CONFIG_PY
        )

        # Add `README.md`
        project_dir.add_file(
            name="README.md",
            content=README_MD
        )

        # Add `LICENSE`
        project_dir.add_file(
            name="LICENSE",
            content=MIT_LICENSE
        )

        # Add `scripts` dir
        project_dir.add_directory(name="scripts")


        # Create the project_dir
        project_dir.create(path=self._root_dir)
        project_dir_path: Path = self._root_dir / _proj_name

        # Create venv
        self.create_virtualenv(
            venv_path=project_dir_path / "env",
            python_executable=sys.executable
        )

        return project_dir_path


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
    print("\nClasses required for `ProjectTemplate`.\n")
