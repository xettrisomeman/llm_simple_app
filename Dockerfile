FROM python:3.11.9-bookworm

WORKDIR /app

COPY . /app

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r req.txt

RUN chown -R 1001:1001 /app/components/app_interface/config.yaml /app/.streamlit/config.toml

