# qreader-api

QR code scanning API powered by [QReader](https://github.com/Eric-Canas/QReader), packaged as a Docker image.

## Quick Start

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

## API Endpoints

### `POST /scan`

Simple scan — returns the first QR code found.

```bash
curl -X POST -F "imageFile=@qr.png" http://localhost:8000/scan
```

```json
{
  "Successful": true,
  "BarcodeType": "QR_CODE",
  "RawText": "https://example.com"
}
```

### `POST /scan/advanced`

Advanced scan — returns all QR codes found in the image.

```bash
curl -X POST -F "imageFile=@qr.png" http://localhost:8000/scan/advanced
```

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

## GitHub Container Registry

Images are published automatically on pushes to `main` (tagged `latest`) and on version tags (`v*`).

```bash
docker pull ghcr.io/Poheart/qreader-api:latest
```
