FROM python:3.8-slim-buster AS base
LABEL key="Jeremy Brex todo_app"

# Add Curl as not part of slim Buster
RUN apt-get update -y && apt-get install curl -y

# Install Poetry

ENV POETRY_HOME=/poetry
ENV PATH=${POETRY_HOME}/bin:${PATH}

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

# Set the working directory.
WORKDIR /app
COPY pyproject.toml /app
COPY poetry.toml /app

# Development Docker
FROM base as development
RUN poetry install
ENTRYPOINT ["poetry", "run", "flask", "run"]
CMD [ "--host=0.0.0.0"]

# Production Docker
FROM base as production
ENV PORT=5000
ENV FLASK_APP=todo_app/app
ENV FLASK_ENV=production

# EXPOSE $PORT
RUN poetry config virtualenvs.create false --local && poetry install --no-dev
COPY todo_app /app/todo_app
COPY herokoentrypoint.sh . 
RUN chmod +x herokuentrypoint.sh
ENTRYPOINT ["./herokuentrypoint.sh"]

# Testing stage
FROM base as test

RUN poetry install

# Install Chrome
RUN curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb &&\
    apt-get install ./chrome.deb -y &&\
    rm ./chrome.deb
    
# Install Chromium WebDriver
RUN LATEST=`curl -sSL https://chromedriver.storage.googleapis.com/LATEST_RELEASE` &&\
    echo "Installing chromium webdriver version ${LATEST}" &&\
    curl -sSL https://chromedriver.storage.googleapis.com/${LATEST}/chromedriver_linux64.zip -o chromedriver_linux64.zip &&\
    apt-get install unzip -y &&\
    unzip ./chromedriver_linux64.zip

# Install Tests
COPY todo_app /app/todo_app
COPY tests /app/tests
COPY tests_int /app/tests_int
COPY tests_e2e /app/tests_e2e

ENV PATH "$PATH:/app"

ENTRYPOINT ["poetry", "run", "pytest"]
