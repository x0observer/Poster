from dotenv import load_dotenv
import os

LOCAL_VARIABLES_FILE = ".env"
env = load_dotenv(LOCAL_VARIABLES_FILE)
print("__env__", env)
DATABASE_USER = os.environ["DATABASE_USER"]
DATABASE_PASSWORD = os.environ["DATABASE_PASSWORD"]
DATABASE_NAME = os.environ["DATABASE_NAME"]
DATABASE_URI = os.environ["DATABASE_URI"]
DATABASE_PORT = os.environ["DATABASE_PORT"]
AUTH_SECRET_KEY = os.environ["AUTH_SECRET_KEY"]
AUTH_ALGORITHM = os.environ["AUTH_ALGORITHM"]
AUTH_ACCESS_TOKEN_EXPIRE_MINUTES = os.environ["AUTH_ACCESS_TOKEN_EXPIRE_MINUTES"]

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://%s:%s@%s:%s/%s" % (
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_URI,
    DATABASE_PORT,
    DATABASE_NAME,
)

settings = {"db": {"uri": SQLALCHEMY_DATABASE_URL},
            "auth": {"secret_key": AUTH_SECRET_KEY,
                     "algorithm": AUTH_ALGORITHM,
                     "access_token_expire_minutes": AUTH_ACCESS_TOKEN_EXPIRE_MINUTES},}