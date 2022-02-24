from typing import List
from uuid import UUID

from pydantic import BaseModel


class Film(BaseModel):
    "Event for sending notification"
    film_id: UUID
    file_name: str
    source_file_path: str
    resolutions: List[str]


class Films(BaseModel):
    films: List[Film]


class FilmFile(BaseModel):
    resolution: str
    file_name: str


class FilmFiles(BaseModel):
    film_id: UUID
    film_files: List[FilmFile]
