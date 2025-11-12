# Use newer Debian base to avoid apt issues
FROM python:3.10-slim-bookworm

# Install curl
RUN apt-get update && apt-get install -y curl && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies using uv
RUN uv sync --frozen

# Expose FastAPI port
EXPOSE 5000

# Run the FastAPI app
#CMD ["uv", "run", "python", "app.py"]
CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
