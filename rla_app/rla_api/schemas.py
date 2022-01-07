"""This file handles schemas for rla_api models."""

from typing import Optional

from pydantic import BaseModel, Field


# Text Analysis Schemas

class TextAnalysisBase(BaseModel):
    """
    Base text analysis schema.
    """
    id: int
    file_id: int
    numeric_diff: Optional[int] = Field(0, description='Task in progress...')
    percentage_diff: Optional[int] = Field(0, description='Task in progress...')


class TextAnalysisCreate(TextAnalysisBase):
    """
    Text analysis schema for creation.
    """
    pass


class TextAnalysisPatch(TextAnalysisBase):
    """
    Text analysis schema for patch.
    """
    pass


class TextAnalysis(TextAnalysisBase):
    """
    Text analysis schema.
    """
    pass

    class Config:
        orm_mode = True


# File Import Schemas

class FileImportBase(BaseModel):
    """
    Base imported file schema.
    """
    name: str
    content: str


class FileImportCreate(FileImportBase):
    """
    Imported file schema for creation.
    """
    pass


class FileImport(FileImportBase):
    """
    Imported file schema.
    """
    id: int

    class Config:
        orm_mode = True
