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
COPY todo_app /app/todo_app
COPY pyproject.toml /app
COPY poetry.toml /app

RUN poetry install

FROM base as development
ENTRYPOINT ["poetry", "run", "flask", "run"]
CMD [ "--host=0.0.0.0"]

FROM base as production
ENTRYPOINT ["poetry", "run", "gunicorn", "todo_app.app:create_app()"]
CMD ["--bind","0.0.0.0:5000"]
