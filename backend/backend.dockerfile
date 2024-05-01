FROM python:3.12.1

WORKDIR /app/

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python
RUN cd /usr/local/bin
RUN ln -s /opt/poetry/bin/poetry
RUN pip install poetry



# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./app/pyproject.toml ./app/poetry.lock* /app/

RUN poetry config virtualenvs.create false

RUN poetry install --no-root

COPY ./app /app
