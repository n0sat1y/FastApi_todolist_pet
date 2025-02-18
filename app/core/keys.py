from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


with open('app/core/private_key.pem', 'rb') as key:
    private_key_obj = serialization.load_pem_private_key(
        key.read(),
        password=None,
        backend=default_backend()
    )
    
with open('app/core/public_key.pem', 'rb') as key:
    public_key_obj = serialization.load_pem_public_key(
        key.read(),
        backend=default_backend()
    )   