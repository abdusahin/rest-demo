FROM python:3.11-slim-buster


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev \
    python3.11 \
    build-essential

# configure python3.11 as the default python
RUN ln -sf /usr/bin/python3.11 /usr/bin/python
# Install pip using Python's ensurepip
RUN python -m ensurepip --upgrade && \
    python -m pip install --upgrade pip  && \
    python -m pip install pip-tools  alembic

# Set pip3.11 as the default pip
RUN ln -sf /usr/bin/pip3.11 /usr/bin/pip

WORKDIR /app
COPY . .

# generate requirements.txt file
RUN pip-compile -o requirements.txt pyproject.toml

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt



