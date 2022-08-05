from dataclasses import dataclass
from http import HTTPStatus
from fastapi import HTTPException, APIRouter
from twijournal.entities.user.schema import TokenUserSchema
from twijournal.infrastructure.jwt_generator import generate_jwt

router = APIRouter()


@router.post(
    "/token",    
    summary="Generate a new JWT token",
    description="Generate a new JWT token for a given user")
async def token(
    request: TokenUserSchema):
    return generate_jwt(request.username)