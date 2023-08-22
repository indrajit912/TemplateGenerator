# Template Generator

This repository contains a Python package named `template_generator` developed by Indrajit Ghosh. This package provides classes for generating project templates and creating project structures with ease. It includes features such as creating directories, files, and project templates like `pyproject`, `flaskapp`, and more.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Classes](#classes)
- [Author](#author)
- [License](#license)

## Installation

- Open Terminal window!
- `clone` this repo by
```bash
git clone https://github.com/indrajit912/TemplateGenerator.git
```
- Change the working directory to `TemplateGenerator` by
```bash
cd TemplateGenerator
```
- Create a `virtualenv` by
```bash
virtualenv env
```
- Activate the `virtualenv`
```bash
source env/bin/activate
```
- Install dependencies by
```bash
pip install -r requirements.txt
```
- Run `main.py`
```bash
python3 main.py
```
- Run `directory_tree.py`
```bash
python3 directory_tree.py
```
Output:
```bash
├── requirements.txt
├── directory_tree.py
├── main.py
├── template_generator
│   ├── terminal_style.py
│   ├── __init__.py
│   ├── model.py
│   ├── constants.py
├── tests
├── scripts
│   └── utils.py
├── README.md
├── setup.py
├── .gitignore
```


## Usage

The template_generator package provides classes that can be used to create project structures and templates. You can instantiate these classes and use their methods to generate your desired project layout. Here's how you can use it:

```python
from template_generator import File, Directory, ProjectTemplate

# Create a Directory instance
project_dir = Directory(name="my_project")

# Add files and directories to the project_dir
project_dir.add_file(name="file.txt", content="Hello, world!")
project_dir.add_directory(name="sub_directory")

# Create the project_dir
project_dir.create(path="/path/to/destination")

# Create a ProjectTemplate instance
template = ProjectTemplate(project_name="my_flask_app", template="flaskapp")

# Create the project template
template.create_project()

```

## Classes

### `File`
A class representing a file. It provides methods to set content, binary content, and create the file.

### `Directory`
A class representing a directory. It allows you to add files and subdirectories, generate directory trees, and create directories with their contents.

### `ProjectTemplate`
A class for generating project templates such as pyproject, flaskapp, etc. It provides methods to create the specified template and virtual environment.

## Author

This package is developed by Indrajit Ghosh. You can contact the author at indrajitghosh912@gmail.com.

## License

This project is licensed under the [MIT License](LICENSE).


