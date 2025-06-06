# Dockerfile for Word Split API Service

FROM python:3.9-slim

WORKDIR /app

# 安装 curl（带重试和 fix-missing）
RUN set -eux; \
    for i in 1 2 3; do \
      apt-get update && \
      apt-get install -y --no-install-recommends curl --fix-missing && \
      break; \
    done; \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 暴露端口
EXPOSE 8000

# 启动服务
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
