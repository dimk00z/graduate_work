import logging
import os
from functools import lru_cache

import ffmpeg

from core.constants import aspect_size
from db.postgres.models import Convertation
from models.convertation import ConvertOut, ConvertVideoCreate, ConvertVideoIn
from services.db import create_convertation


class ConvertationService:
    def __init__(self):
        pass

    @staticmethod
    async def convert(convertation: ConvertVideoIn):
        res = False
        try:
            new_convert = ConvertVideoCreate(**convertation.dict())
            stream = ffmpeg.input(new_convert.source_path)
            audio = stream.audio
            destination = os.path.join(
                new_convert.destination_path,
                f"{os.path.basename(new_convert.source_path).split('.')[0]}_{new_convert.resolution}.avi",
            )
            if new_convert.resolution:
                if new_convert.resolution in aspect_size:
                    logging.debug(new_convert.resolution)
                    stream = ffmpeg.filter(
                        stream,
                        "scale",
                        size=aspect_size.get(new_convert.resolution),
                        force_original_aspect_ratio="increase",
                    )
            if new_convert.fps:
                stream = ffmpeg.filter(stream, "fps", fps=new_convert.fps, round="up")
            if new_convert.codec_name:
                stream = ffmpeg.output(
                    stream, destination, format=new_convert.codec_name
                ).overwrite_output()
            else:
                stream = ffmpeg.output(audio, stream,  destination).overwrite_output()
            proc = ffmpeg.run(stream)
            if proc:
                res = True

            convertation_to_create: Convertation = Convertation(**new_convert.dict())
            convertation = await create_convertation(
                convertation_to_create=convertation_to_create
            )
            return ConvertOut(result=res)
        except Exception as e:
            logging.exception(e)
            return ConvertOut(result=res)


@lru_cache()
def get_convertation_service() -> ConvertationService:
    return ConvertationService()
