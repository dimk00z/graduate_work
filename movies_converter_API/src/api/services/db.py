from db.postgres.models import Convertation
from tortoise.transactions import in_transaction


async def create_convertation(convertation_to_create: Convertation) -> Convertation:
    async with in_transaction() as tr:
        res_ = await Convertation.create(
            id=convertation_to_create.id,
            source_path=convertation_to_create.source_path,
            destination_path=convertation_to_create.destination_path,
            resolution=convertation_to_create.resolution,
            codec_name=convertation_to_create.codec_name,
            display_aspect_ratio=convertation_to_create.display_aspect_ratio,
            fps=convertation_to_create.fps,
            created_at=convertation_to_create.created_at,
            status=convertation_to_create.status,
            using_db=tr,
        )
        return res_
