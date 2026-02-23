import hashlib
from datetime import datetime, timezone

import jwt
from django.conf import settings
from django.utils import timezone as tz
from rest_framework.exceptions import AuthenticationFailed

from user.models import RefreshToken, User


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def generate_access_token(user: "User") -> str:
    payload = {
        "user_id": user.id,
        "type": "access",
        "exp": datetime.now(tz.utc) + settings.JWT_ACCESS_TOKEN_EXPIRY,
        "iat": datetime.now(tz.utc),
    }
    return jwt.encode(
        payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )


def generate_refresh_token(user):
    now = timezone.now()
    expires_at = now + settings.JWT_REFRESH_TOKEN_EXPIRY
    payload = {
        "user_id": user.id,
        "type": "refresh",
        "exp": expires_at,
        "iat": now,
    }
    token = jwt.encode(
        payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    RefreshToken.objects.create(
        user=user,
        token_hash=hash_token(token),
        expires_at=expires_at,
    )
    return token


def rotate_refresh_token(old_token_str: str):
    old_token_hash = hash_token(old_token_str)
    try:
        old_token = RefreshToken.objects.select_for_update().get(
            token_hash=old_token_hash
        )
    except RefreshToken.DoesNotExist:
        raise AuthenticationFailed("Invalid refresh token")
    if old_token.is_revoked or old_token.is_expired():
        raise AuthenticationFailed("Refresh token invalid")
    try:
        payload = jwt.decode(
            old_token_str,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Refresh token expired")
    except jwt.InvalidTokenError:
        raise AuthenticationFailed("Invalid refresh token")
    if payload.get("type") != "refresh":
        raise AuthenticationFailed("Invalid token type")

    user = old_token.user
    new_refresh_token = generate_refresh_token(user)
    old_token.is_revoked = True
    old_token.save(update_fields=["is_revoked"])
    access_token = generate_access_token(user)

    return access_token, new_refresh_token


def revoke_refresh_token(token_str: str):
    token_hash = hash_token(token_str)
    try:
        token = RefreshToken.objects.get(token_hash=token_hash)
    except RefreshToken.DoesNotExist:
        return
    token.is_revoked = True
    token.save(update_fields=["is_revoked"])


def just_for_commit():
    """
    This function is just a placeholder to ensure that the file is not empty.
    It can be removed or modified as needed.
    """
    pass
