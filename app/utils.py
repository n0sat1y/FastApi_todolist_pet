import bcrypt
from fastapi import HTTPException, status
import jwt
from datetime import datetime, timedelta

from core.keys import public_key_obj, private_key_obj
from core.config import settings

def hash_password(password: str) -> bytes:
	salt = bcrypt.gensalt()
	hashed_pwd = bcrypt.hashpw(password.encode(), salt)
	return hashed_pwd

def validate_password(password: str, hashed_pw: bytes) -> bool:
	return bcrypt.checkpw(password.encode(), hashed_pw)

def encode_jwt(payload, type):
	key = private_key_obj
	algorithm = settings.jwt_encode_algorithm
	payload['iat'] = settings.jwt_iat
	payload['type'] = type
	token = jwt.encode(payload, key, algorithm)
	return token

def encode_access_jwt(payload):
	payload['exp'] = settings.jwt_access_exp
	return encode_jwt(payload, 'access')

def encode_refresh_jwt(payload):
	payload['exp'] = settings.jwt_refresh_exp
	return encode_jwt(payload, 'refresh')

def decode_jwt(token: str) -> dict:
	key = public_key_obj
	algorithm = settings.jwt_encode_algorithm

	data = jwt.decode(token, key, algorithms=[algorithm])
	return data

def validate_token_type(token, token_type_to_validate):
	token_type = token.get('type')
	if token_type != token_type_to_validate:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token type')
	return token