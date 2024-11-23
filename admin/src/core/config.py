from os import environ

class Config(object):
    """Base configuration."""

    SECRET_KEY = "secret"
    TESTING = False
    SESSION_TYPE = "filesystem"
    DEBUG = False
    


class ProductionConfig(Config):
    MINIO_SERVER = environ.get("MINIO_SERVER")
    MINIO_ACCESS_KEY = environ.get("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = environ.get("MINIO_SECRET_KEY")
    MINIO_SECURE = True
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "pool_recycle": 60,
        "pool_pre_ping": True,
    }
    GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI = environ.get("GOOGLE_REDIRECT_URI")
    GOOGLE_REDIRECT_URI_REGISTER = environ.get("GOOGLE_REDIRECT_URI_REGISTER")
    environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


    pass


class DevelopmentConfig(Config):
    MINIO_SERVER = "localhost:9000" 
    MINIO_ACCESS_KEY="minioAcceso" # Cambiar por el acceso de minio
    MINIO_SECRET_KEY="minioSecreto" # Cambiar por el secreto de minio
    MINIO_SECURE=False
    GOOGLE_CLIENT_ID="clienteGoogle" # Cambiar por el id de google
    GOOGLE_CLIENT_SECRET = "clienteSecreto" # Cambiar por el secreto de google
    GOOGLE_REDIRECT_URI = "http://localhost:5000/auth/callback"
    GOOGLE_REDIRECT_URI_REGISTER = "http://localhost:5000/auth/register_callback"
    environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    DB_USER = "postgres"
    DB_PASSWORD = "postgres"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "postgres"

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    pass

class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True

config = {
    "production" : ProductionConfig,
    "development": DevelopmentConfig,
    "test": TestingConfig,
}