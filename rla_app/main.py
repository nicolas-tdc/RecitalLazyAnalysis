"""This file handles rla_api views."""

from typing import List

from fastapi import Depends, FastAPI, HTTPException, File, UploadFile
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session
from rla_app.rla_api.database import SessionLocal, engine

from PIL import Image
from pytesseract import image_to_string, pytesseract
import PyPDF2

from rla_app import tasks
from rla_app.rla_api import crud, models, schemas


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def rla_get_db():
    """
    Database session handling.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/files/")
async def rla_create_file(db: Session = Depends(rla_get_db), files: List[UploadFile] = File(...)):
    """
    :param db:
    :param files:
    :return: API View for text analysis creation after file upload.
    """

    treated_data = []

    for file in files:
        file_crud_data = schemas.FileImportCreate

        # Read text from uploaded file depending on mimetype.
        if file.content_type.startswith('image/'):
            # Needed in Windows 10 to find tesseract app.
            pytesseract.tesseract_cmd = r'C:/OCR/tesseract.exe'
            image_file = Image.open(file.file)
            file_crud_data.content = image_to_string(image_file)
        elif file.content_type.startswith('text/'):
            file_crud_data.content = await file.read()
        elif file.content_type == 'application/pdf':
            pdf = PyPDF2.PdfFileReader(file.file)
            file_crud_data.content = ''
            for page in pdf.pages:
                file_crud_data.content += page.extractText() + ' '
        else:
            return {'File type not supported'}

        file_crud_data.name = file.filename
        file_import = crud.rla_create_file(db, file_crud_data)
        # Create Text Analysis.
        analysis_crud_data = schemas.TextAnalysisCreate
        analysis_crud_data.file_id = file_import.id
        text_analysis = crud.rla_create_text_analysis(db, analysis_crud_data)

        zipf_task = tasks.rla_zipf_task(db, file_import.content, text_analysis.id)
        treated_data.append({
            'file_name': file_import.name, 'analysis_path': '/analysis/' + str(text_analysis.id),
        })

    return treated_data


@app.get("/files/", response_model=List[schemas.FileImport])
def rla_read_files(skip: int = 0, limit: int = 100, db: Session = Depends(rla_get_db)):
    """
    :param skip:
    :param limit:
    :param db:
    :return: API View for uploaded files list.
    """

    files = crud.rla_get_files(db, skip=skip, limit=limit)
    return files


@app.get("/files/{file_id}", response_model=schemas.FileImport)
def rla_read_file(file_id: int, db: Session = Depends(rla_get_db)):
    """
    :param file_id:
    :param db:
    :return: API View for single uploaded file.
    """

    db_file = crud.rla_get_file(db, file_id=file_id)
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return db_file


@app.get("/analyses/", response_model=List[schemas.TextAnalysis])
def rla_read_analyses(skip: int = 0, limit: int = 100, db: Session = Depends(rla_get_db)):
    """
    :param skip:
    :param limit:
    :param db:
    :return: API View for text analyses list.
    """

    analyses = crud.rla_get_text_analyses(db, skip=skip, limit=limit)
    return analyses


@app.get("/analysis/{analysis_id}", response_model=schemas.TextAnalysis)
def rla_read_analysis(analysis_id: int, db: Session = Depends(rla_get_db)):
    """
    :param analysis_id:
    :param db:
    :return: API View for single text analysis.
    """

    db_analysis = crud.rla_get_text_analysis(db, analysis_id=analysis_id)
    if db_analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return db_analysis


@app.get("/analysis/", response_class=HTMLResponse)
async def rla_upload_file_for_analysis():
    """
    :return: API View for file upload form.
    """

    return """
        <body>
        <form action="/files/" method="post" enctype="multipart/form-data">
        <input name="files" type="file" multiple>
        <input type="submit">
        </form>
        </body>
    """
