from datetime import datetime, timedelta

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from config import SECRET_KEY, ALGORITHM
from dependencies.database import get_db
from repository import users


class Auth:
    """
    A class for auth services

    :param pwd_context: (CryptContext) context for password hashing
    :param SECRET_KEY: (str) secret key for jwt token signing and verification
    :param ALGORITHM: (str) cyphering algorithm for jwt token generation
    :param oauth2_scheme: (OAuth2PasswordBearer) custom oauth2 scheme

    """

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = SECRET_KEY
    ALGORITHM = ALGORITHM
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

    def verify_password(self, plain_password, hashed_password):
        """
        a method for password verification

        :param plain_password: (str) password to verify
        :param hashed_password: (str) hashed password
        :return: (bool) True if password is correct, False otherwise

        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        """
        a method for password hashing

        :param password: (str) password to hash
        :return: (str) hashed password
        """
        return self.pwd_context.hash(password)

    async def create_access_token(self, data: dict, expires_delta: int | None = None):

        """
        a method for creating access token

        :param data: (dict) data to encode
        :param expires_delta: (int) expiration time in seconds
        :return: (str) encoded access token

        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire,
                          "scope": "access_token"})
        encoded_access_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_access_token

    async def create_refresh_token(self, data: dict, expires_delta: int | None = None):
        """
        a method for creating refresh token

        :param data: (dict) data to encode
        :param expires_delta: (int) expiration time in seconds
        :return: (str) encoded refresh token
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=15)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire,
                          "scope": "refresh_token"})
        encoded_refresh_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_refresh_token

    async def decode_refresh_token(self, refresh_token: str):
        """
        a method for decoding refresh token

        :param refresh_token: (str) refresh token
        :return: (str) email of the user
        :raise: HTTPException with status code 401 if token is invalid or expired
        """
        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload["scope"] == "refresh_token":
                email = payload["sub"]
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid scope for token")
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate credentials")

    async def get_current_user(self, token: str = Depends(oauth2_scheme),
                               db: Session = Depends(get_db)):

        """
        a method for getting current user

        :param token: (str) access token
        :param db: (Session) database session
        :return: (User) current user
        :raise: HTTPException with status code 401 if token is invalid or expired

        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])

            if payload["scope"] == "access_token":
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as e:
            raise credentials_exception

        user = await users.get_user_by_email(email, db)
        if user is None:
            raise credentials_exception
        return user

    def create_email_token(self, data: dict):
        """
        a method for creating email token

        :param data: (dict) data to encode
        :return: (str) encoded email token

        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=1)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token

    def get_email_from_token(self, token: str):
        """
        a method for getting email from token

        :param token: (str) token
        :return: (str) email of the user
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email = payload["sub"]
            return email
        except JWTError:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Invalid token for email")


auth_service = Auth()
