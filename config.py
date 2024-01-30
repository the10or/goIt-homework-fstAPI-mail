import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
MAIL_FROM = os.environ.get("MAIL_FROM")
MAIL_PORT = os.environ.get("MAIL_PORT")
MAIL_SERVER = os.environ.get("MAIL_SERVER")
MAIL_FROM_NAME = os.environ.get("MAIL_FROM_NAME")
MAIL_STARTTLS = False
MAIL_SSL_TLS = True
USE_CREDENTIALS = True
VALIDATE_CERTS = True
TEMPLATE_FOLDER = Path(__file__).parent / 'templates'

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

CLOUDINARY_NAME = os.environ.get("CLOUD_NAME")
CLOUDINARY_API_KEY = os.environ.get("API_KEY")
CLOUDINARY_API_SECRET = os.environ.get("API_SECRET")
