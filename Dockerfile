# creation of system image
FROM python:3.13-slim AS runtimecontainer

# Create app directory and the non-root user
WORKDIR /containerApp
RUN useradd -m appuser

# Copy dependencies and installation
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy pokedex app source code into the container app
COPY --chown=appuser:appuser app/ .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Run the pokedex app via Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
