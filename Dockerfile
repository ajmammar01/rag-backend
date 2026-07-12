# 1. Use an official, lightweight Python base image
FROM python:3.12-slim

# 2. Install basic tools needed by the operating system
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 3. Install your fast package manager (uv) globally inside the container
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 4. Set the internal working directory where our app will live
WORKDIR /app

# 5. Copy your dependency manifests first (for fast caching)
COPY pyproject.toml uv.lock ./

# 6. Install all dependencies inside the container
RUN uv sync --frozen --no-install-project

# 7. Copy your actual code over
COPY app/ ./app/

# 8. Create a blank folder where your vector database will persist its data
RUN mkdir -p /app/chroma_db

# 9. Tell the container to expose the network port FastAPI uses
EXPOSE 8000

# 10. The command that boots up your server when the container starts
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]