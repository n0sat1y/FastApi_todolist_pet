from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

from repositories import UserRepository
from schemas import GetUserIdSchema, TokenSchema, UserSchema
from utils import decode_jwt, encode_access_jwt, validate_token_type


router = APIRouter(prefix='/users', tags=['Пользователи'])
http_bearer = HTTPBearer()


@router.post('/register', response_model=GetUserIdSchema, summary='Регистрация пользователя')
async def add_user(user: UserSchema = Depends()):
	user_id = await UserRepository.create_user(user)
	return GetUserIdSchema(user_id=user_id)

@router.post('/login', summary='Логин')
async def login(user: UserSchema = Depends()):
	tokens = await UserRepository.login_user(user)
	return TokenSchema(**tokens, type='Bearer')

@router.post('/refresh', response_model=TokenSchema, response_model_exclude_none=True, summary='Получить аксесс токен по рефрешу')
async def get_access_from_refresh(creds: HTTPAuthorizationCredentials = Depends(http_bearer)):
	try:
		token = decode_jwt(creds.credentials)
		refresh = validate_token_type(token, 'refresh')
		payload = {'sub': refresh.get('sub')}
		access_token = encode_access_jwt(payload)
		return TokenSchema(access_token=access_token, type='Baerer')
	except jwt.ExpiredSignatureError:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Refresh token has expired')