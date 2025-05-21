ARG BUILD_FROM
FROM $BUILD_FROM

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Setup Python environment
ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED 1
ARG PYTHON_VERSION=3.11

RUN apk add --no-cache \
    build-base \
    python${PYTHON_VERSION} \
    py${PYTHON_VERSION}-pip \
    libffi-dev # Notwendig für discord.py cryptography

# Install application requirements
RUN pip install --no-cache-dir -r /requirements.txt

CMD [ "python3", "/app/main.py" ]
