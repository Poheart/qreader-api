import asyncio
import os

import cv2
import numpy as np
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File

from app.auth import check_api_key
from app.models import (
    BarcodeAdvancedResultItem,
    BarcodeAdvancedScanResult,
    BarcodeScanResult,
)

router = APIRouter()

MAX_UPLOAD_SIZE_MB = int(os.environ.get("MAX_UPLOAD_SIZE_MB", "5"))


def _decode_image(data: bytes) -> np.ndarray:
    arr = np.frombuffer(data, dtype=np.uint8)
    try:
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    except cv2.error:
        raise HTTPException(status_code=400, detail="Could not decode image")
    if img is None:
        raise HTTPException(status_code=400, detail="Could not decode image")
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


async def _read_and_validate(image_file: UploadFile) -> bytes:
    data = await image_file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty file provided")
    if len(data) > MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail=f"File size exceeds {MAX_UPLOAD_SIZE_MB}MB limit",
        )
    return data


@router.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@router.post(
    "/scan",
    response_model=BarcodeScanResult,
    dependencies=[Depends(check_api_key)],
)
async def scan_image(request: Request, imageFile: UploadFile = File(...)) -> BarcodeScanResult:
    data = await _read_and_validate(imageFile)
    image = _decode_image(data)
    qreader = request.app.state.qreader
    results = await asyncio.to_thread(qreader.detect_and_decode, image)

    for text in results:
        if text is not None:
            return BarcodeScanResult(Successful=True, BarcodeType="QR_CODE", RawText=text)

    return BarcodeScanResult(Successful=False)


@router.post(
    "/scan/advanced",
    response_model=BarcodeAdvancedScanResult,
    dependencies=[Depends(check_api_key)],
)
async def scan_image_advanced(request: Request, imageFile: UploadFile = File(...)) -> BarcodeAdvancedScanResult:
    data = await _read_and_validate(imageFile)
    image = _decode_image(data)
    qreader = request.app.state.qreader

    try:
        results = await asyncio.to_thread(qreader.detect_and_decode, image)
    except Exception as e:
        return BarcodeAdvancedScanResult(
            Successful=False, ErrorMessage=str(e)
        )

    barcodes = [
        BarcodeAdvancedResultItem(RawText=text, BarcodeType="QR_CODE")
        for text in results
        if text is not None
    ]

    return BarcodeAdvancedScanResult(
        Successful=True,
        ResultBarcodes=barcodes,
        BarcodeCount=len(barcodes),
    )
