from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import datetime, timedelta, timezone


class Settings(BaseSettings):
	#----jwt config----
	jwt_encode_algorithm: str = 'RS256'
	jwt_iat: datetime = datetime.now(timezone.utc)
	jwt_access_exp: datetime = datetime.now(timezone.utc) + timedelta(minutes=15)
	jwt_refresh_exp: datetime = datetime.now(timezone.utc) + timedelta(days=30)

	#----db----
	db_url: str
	
	model_config = SettingsConfigDict(env_file='.env')


settings = Settings()