from typing import List

from fastapi import Depends, FastAPI, HTTPException, File, UploadFile
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from PIL import Image
from pytesseract import image_to_string, pytesseract

import crud
import models
import schemas

from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def rla_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/files/")
async def rla_create_file(db: Session = Depends(rla_get_db), files: List[UploadFile] = File(...)):
    treated_data = []

    for file in files:
        file_crud_data = schemas.FileImportCreate
        if file.content_type.startswith('image/'):
            # Needed in Windows 10 to find tesseract app
            pytesseract.tesseract_cmd = r'C:/OCR/tesseract.exe'
            image_file = Image.open(file.file)
            file_crud_data.content = image_to_string(image_file)
        elif file.content_type.startswith('text/'):
            file_crud_data.content = await file.read()
        else:
            return {'File type not supported'}

        file_crud_data.name = file.filename
        file_import = crud.rla_create_file(db, file_crud_data)
        # Create Text Analysis
        analysis_crud_data = schemas.TextAnalysisCreate
        analysis_crud_data.file_id = file_import.id
        text_analysis = crud.rla_create_text_analysis(db, analysis_crud_data)
        # Launch Celery tasks and patch corresponding fields when task is done
        treated_data.append({
            'file_name': file_import.name, 'analysis_path': '/analysis/' + str(text_analysis.id)
        })

    return treated_data


@app.get("/files/", response_model=List[schemas.FileImport])
def rla_read_files(skip: int = 0, limit: int = 100, db: Session = Depends(rla_get_db)):
    files = crud.rla_get_files(db, skip=skip, limit=limit)
    return files


@app.get("/files/{file_id}", response_model=schemas.FileImport)
def rla_read_file(file_id: int, db: Session = Depends(rla_get_db)):
    db_file = crud.rla_get_file(db, file_id=file_id)
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return db_file


@app.get("/analyses/", response_model=List[schemas.TextAnalysis])
def rla_read_analyses(skip: int = 0, limit: int = 100, db: Session = Depends(rla_get_db)):
    analyses = crud.rla_get_text_analyses(db, skip=skip, limit=limit)
    return analyses


@app.get("/analysis/{analysis_id}", response_model=schemas.TextAnalysis)
def rla_read_analysis(analysis_id: int, db: Session = Depends(rla_get_db)):
    db_analysis = crud.rla_get_text_analysis(db, analysis_id=analysis_id)
    if db_analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return db_analysis


@app.get("/analysis/", response_class=HTMLResponse)
async def rla_upload_file_for_analysis():
    return """
        <body>
        <form action="/files/" method="post" enctype="multipart/form-data">
        <input name="files" type="file" multiple>
        <input type="submit">
        </form>
        </body>
    """
