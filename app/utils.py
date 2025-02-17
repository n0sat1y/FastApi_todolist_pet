import bcrypt
from fastapi import HTTPException, status
import jwt
from datetime import datetime, timedelta

from keys import public_key_obj, private_key_obj

def hash_password(password: str) -> bytes:
	salt = bcrypt.gensalt()
	hashed_pwd = bcrypt.hashpw(password.encode(), salt)
	return hashed_pwd

def validate_password(password: str, hashed_pw: bytes) -> bool:
	return bcrypt.checkpw(password.encode(), hashed_pw)

def encode_jwt(payload, type, timedelta_minutes=0, timedelta_days=0):
	key: str = private_key_obj
	algorithm: str = 'RS256'

	payload['iat'] = datetime.utcnow()
	payload['exp'] = datetime.utcnow() + timedelta(minutes=timedelta_minutes, days=timedelta_days)
	payload['type'] = type
	
	token = jwt.encode(payload, key, algorithm)
	return token

def encode_access_jwt(payload):
	token_lifetime_minutes = 15
	return encode_jwt(payload, 'access', timedelta_minutes=token_lifetime_minutes)

def encode_refresh_jwt(payload):
	token_lifetime_days = 30
	return encode_jwt(payload, 'refresh', timedelta_days=token_lifetime_days)

def decode_jwt(token):
	key: str = public_key_obj
	algorithm: str = 'RS256'

	data = jwt.decode(token, key, algorithms=[algorithm])
	return data

def validate_token_type(token, token_type_to_validate):
	token_type = token.get('type')
	if token_type != token_type_to_validate:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token type')
	return token