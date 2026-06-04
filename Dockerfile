FROM python:3.14.4-alpine3.23

WORKDIR /app

RUN pip install uv==0.8.14

COPY pyproject.toml .
COPY uv.lock .
COPY README.md .
COPY src ./src

RUN uv sync --frozen

ENTRYPOINT [ "uv", "run", "pool-tracker-server" ]