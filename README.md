# qreader-api

QR code scanning API powered by [QReader](https://github.com/Eric-Canas/QReader), packaged as a Docker image.

## Quick Start with Docker

You only need Docker Desktop (or Docker Engine) installed. No Python installation is required.

### 1. Download and start the API

```bash
docker pull ghcr.io/Poheart/qreader-api:latest
docker run -d \
  --name qreader-api \
  --restart unless-stopped \
  -p 8000:8000 \
  ghcr.io/Poheart/qreader-api:latest
```

The first startup can take up to a minute while the QR model loads. Check that it is ready:

```bash
curl http://localhost:8000/health
```

The API is available at `http://localhost:8000`. Open `http://localhost:8000/docs` for interactive API documentation.

### 2. Scan an image

Replace `qr.png` with the path to an image containing a QR code:

```bash
curl -X POST \
  -F "imageFile=@qr.png" \
  http://localhost:8000/scan
```

Example response:

```json
{
  "Successful": true,
  "BarcodeType": "QR_CODE",
  "RawText": "https://example.com"
}
```

To return every QR code found in the image, use `/scan/advanced`:

```bash
curl -X POST \
  -F "imageFile=@qr.png" \
  http://localhost:8000/scan/advanced
```

### 3. Stop or remove the container

```bash
docker stop qreader-api
docker rm qreader-api
```

View startup and request logs with:

```bash
docker logs -f qreader-api
```

## Quick Start with Docker Compose

To build the image locally instead of pulling it from GHCR:

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`.

## API Endpoints

### `POST /scan`

Simple scan — returns the first QR code found. Send the image as the `imageFile` multipart form field.

### `POST /scan/advanced`

Advanced scan — returns all QR codes found in the image.

```json
{
  "Successful": true,
  "ResultBarcodes": [
    { "RawText": "https://example.com", "BarcodeType": "QR_CODE" }
  ],
  "BarcodeCount": 1,
  "ErrorMessage": null
}
```

### `GET /health`

```bash
curl http://localhost:8000/health
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `API_KEY` | *(unset)* | If set, requires `Apikey` header on scan endpoints |
| `MODEL_SIZE` | `s` | QReader model size: `n`, `s`, `m`, or `l` |
| `MAX_UPLOAD_SIZE_MB` | `5` | Maximum upload file size in MB |

Pass environment variables when starting the published image:

```bash
docker run -d \
  --name qreader-api \
  -p 8000:8000 \
  -e MODEL_SIZE=s \
  -e MAX_UPLOAD_SIZE_MB=10 \
  ghcr.io/Poheart/qreader-api:latest
```

## Docker

### Build and run directly

```bash
docker build -t qreader-api .
docker run -p 8000:8000 qreader-api
```

### With authentication

```bash
docker run -p 8000:8000 -e API_KEY=your-secret-key qreader-api
```

Then include the `Apikey` header in requests:

```bash
curl -X POST -H "Apikey: your-secret-key" -F "imageFile=@qr.png" http://localhost:8000/scan/advanced
```

When using the published image, replace `qreader-api` in the command with `ghcr.io/Poheart/qreader-api:latest`.

## GitHub Container Registry

Images are published automatically on pushes to `main` (tagged `latest`) and on version tags (`v*`).

```bash
docker pull ghcr.io/Poheart/qreader-api:latest
```
