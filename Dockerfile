FROM python:3.10-slim

## Esential evvironment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Work directory insiede the docker container
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y \
    curl \
    wget \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# copy the source code to the work directory
COPY . .

# install the dependencies
RUN pip install --no-cache-dir -e .
# Expose the port

# Backend
EXPOSE 8000 
# Frontend
EXPOSE 8501 
# Run the backend
CMD ["uvicorn", "app.backend.api:app", "--host", "0.0.0.0", "--port", "8000"]