from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from core.config import settings

public_key=settings.public_key
secret_key=settings.secret_key

private_key_obj = serialization.load_pem_private_key(
    secret_key.encode(),
    password=None,
    backend=default_backend()
)

public_key_obj = serialization.load_pem_public_key(
    public_key.encode(),
    backend=default_backend()
)