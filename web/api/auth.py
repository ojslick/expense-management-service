from pathlib import Path
import jwt

from cryptography.hazmat.primitives import serialization

public_key_text = (Path(__file__).parent / "../../public_key.pem").read_text()

public_key = serialization.load_pem_public_key(public_key_text.encode())

def decode_and_validate_token(access_token):
    """
    Validates the access token and returns the payload if the token is valid.
    """
    return jwt.decode(
        access_token,
        key=public_key,
        algorithms=["RS256"],
        audience=["https://127.0.0.1/api/v1/expenses"],
    )
