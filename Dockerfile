# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and source files first
COPY requirements.txt pyproject.toml setup.py README.md ./
COPY src/ ./src/

# Install Python dependencies
RUN pip install -e .

# Copy remaining application files
COPY . .

# Create non-root user for security
RUN groupadd -r budgetuser && useradd -r -g budgetuser budgetuser
RUN chown -R budgetuser:budgetuser /app
USER budgetuser

# Create volume for data persistence
VOLUME ["/app/data"]

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import budget_manager; print('OK')" || exit 1

# Default command
ENTRYPOINT ["budget"]
CMD ["--help"]