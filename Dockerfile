FROM python:3.11-slim AS base

RUN apt-get update && \
    apt-get install -y --no-install-recommends libzbar0 libglib2.0-0 libsm6 libxext6 libgl1 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt/qreader-api

COPY requirements.txt .

# CPU-only PyTorch keeps the image ~2GB smaller
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

COPY app/ app/

# Pre-download YOLOv8 model weights so first request is fast
RUN python -c "from qreader import QReader; QReader(model_size='s')"

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
