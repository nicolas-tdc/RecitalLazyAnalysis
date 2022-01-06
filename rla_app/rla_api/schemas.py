"""This file handles schemas for rla_api models."""

from typing import Optional

from pydantic import BaseModel, Field


# Text Analysis Schemas

class TextAnalysisBase(BaseModel):
    id: int
    file_id: int
    numeric_diff: Optional[int] = Field(0, description='Task in progress...')
    percentage_diff: Optional[int] = Field(0, description='Task in progress...')


class TextAnalysisCreate(TextAnalysisBase):
    pass


class TextAnalysisPatch(TextAnalysisBase):
    pass


class TextAnalysis(TextAnalysisBase):
    pass

    class Config:
        orm_mode = True


# File Import Schemas

class FileImportBase(BaseModel):
    name: str
    content: str


class FileImportCreate(FileImportBase):
    pass


class FileImport(FileImportBase):
    id: int

    class Config:
        orm_mode = True
