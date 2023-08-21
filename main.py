# ProjectGenerator - A python script that can generate various 
# project dir template!
#
# Author: Indrajit Ghosh
# Created on: Aug 20, 2023
#
from pathlib import Path
from template_generator import *
import click

TEMPLATES = [
    "pyscript",
    "pyproject",
    "flaskapp"
]

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


TEMPLATES_MAP = {
    "pyscript": pyscript_template,
    "pyproject": pyproject_template,
    "flaskapp": flaskapp_template
}

@click.command()
@click.option('--template', prompt='Choose a template', type=click.Choice(TEMPLATES))
def main(template):
    template_function = TEMPLATES_MAP[template]
    template_function()


if __name__ == '__main__':
    main()
