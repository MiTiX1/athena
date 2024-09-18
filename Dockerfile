FROM python:3.10.12-slim-buster as builder

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_NO_INTERACTION=1

# to run poetry directly as soon as it's installed
ENV PATH="$POETRY_HOME/bin:$PATH"

# install poetry
RUN apt-get update \
    && apt-get install -y curl \
    && curl -sSL https://install.python-poetry.org | python3 - --version 1.8.1

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock ./

# this will create the folder /app/.venv (might need adjustment depending on which poetry version you are using)
RUN poetry lock --no-update
RUN poetry install --only main --no-root --no-ansi

# --------------------------------------------------------------

FROM python:3.10.12-slim-buster as runtime

WORKDIR /app

ENV PATH=/app/.venv/bin:$PATH

#Install chrome
RUN apt-get update
RUN apt-get install -y wget
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

COPY --from=builder /app/.venv .venv

RUN . .venv/bin/activate

COPY . /app
#Because it is running in Cloud run Jobs, we just need to launch main.py entrypoint.
CMD . .venv/bin/activate && python main.py