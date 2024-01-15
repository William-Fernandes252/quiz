ARG pythonVersion=3.12.1-slim-bullseye

# define an alias for the specfic python version used in this file.
FROM python:${pythonVersion} as python

ARG poetryVersion=1.5.0
ARG appHome=/app
ARG buildEnv=local

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${buildEnv}
ENV POETRY_VERSION ${poetryVersion}

# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    # dependencies for building Python packages
    build-essential \
    # psycopg dependencies
    libpq-dev \
    # Translations dependencies
    gettext \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Install dependency manager
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
COPY poetry.lock pyproject.toml ${appHome}/

# Set the working directory
WORKDIR ${appHome}

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install $(test $BUILD_ENV = production && echo "--only main") --no-interaction --no-ansi

COPY ./docker/${BUILD_ENV}/django/entrypoint.sh /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./docker/${buildEnv}/django/start.sh /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# Copy application code to WORKDIR
COPY . ${appHome}

ENTRYPOINT ["/entrypoint"]
