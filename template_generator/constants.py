# Constants
import re

ROUTES_PY = r'''"""
%s

This module defines the routes and views for the Flask web application.

Author: %s
Created on: %s
"""

from %s import %s
from flask import render_template

import logging

logger = logging.getLogger(__name__)

#######################################################
#                      Homepage
#######################################################
@main_bp.route('/')
def index():
    logger.info("Visited homepage.")
    return render_template("index.html")

'''

APP_INIT_PY = r'''
from flask import Flask
import logging
from config import get_config, LOG_FILE

def configure_logging(app:Flask):
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s %(name)s: %(message)s',
        filename=str(LOG_FILE)
    )

    if app.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        
        # Fix werkzeug handler in debug mode
        logging.getLogger('werkzeug').handlers = []


def create_app(config_class=get_config()):
    """
    Creates an app with specific config class
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Configure logging
    configure_logging(app)

    from app.main import main_bp
    app.register_blueprint(main_bp)

    @app.route('/test/')
    def test():
        return '<h1>Testing the Flask Application!</h1>'

    return app

'''

ROUTE_INIT_PY = r"""# %s
#
# Author: %s
# Created On: %s
#

from flask import Blueprint

%s_bp = Blueprint(
    '%s', 
    __name__,
    template_folder="templates", 
    static_folder="static"
)

from app.%s import routes

"""

SCRIPT_MAIN_PY = r"""# %s - Description
#
# Author: %s
# Created on: %s
#
"""

MAIN_PY = r"""# %s - Description
#
# Author: %s
# Created on: %s
#

from %s import *

def main():
    print("Hello World!")


if __name__ == '__main__':
    main()
"""

DOT_ENV = r'''FLASK_ENV=dev'''

RUN_PY = r'''# %s
#
# Author: %s
# Created on: %s
#

"""
This script starts the Flask development server to run the web application.

Usage:
    - Run the Flask development server:
    >>> python3 run.py

    - Run the gunicorn server
    >>> /env/bin/gunicorn --bind 0.0.0.0:5000 run:app

Database initialization:
    1. flask shell
        >>> from app import db
        >>> db.create_all()

    2. python run.py

Note: Flask Migration
    1. flask db init
    2. flask db migrate -m 'Initial Migrate'
    3. flask db upgrade
    These 2 and 3 you need to do everytime you change some in your db!
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app.config['PORT'])'''

REQUIREMENTS = """
# Write down the modules you need to install and then
# run the cmd: ```pip install -r requirements.txt```
"""

FLASK_APP_CONFIG_PY = r'''"""
config.py

Author: %s
Created on: %s
"""
import os
from os.path import join, dirname
from dotenv import load_dotenv
from pathlib import Path
from secrets import token_hex

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

class Config:
    BASE_DIR = Path(__name__).parent.absolute()
    UPLOAD_DIR = BASE_DIR / 'uploads'
    LOG_FILE = BASE_DIR / 'app.log'
    PORT = os.environ.get("PORT") or 8080

    FLASK_ENV = os.environ.get("FLASK_ENV") or 'production'
    if FLASK_ENV in ['dev', 'developement']:
        FLASK_ENV = 'development'
    elif FLASK_ENV in ['prod', 'production', 'pro']:
        FLASK_ENV = 'production'
    else:
        FLASK_ENV = 'development'
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or token_hex(16)

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    # Add production-specific configurations if needed

def get_config():
    """
    Get the appropriate configuration based on the specified environment.
    :return: Config object
    """
    if Config.FLASK_ENV == 'production':
        return ProductionConfig()
    else:
        return DevelopmentConfig()
    

LOG_FILE = Config.LOG_FILE

'''

README_MD = r"""# Write your Markdown here"""

FLASK_REQU = r"""# Write down the modules you need to install and then
# run the cmd: ```pip install -r requirements.txt```
Flask
gunicorn
python-dotenv
"""


FLASK_INIT = r'''"""
Flask Web App Initialization

This module initializes the Flask web application instance, configures it, and imports the routes and extensions.

Attributes:
    app (Flask): The Flask web application instance.
"""
from flask import Flask

app = Flask(__name__)

# Import routes and extensions
from app import routes
'''

FLASK_BASE_HTML = r"""

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0">
    <title>{% block title %}{% endblock %}</title>
    
    {% block styles %}
    <link rel="stylesheet" href="{{ url_for('main.static', filename='css/style.css') }}">
    
    <!-- Add Bootstrap Stylesheet -->

    <!-- Add stylesheets for Bootstrap icons -->
    
    {% endblock %}
</head>

<body>

<section id="main-content" class="container">
    {% block content %}{% endblock %}
</section>

<!-- Include any additional JavaScript or external (Bootstrap) scripts here -->

</body>
</html>
"""
FLASK_APP_INDEX_HTML = r"""

{% extends 'base.html' %}
{% block title %}Home{% endblock %}
{% block styles %}
    {{ super() }}
{% endblock %}

{% block content %}
    <h1>Welcome to my Homepage!</h1>
{% endblock %}
"""

FLASK_EXTENSIONS_PY = r"""# app/extensions.py
# 
# Author: %s
# Created On: %s
#

"""

MIT_LICENSE = r"""MIT License

Copyright (c) 2023 Indrajit Ghosh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

PY_GITIGNORE = r"""
### Python ###
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
media/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#pdm.lock
#   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
#   in version control.
#   https://pdm.fming.dev/#use-with-ide
.pdm.toml

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/

# End of https://www.toptal.com/developers/gitignore/api/python

"""

PYPROJ_INIT_PY = r'''# %s/__init__.py

# Import statements
from .model import *

# Package-level variables
version = "1.0"
'''

MODEL_PY = r"""# %s/model.py
#
# Author: %s
# Created on: %s
#
"""

FLASK_STYLE_CSS = r"""/* static/styles.css */

