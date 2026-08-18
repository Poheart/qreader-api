from pydantic import BaseModel


class BarcodeScanResult(BaseModel):
    Successful: bool
    BarcodeType: str | None = None
    RawText: str | None = None


class BarcodeAdvancedResultItem(BaseModel):
    RawText: str
    BarcodeType: str


class BarcodeAdvancedScanResult(BaseModel):
    Successful: bool
    ResultBarcodes: list[BarcodeAdvancedResultItem] = []
    BarcodeCount: int = 0
    ErrorMessage: str | None = None
