from rest_framework.authentication import authenticate

from .models import User


def register_user(*, username: str, email: str, password: str) -> User:
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
    )
    return user


def login_user(*, email: str, password: str) -> User:
    user = authenticate(username=email, password=password)
    if not user:
        raise ValueError("Invalid credentials")
    return user
