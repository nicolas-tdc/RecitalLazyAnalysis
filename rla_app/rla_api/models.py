"""This file handles models for rla_api."""

from sqlalchemy import Column, Integer, String

from rla_api.database import Base


class FileImport(Base):
    __tablename__ = "file_import"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    content = Column(String, index=True)


class TextAnalysis(Base):
    __tablename__ = "text_analysis"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, index=True)
    numeric_diff = Column(Integer, index=True)
    percentage_diff = Column(Integer, index=True)
