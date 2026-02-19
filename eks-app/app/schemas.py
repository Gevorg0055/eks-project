from pydantic import BaseModel
from datetime import datetime

class FileResponse(BaseModel):
    id: int
    filename: str
    size: int
    created_at: datetime
    download_url: str

    class Config:
        from_attributes = True
