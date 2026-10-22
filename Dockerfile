# Artemis Bot 容器镜像：依赖与代码烘入镜像，config.yaml/日志运行时挂载。
# Container image for Artemis Bot: deps + code baked in, config/logs mounted at runtime.
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

# 先装依赖，利用 docker 层缓存：app/ 变动不重跑 uv sync
# Install deps first for layer caching: app/ changes don't re-run uv sync
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

COPY app ./app
COPY run.py ./

# 容器内非 root 运行
# Run as non-root inside the container
RUN useradd -r -u 10001 artemis && mkdir -p /app/data && chown artemis /app/data
USER artemis

EXPOSE 8080
CMD [".venv/bin/python", "run.py"]
