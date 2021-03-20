# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.tempalate` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. 

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.


## Running in Docker

The code has been modified to run within Docker.

Use the following to builld and run the image. There are 2 versions
1 - Development that uses Flask only 
2 - Production that uses Gunicorn WSGI to scale

These can be run as follows

* Developmemt
```bash
docker build --target development --tag todo_app .
docker run --env-file .env -p 5000:5000 --mount type=bind,source="$(pwd)"/todo_app,target=/app/todo_app todo_app
```

* Production
```bash
docker build --target production --tag todo_app .
docker run --env-file .env -p 5000:5000 todo_app
```
## Operations

The backend is now in Trello. The local .env file contains the variables. These are not shared in Github

Items are marked To Do, Doing and Done. The 'complete action' button has been added to move any item to Done *


* Future revision should limit this to To Do and Doing Only.

## Working with pytest

poetry install pytest

To run a test session for unit testing :-

poetry run pytest

To run end to end tests 

ensure gechodriver is installed in the root directory and included in the path
cd tests_e2e
poetry run pytest

## Working with GIT

git add --all

git commit -m "<add change details>"
  
git push origin module-2

## Working with Selenium

poetry add selenium

selenium --version

## Working with Docker

## Basic Docker Connands

# Testing With Docker
$ docker build --target test --tag my-test-image .
# Run Unit Tests
$ docker run my-test-image tests
# Run Integration tests
docker run my-test-image tests_int
# Run end to end tests
$ docker run my-test-image tests_e2e


  
  
