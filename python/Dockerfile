from python:3.11.8-slim

MAINTAINER benjmain@datavaluepeople.com

# Disable linux frontend.
ENV DEBIAN_FRONTEND noninteractive

# Set environment variables to ensure Python runs in unbuffered mode,
# recommended for Docker.
ENV PYTHONUNBUFFERED 1 \
    PYTHONDONTWRITEBYTECODE 1

# Install system dependencies, and clean up to reduce image size.
RUN apt-get update \
    && apt-get -yq dist-upgrade \
    && apt-get install -yq --no-install-recommends \
    build-essential \
    libpq-dev \
    pkg-config \
    unixodbc-dev \
    libicu-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container (convention).
WORKDIR /app

# Script for docker entrypoint.
COPY ./.docker-entrypoint.sh /app/.docker-entrypoint.sh
RUN chmod -R +x .docker-entrypoint.sh

# ARG PROJECT - used to parameterise the Dockerfile to build a serparate image per project.
ARG PROJECT=example_project_1

# Install Python dependencies.
COPY pyproject.toml Makefile /app/
COPY projects/${PROJECT}/requirements.txt /app/projects/${PROJECT}/requirements.txt

# Create a new requirements file without `file:libs/` lines and save those lines to a file.
RUN sed '/file:libs\//d' projects/${PROJECT}/requirements.txt > projects/${PROJECT}/requirements_no_local_libs.txt \
    && grep 'file:libs/' projects/${PROJECT}/requirements.txt > projects/${PROJECT}/requirements_local_libs.txt

# Then install the Python dependencies, to levarage Docker's caching mechanism.
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r projects/${PROJECT}/requirements_no_local_libs.txt

# Copy all python code:
#   - Do this after install to leverage Docker's caching mechanism.
#   - Copying all the code simplifies ensuring that the project has the code
#   for al local monorepo dependencies it needs.
COPY . /app

# Now install the local monorepo libaries.
RUN pip install -r projects/${PROJECT}/requirements_local_libs.txt

# Install the project as a package.
RUN pip install -e projects/${PROJECT}/.

ENTRYPOINT ["/app/.docker-entrypoint.sh"]
