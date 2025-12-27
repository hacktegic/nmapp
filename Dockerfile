FROM python:3.14-slim

WORKDIR /app

COPY dist/nmapp*.whl /app

RUN groupadd -r nmapp && useradd -d /app -r -g nmapp nmapp && \
    chown -R nmapp:nmapp /app && \
    pip install --no-cache-dir /app/nmapp*.whl

USER nmapp