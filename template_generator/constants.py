# Constants
import re

ROUTES_PY = r'''"""
%s

This module defines the routes and views for the Flask web application.

Author: %s
Created on: %s
"""
import logging

from flask import render_template, abort

from %s import %s

logger = logging.getLogger(__name__)


#######################################################
#                      Homepage
#######################################################
@main_bp.route('/')
def index():
    logger.info("Visited homepage.")
    return render_template("index.html")

    #######################################################
#                      Test Errors
#######################################################
@main_bp.route('/dev/errors/<int:code>')
def dev_error(code):
    """
    Test route to manually trigger error pages.

    Supported codes:
        401 - Unauthorized
        403 - Forbidden
        404 - Not Found
        422 - Unprocessable Entity
        500 - Internal Server Error

    Example usage:
        /dev/error/403
    """
    if code == 401:
        abort(401)
    elif code == 400:
        abort(400)
    elif code == 403:
        abort(403)
    elif code == 404:
        abort(404)
    elif code == 422:
        abort(422)
    elif code == 500:
        abort(500)
    else:
        return f"Unsupported error code {code}. Try 400, 401, 403, 404, 422, or 500."

'''

APP_INIT_PY = r'''
import logging

from flask import Flask

# Local application imports
from config import LOG_FILE, Config
from .extensions import db, migrate, moment, csrf


def configure_logging(app:Flask):
    # --- Main application logger ---
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s %(name)s: %(message)s',
        filename=str(LOG_FILE),
        datefmt='%d-%b-%Y %I:%M:%S %p'
    )

    if app.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        
        # Fix werkzeug handler in debug mode
        logging.getLogger('werkzeug').handlers = []


def create_app(config_class=Config):
    """
    Creates an app with specific config class
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Configure logging
    configure_logging(app)

    # Register error handlers
    from app.errors.handlers import register_error_handlers
    register_error_handlers(app)

     # Add cli commands
    from cli import deploy
    app.cli.add_command(deploy)

    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)

    # register blueprints
    from app.main import main_bp
    app.register_blueprint(main_bp)

    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.api import api_v1
    csrf.exempt(api_v1)
    app.register_blueprint(api_v1, url_prefix='/api/v1')

    return app

'''

API_INIT_PY = r"""# app/api/__init__.py
#
# Author: %s
# Created On: %s
#

from app.api.v1 import api_v1
"""

API_V1_INIT_PY = r"""# app/api/v1/__init__.py
#
# Author: %s
# Created On: %s
#

from flask import Blueprint

api_v1 = Blueprint(
    'api_v1', 
    __name__
)

from app.api.v1 import user_api
"""


AUTH_ROUTES_PY = r"""# %s
#
# Author: %s
# Created On: %s
#

import logging

from flask import render_template
from . import auth_bp

logger = logging.getLogger(__name__)

# Login view (route)
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

"""

ROUTE_INIT_PY = r"""# %s
#
# Author: %s
# Created On: %s
#

from flask import Blueprint

%s_bp = Blueprint(
    '%s', 
    __name__
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

DOT_ENV = r"""
# Development environment variables
FLASK_APP=%s
FLASK_ENV=development
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=8080
FLASK_DEBUG=true
"""

SERVER_PY = r'''# %s
#
# Author: %s
# Created on: %s
#

"""
This script starts the Flask development server to run the web application.

Usage:
    - Run the Flask development server:
    >>> flask run

Note: Flask Migration
    1. flask db init
    2. flask db migrate -m 'Initial Migrate'
    3. flask db upgrade
    These 2 and 3 you need to do everytime you change some in your db!
