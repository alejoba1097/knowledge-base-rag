FROM pytorch/pytorch:2.3.1-cuda12.1-cudnn8-runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System deps for OCR and PDF rendering
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        tesseract-ocr \
        libtesseract-dev \
        poppler-utils \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/backend

# Install Python dependencies first to leverage Docker layer caching
COPY backend/pyproject.toml ./pyproject.toml
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir pip-tools \
    && pip-compile pyproject.toml --output-file requirements.txt \
    && pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cu121 -r requirements.txt \
    && pip uninstall -y pip-tools

# Copy application code
COPY backend/src ./src

ENV PYTHONPATH=/app/backend/src

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
