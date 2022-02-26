import os
from functools import lru_cache

import ffmpeg
from db.postgres.models import Convertation
from models.convertation import ConvertOut, ConvertVideoCreate, ConvertVideoIn
from services.db import create_convertation


class ConvertationService:
    def __init__(self):
        pass

    @staticmethod
    async def convert(convertation: ConvertVideoIn):
        res = False
        new_convert = ConvertVideoCreate(**convertation.dict())
        stream = ffmpeg.input(new_convert.source_path)
        destination = os.path.join(
            new_convert.destination_path,
            f"{os.path.basename(new_convert.source_path).split('.')[0]}_{new_convert.resolution}.avi",
        )
        if new_convert.resolution:
            stream.filter(
                "scale",
                size=new_convert.resolution,
                force_original_aspect_ratio="increase",
            )
        if new_convert.fps:
            stream = ffmpeg.filter(stream, "fps", fps=new_convert.fps, round="up")
        if new_convert.codec_name:
            stream = ffmpeg.output(
                stream, destination, format=new_convert.codec_name
            ).overwrite_output()
        else:
            stream = ffmpeg.output(stream, destination).overwrite_output()
        proc = ffmpeg.run(stream)
        if proc:
            res = True

        convertation_to_create: Convertation = Convertation(**new_convert.dict())
        convertation = await create_convertation(
            convertation_to_create=convertation_to_create
        )
        return ConvertOut(result=res)


@lru_cache()
def get_convertation_service() -> ConvertationService:
    return ConvertationService()