"""

from app import create_app

app = create_app()
'''

CLI_PY = r'''# cli.py
#
# Author: %s
# Created on: %s
#

import logging
import click
from flask_migrate import upgrade
from flask.cli import FlaskGroup
from app import create_app

cli = FlaskGroup(create_app=create_app)

logger = logging.getLogger(__name__)

@cli.command("deploy")
def deploy():
    """Run deployment tasks."""  
    # migrate database to latest revision
    upgrade()

if __name__ == '__main__':
    cli()
'''

SCRIPTS_UTILS_PY = r'''# Some utility functions
#
# Author: Indrajit Ghosh
# Created On: May 10, 2025
#
import hashlib
import secrets
from datetime import datetime, timezone

def utcnow():
    """
    Get the current UTC datetime.

    Returns:
        datetime: A datetime object representing the current UTC time.
    """
    return datetime.now(timezone.utc)


def sha256_hash(raw_text:str):
    """Hash the given text using SHA-256 algorithm.

    Args:
        raw_text (str): The input text to be hashed.

    Returns:
        str: The hexadecimal representation of the hashed value.

    Example:
        >>> sha256_hash('my_secret_password')
        'e5e9fa1ba31ecd1ae84f75caaa474f3a663f05f4'
    """
    hashed = hashlib.sha256(raw_text.encode()).hexdigest()
    return hashed

def generate_token():
    # Generate a secure random token (hex string)
    token = secrets.token_hex(32)  # 64 chars long

    # Hash the token for storage (never store plain tokens in code)
    token_hash = hashlib.sha256(token.encode()).hexdigest()

    return token, token_hash
'''

REQUIREMENTS = """
# Write down the modules you need to install and then
# run the cmd: ```pip install -r requirements.txt```
"""

FLASK_APP_CONFIG_PY = r'''"""
config.py

Author: %s
Created on: %s

This module provides configuration settings for the SoundBit application,
including email configuration, environment settings, and database URIs.
"""
import os
from pathlib import Path
from os.path import join, dirname
from dotenv import load_dotenv
from secrets import token_hex

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

class EmailConfig:
    HERMES_API_KEY = os.environ.get("HERMES_API_KEY")
    HERMES_EMAILBOT_ID = os.environ.get("HERMES_EMAILBOT_ID")
    HERMES_BASE_URL = "https://hermesbot.pythonanywhere.com"

class Config:
    FLASK_APP_NAME = "SpendBit"
    BASE_DIR = Path(__name__).parent.absolute()
    APP_DATA_DIR = BASE_DIR / "app_data"

    LOG_DIR = BASE_DIR / "logs"
    LOG_FILE = LOG_DIR / f'{FLASK_APP_NAME.lower()}.log'

    DATABASE_URI = os.environ.get("DATABASE_URI")
    SQLALCHEMY_DATABASE_URI = DATABASE_URI or \
        'sqlite:///' + os.path.join(BASE_DIR, f'{FLASK_APP_NAME.lower()}.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


LOG_FILE = Config.LOG_FILE
LOG_DIR = Config.LOG_DIR
LOG_DIR.mkdir(exist_ok=True) 

'''

README_MD = r"""# Write your Markdown here"""

FLASK_REQU = r"""
Flask
python-dotenv
Flask-SQLAlchemy
Flask-Migrate
Flask-Moment
Flask-Login
Flask-WTF
email-validator
pytz
cryptography
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
<html lang="en" class="h-100">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0">
    <title>{% block title %}{% endblock %} - ProjectTitle</title>

    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">

    <!-- Bootstrap 5 CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- Bootstrap Icons -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">

    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">

    <!-- Ionicons -->
    <link rel="stylesheet" href="https://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css">

    {% block styles %}{% endblock %}
    
    {% block head %}{% endblock %}
</head>
<body class="d-flex flex-column h-100">

    <!-- Main Content -->
    <main class="flex-grow-1 mb-5">
        <div class="container">
            <!-- Flash messages -->
            {% include "flash_msgs.html" %}

            <!-- Main content -->
            {% block content %}{% endblock %}
        </div>
    </main>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    {% block scripts %}{% endblock %}

    {{ moment.include_moment() }}
</body>
</html>

"""
FLASK_APP_INDEX_HTML = r"""

{% extends "base.html" %}

{% block title %}Home{% endblock %}

{% block content %}
{% include 'flash_msgs.html' %}

    <h1>Hello World!</h1>
{% endblock %}

"""

