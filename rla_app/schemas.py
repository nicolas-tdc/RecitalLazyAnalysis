from typing import Optional

from pydantic import BaseModel, Field


# Text Analysis Schemas

class TextAnalysisBase(BaseModel):
    file_id: int
    letter_count: Optional[str] = Field(None, description='Task in progress...')
    politeness_level: Optional[int] = Field(None, description='Task in progress...')


class TextAnalysisCreate(TextAnalysisBase):
    pass


class TextAnalysis(TextAnalysisBase):
    id: int

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
