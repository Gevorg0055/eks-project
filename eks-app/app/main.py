from fastapi import FastAPI, UploadFile, File as FastFile, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from .database import Base, engine
from .models import File
from .schemas import FileResponse
from .deps import get_db
from . import s3

app = FastAPI(title="Cloud EKS Practice App")

# Create tables
Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload", response_model=FileResponse)
def upload_file(
    file: UploadFile = FastFile(...),
    db: Session = Depends(get_db)
):
    unique_id = str(uuid.uuid4())
    s3_key = f"uploads/{unique_id}_{file.filename}"

    try:
        s3.upload_file(file.file, s3_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    file.file.seek(0)
    content = file.file.read()
    size = len(content)

    db_file = File(
        filename=file.filename,
        s3_key=s3_key,
        size=size
    )

    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    download_url = s3.generate_presigned_url(s3_key)

    return FileResponse(
        id=db_file.id,
        filename=db_file.filename,
        size=db_file.size,
        created_at=db_file.created_at,
        download_url=download_url
    )


@app.get("/files/{file_id}", response_model=FileResponse)
def get_file(file_id: int, db: Session = Depends(get_db)):
    file_record = db.query(File).filter(File.id == file_id).first()

    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")

    download_url = s3.generate_presigned_url(file_record.s3_key)

    return FileResponse(
        id=file_record.id,
        filename=file_record.filename,
        size=file_record.size,
        created_at=file_record.created_at,
        download_url=download_url
    )


@app.get("/files")
def list_files(db: Session = Depends(get_db)):
    return db.query(File).all()
