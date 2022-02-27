from fastapi import APIRouter, Depends
from models.convertation import ConvertOut, ConvertVideoIn
from services.convertation import ConvertationService, get_convertation_service

router = APIRouter()


@router.post("/convert", response_model=ConvertOut)
async def create_convert(
    convertation: ConvertVideoIn,
    convert_service: ConvertationService = Depends(get_convertation_service),
) -> ConvertOut:
    return await convert_service.convert(
        convertation,
    )
