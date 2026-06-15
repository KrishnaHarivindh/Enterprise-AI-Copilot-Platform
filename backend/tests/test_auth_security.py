from uuid import uuid4

from app.auth.hashing import hash_password, verify_password
from app.auth.jwt import create_access_token, decode_token


def test_password_hashing_does_not_store_plain_text():
    password = "StrongPass1!"
    hashed_password = hash_password(password)

    assert hashed_password != password
    assert verify_password(password, hashed_password)
    assert not verify_password("WrongPass1!", hashed_password)


def test_access_token_round_trip():
    user_id = uuid4()
    token = create_access_token(user_id)

    assert decode_token(token) == user_id
    assert decode_token(token, expected_type="refresh") is None