@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap");

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    text-decoration: none;
    font-family: "Poppins", sans-serif;
    border: none;
    outline: none;
    letter-spacing: .4px;
}

html {
    scroll-behavior: smooth;
}

:root {
    --primary-color: #0056b3;   /* Dark Blue */
    --secondary-color: #4caf50; /* Green */
    --background-color: #f4f4f4; /* Light Gray */
    --text-color: #333;

    --color-black: #000000;  
    --color-white: #ffffff;
    --color-dark: #2c2c2c;      /* Dark Gray */
    --color-dark-variant: #444; /* Slightly Darker Gray */
}


body {
    background-color: var(--background-color);
}

/* Example style for the home page content */
h1,h2,h3,h4,h5 {
    line-height: 120%;
}

h1 {
    font-size: 48px;
    color: var(--color-black);
}

h2 {
    font-size: 28px;
    color: var(--color-dark-variant);
}

h3 {
    font-size: 26px;
    color: var(--color-black);
}

h4 {
    font-size: 19px;
    color: var(--color-black);
}

h4 {
    font-size: 18px;
    font-weight: 400;
}
"""

ERR_STYLE_CSS = r"""/* errors/static/css/error_style.css */
@import url('https://fonts.googleapis.com/css?family=Nunito+Sans');
:root {
  --blue: #0e0620;
  --white: #fff;
  --green: #2ccf6d;
}
html,
body {
  height: 100%;
}
body {
  display: flex;
  align-items: center;
  justify-content: center;
  font-family:"Nunito Sans";
  color: var(--blue);
  font-size: 1em;
}

.error_container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 40%;
}

button {
  font-family:"Nunito Sans";
}

h1 {
    font-size: 7.5em;
    margin: 15px 0px;
    font-weight:bold;
}
h2 {
  font-weight:bold;
}

.btn {
    z-index: 1;
    overflow: hidden;
    background: transparent;
    position: relative;
    padding: 8px 50px;
    border-radius: 30px;
    cursor: pointer;
    font-size: 1em;
    letter-spacing: 2px;
    transition: 0.2s ease;
    font-weight: bold;
    margin: 5px 0px;
    &.green {
      border: 4px solid var(--green);
      color: var(--blue);
      &:before {
        content: "";
        position: absolute;
        left: 0;
        top: 0;
        width: 0%;
        height: 100%;
        background: var(--green);
        z-index: -1;
        transition: 0.2s ease;
      }
      &:hover {
        color: var(--white);
        background: var(--green);
        transition: 0.2s ease;
        &:before {
          width: 100%;
        }
      }
    }
  }
  
"""

ERR_BASE_HTML = r"""<!-- error_base.html -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('main.static', filename='css/error_style.css') }}">
</head>
<body>

    <div class="error_container">
        <div class="col-md-6 align-self-center">
            {% block content %}{% endblock %}
    
            <button class="btn green" id="homeButton">HOME</button>
            <button class="btn green" id="backButton">BACK</button>
            {% if error %}
                <button class="btn green" id="detailsButton">DETAILS</button>
                <div id="errorDetails" style="display: none;">
                    <p>{{ error }}</p>
                </div>
            {% endif %}
        </div>
    </div>

    <script>
        document.getElementById("homeButton").addEventListener("click", function() {
            window.location.href = "/"; // Redirect to the home page
        });

        document.getElementById("backButton").addEventListener("click", function() {
            window.history.back(); // Go back in the browser history
        });

        var detailsButton = document.getElementById("detailsButton");
        var errorDetails = document.getElementById("errorDetails");

        if (detailsButton && errorDetails) {
            detailsButton.addEventListener("click", function() {
                errorDetails.style.display = (errorDetails.style.display === "none") ? "block" : "none";
            });
        }
    </script>
    
</body>
</html>
"""

ERR_404_HTML = r"""<!-- templates/errors/400.html -->

{% extends 'error_base.html' %}

{% block title %}Bad Request{% endblock %}

{% block content %}

    <h1>400</h1>
    <h2>Oops! Bad Request.</h2>
    <p>It seems there was a problem with your request.
      Please check the information you provided and try again.
    </p>

{% endblock %}
"""

ERR_500_HTML = r"""<!-- templates/errors/500.html -->

{% extends 'error_base.html' %}

{% block title %}Internal Server Error{% endblock %}

{% block content %}

    <h1>500</h1>
    <h2>Oops! Internal Server Error.</h2>
    <p>We're sorry, but there's been an internal server error on this website.
      Indrajit Ghosh, the owner of this site, has been notified and is actively working to fix the issue.
      Feel free to try again later. If the problem persists or if you would like to report this issue,
      please contact Indrajit.
      Thank you for your patience.
    </p>

{% endblock %}"""

ERR_HANDLERS_PY = r"""# Error Handlers for the site
#
# Author: %s
# Created On: %s
#

from flask import render_template


##########################################
#        Page not found!
##########################################
def page_not_found(error):
    return render_template('errors/404.html'), 404


##########################################
#        Internal Server Error!
##########################################
def internal_server_error(error):
    return render_template('errors/500.html', error=error), 500

"""

# 7-bit C1 ANSI sequences
ANSI_ESCAPE = re.compile(r"""
    \x1B  # ESC
    (?:   # 7-bit C1 Fe (except CSI)
        [@-Z\\-_]
    |     # or [ for CSI, followed by a control sequence
        \[
        [0-?]*  # Parameter bytes
        [ -/]*  # Intermediate bytes
        [@-~]   # Final byte
    )
""", re.VERBOSE
)