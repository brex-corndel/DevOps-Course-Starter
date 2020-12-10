FROM python:3.8-slim-buster
LABEL key="Jeremy Brex todo_app"

# Add to the PATH for Poetry
ENV PATH="/root/.local/bin:${PATH}"

# Build up the Environment
# RUN apt update && apt upgrade

# Add Curl as not part of slim Buster

RUN apt-get update && apt-get install curl -y

# Add Flask and gunicorn

RUN pip install -U Flask
RUN pip install gunicorn

# Install Poetry

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

ENV PATH="/root/.poetry/bin:$PATH"

RUN pip install python-dotenv

# declare any ports to be used use -p in run

EXPOSE 5000/tcp

# Set the working directory.
WORKDIR /usr/src/app
COPY . .

# Run the todo_app App
# ENTRYPOINT source $HOME/.poetry/env
# CMD poetry run gunicorn
CMD poetry run flask run