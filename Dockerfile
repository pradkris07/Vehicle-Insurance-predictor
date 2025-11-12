# Use an official Python 3.10 slim image
FROM python:3.10-slim-buster

# Install curl (required to install uv)
RUN apt-get update && apt-get install -y curl && apt-get clean

# Install uv globally
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy the project files
COPY . /app

# Install dependencies using uv (reads pyproject.toml and uv.lock)
RUN uv sync --frozen

# Expose FastAPI port
EXPOSE 5000

# Command to run the FastAPI app
# You can change "app.py" to your entrypoint (e.g., "main.py" or "src/app/main.py")
CMD ["uv", "run", "python", "app.py"]
