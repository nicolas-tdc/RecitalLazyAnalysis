"""This file handles CRUD for rla_api models."""

from sqlalchemy.orm import Session

from rla_app.rla_api import models, schemas


def rla_get_file(db: Session, file_id: int):
    """
    :param db:
    :param file_id:
    :return: Single imported file.
    """

    return db.query(models.FileImport).filter(models.FileImport.id == file_id).first()


def rla_get_files(db: Session, skip: int = 0, limit: int = 100):
    """
    :param db:
    :param skip:
    :param limit:
    :return: List of imported files.
    """
    return db.query(models.FileImport).offset(skip).limit(limit).all()


def rla_create_file(db: Session, file: schemas.FileImportCreate):
    """
    :param db:
    :param file:
    :return: Imported file creation.
    """
    db_file = models.FileImport(name=file.name, content=file.content)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def rla_get_text_analysis(db: Session, analysis_id: int):
    """
    :param db:
    :param analysis_id:
    :return: Single text analysis.
    """
    return db.query(models.TextAnalysis).filter(models.TextAnalysis.id == analysis_id).first()


def rla_get_text_analyses(db: Session, skip: int = 0, limit: int = 100):
    """
    :param db:
    :param skip:
    :param limit:
    :return: List of text analyses.
    """
    return db.query(models.TextAnalysis).offset(skip).limit(limit).all()


def rla_create_text_analysis(db: Session, text_analysis: schemas.TextAnalysisCreate):
    """
    :param db:
    :param text_analysis:
    :return: Created text analysis.
    """
    db_analysis = models.TextAnalysis(file_id=text_analysis.file_id)
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return db_analysis


def rla_patch_text_analysis(db: Session, analysis: schemas.TextAnalysisPatch):
    """
    :param db:
    :param analysis:
    :return: Patched text analysis.
    """
    # Get the existing data.
    db_analysis = db.query(models.TextAnalysis).filter(models.TextAnalysis.id == analysis.id).one_or_none()
    if db_analysis is None:
        return None

    # Update model class variable from requested fields.
    for var, value in vars(analysis).items():
        setattr(db_analysis, var, value) if value else None

    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return db_analysis