FLASK_EXTENSIONS_PY = r"""# app/extensions.py
# 
# Author: %s
# Created On: %s
#

"""

MIT_LICENSE = r"""MIT License

Copyright (c) 2025 Indrajit Ghosh

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

EXTENSIONS_PY = r"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask_login import LoginManager
from flask_wtf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
login_manager = LoginManager()
csrf = CSRFProtect()
"""

FLASH_MSG_HTML = r"""
<svg xmlns="http://www.w3.org/2000/svg" class="d-none">
    <symbol id="check-circle-fill" viewBox="0 0 16 16">
      <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
    </symbol>
    <symbol id="info-fill" viewBox="0 0 16 16">
      <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/>
    </symbol>
    <symbol id="exclamation-triangle-fill" viewBox="0 0 16 16">
      <path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
    </symbol>
  </svg>
  
  <!-- get_flashed_messages(with_categories=True) = [(category, message)] -->
  {% with messages = get_flashed_messages(with_categories=True) %}
      {% if messages %}
          {% for message in messages %}
              {% if 'error' in message[0] %}
                  <div class="alert alert-danger d-flex alert-dismissible fade show" role="alert">
                      <svg class="bi flex-shrink-0 me-2" role="img" aria-label="Danger:"><use xlink:href="#exclamation-triangle-fill"/></svg>
              {% elif 'success' in message[0] %}
                  <div class="alert alert-success d-flex alert-dismissible fade show" role="alert">
                      <svg class="bi flex-shrink-0 me-3" role="img" aria-label="Success:"><use xlink:href="#check-circle-fill"/></svg>
              {% elif 'warning' in message[0] %}
                  <div class="alert alert-warning d-flex alert-dismissible fade show" role="alert">
                      <svg class="bi flex-shrink-0 me-2" role="img" aria-label="Warning:"><use xlink:href="#exclamation-triangle-fill"/></svg>
              {% elif 'info' in message[0] %}
                  <div class="alert alert-info d-flex alert-dismissible fade show" role="alert">
                      <svg class="bi flex-shrink-0 me-2" role="img" aria-label="Info:"><use xlink:href="#info-fill"/></svg>
              {% else %}
                  <div class="alert alert-secondary alert-dismissible fade show" role="alert">
              {% endif %}
                  {{ message[1] }}
                  <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
              </div>
          {% endfor %}
      {% endif %}
  {% endwith %}
"""

LOGIN_HTML = r"""
{% extends 'base.html' %}

{% block title %}Login{% endblock %}

{% block content %}
{% include 'flash_msgs.html' %}
  
<h1>Log In</h1>
<h3>Welcome!</h3>

{% endblock %}

"""

FLASK_STYLE_CSS = r"""/* static/css/styles.css */

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

/* Prevent horizontal overflow globally */
body, html {
    overflow-x: hidden;
    max-width: 100vw;  /* Prevent viewport overflow */
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
  
  /* Make sure all containers don't exceed viewport */
  .container, .register-container, .card {
    max-width: 100vw;
    box-sizing: border-box;
    padding-left: 1rem;  /* or your preferred horizontal padding */
    padding-right: 1rem;
  }
  

/* To make the icons in the flash message smaller */
svg.bi {
    width: 1.5rem;
    height: 1.5rem;
}

/* Twitter X icon */
.fa.fa-twitter::before {
    display: inline-block;
    width: 1em;
    height: 1em;
    content: "";
    background-color: currentColor;
    -webkit-mask: url('data:image/svg+xml;utf8,<svg viewBox="0 -8 26 30" xmlns="http://www.w3.org/2000/svg"><g><path fill="white" d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"></path></g></svg>') no-repeat center;
    mask: url('data:image/svg+xml;utf8,<svg viewBox="0 -8 26 30" xmlns="http://www.w3.org/2000/svg"><g><path fill="white" d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"></path></g></svg>') no-repeat center;
    background-position: center 3px;
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

ERR_BASE_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{% block title %}Error{% endblock %} - SpendBit</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">
  <style>
    /* Optional: ensure min height on small screens to center content nicely */
    body, html {
      height: 100%;
    }
    main.container {
      display: flex;
      flex-direction: column;
      justify-content: center;
      min-height: 100vh;
      padding: 1rem;
    }
  </style>
</head>
<body class="bg-light">
  <main class="container text-center">
    {% block content %}{% endblock %}
  </main>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

ERR_404_HTML = r"""{% extends 'error_base.html' %}

