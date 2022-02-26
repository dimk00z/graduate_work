from lib2to3.pytree import convert
from typing import List
from uuid import UUID

from pydantic import BaseModel


class Film(BaseModel):
    "Event for sending notification"
    film_id: UUID
    resolutions: List[str]
    file_name: str
    source_path: str
    destination_path: str


class Films(BaseModel):
    films: List[Film]


class FilmFile(BaseModel):
    resolution: str
    destination_path: str
    succeded: bool


class TransformResult(BaseModel):
    film_id: UUID
    film_files: List[FilmFile]


class TransformResults(BaseModel):
    results: List[TransformResult]
