from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import datetime, timedelta


class Settings(BaseSettings):
	#----jwt config----
	jwt_encode_algorithm: str = 'RS256'
	jwt_iat: datetime = datetime.utcnow()
	jwt_access_exp: datetime = datetime.utcnow() + timedelta(minutes=15)
	jwt_refresh_exp: datetime = datetime.utcnow() + timedelta(days=30)

	#----db----
	db_url: str = 'sqlite+aiosqlite:///tasks.db'

	#----keys----
	public_key: str
	secret_key: str

	model_config = SettingsConfigDict(env_file='.env')

settings = Settings()