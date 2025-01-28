FROM ubuntu:24.04

RUN apt update && \
    apt upgrade -y

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN useradd -ms /bin/bash user && \
    usermod -a -G dialout user
USER user
WORKDIR /home/user/app

# RUN --mount=type=bind,source=uv.lock,target=uv.lock \
#     --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
#     uv sync --frozen --no-install-project --no-dev
COPY uv.lock .
COPY pyproject.toml .
RUN uv sync --frozen --no-install-project --no-dev

COPY us2000c_prometheus_exporter.py .

ENTRYPOINT []
CMD ["uv", "run", "us2000c_prometheus_exporter.py"]