{% block title %}Page Not Found{% endblock %}

{% block content %}
<div class="mx-auto p-5 bg-white rounded shadow" style="max-width: 420px;">
    <h1 class="display-1 text-danger fw-bold mb-4">404</h1>
    <p class="lead fs-4 mb-4">😕 Oops! The page you're looking for can't be found.</p>
    <p class="mb-4 text-muted">
        It might have been moved or deleted. Try returning to the homepage.
    </p>
    <a href="{{ url_for('main.index') }}" class="btn btn-primary btn-lg shadow">
        <i class="bi bi-house-door-fill me-2"></i>Go Home
    </a>
</div>
{% endblock %}
"""

ERR_500_HTML = r"""{% extends 'error_base.html' %}

{% block title %}Server Error{% endblock %}

{% block content %}
<div class="container text-center mt-5">
    <h1 class="display-4">500</h1>
    <p class="lead">Oops! Something went wrong on our end.</p>
    <p>We're working to fix it. Please try again later.</p>
    <a href="{{ url_for('main.index') }}" class="btn btn-danger">Go Back Home</a>
</div>
{% endblock %}
"""

ERR_400_HTML = r"""{% extends "error_base.html" %}

{% block title %}Bad Request{% endblock %}

{% block content %}
<div class="container text-center mt-5">
  <h1 class="display-3 text-warning">400</h1>
  <h2 class="mb-3">Bad Request</h2>
  <p class="lead">The request could not be understood or was missing required parameters.</p>
  <a href="{{ url_for('main.index') }}" class="btn btn-primary mt-3">Go Home</a>
</div>
{% endblock %}
"""

ERR_401_HTML = r"""{% extends 'error_base.html' %}

{% block title %}Unauthorized{% endblock %}

{% block content %}
<div class="container text-center mt-5">
    <h1 class="display-4">401</h1>
    <p class="lead">You must be logged in to access this page.</p>
    <a href="{{ url_for('auth.login') }}" class="btn btn-secondary">Login</a>
</div>
{% endblock %}
"""
ERR_403_HTML = r"""{% extends 'error_base.html' %}

{% block title %}Access Denied{% endblock %}

{% block content %}
<div class="container text-center mt-5">
    <h1 class="display-4">403</h1>
    <p class="lead">You don't have permission to access this page.</p>
    <a href="{{ url_for('main.index') }}" class="btn btn-warning">Return to Home</a>
</div>
{% endblock %}
"""

ERR_INIT_PY = r'''# app/errors/__init__.py
"""
Error handlers package for SpendBit
"""

from .handlers import register_error_handlers

__all__ = ["register_error_handlers"]
'''

HANDLERS_PY = r"""# app/errors/handlers.py
#
# Author: %s
# Created On: %s
#

from flask import render_template, jsonify, request

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Bad Request", "message": str(error)}), 400
        return render_template("errors/400.html"), 400

    @app.errorhandler(401)
    def bad_request(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Unauthorized", "message": str(error)}), 401
        return render_template("errors/401.html"), 401

    @app.errorhandler(403)
    def forbidden(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Forbidden"}), 403
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Not Found"}), 404
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Internal Server Error"}), 500
        return render_template("errors/500.html"), 500

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