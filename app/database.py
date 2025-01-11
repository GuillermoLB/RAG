from app.dependencies import get_settings

settings = get_settings()
database = settings.POSTGRES_DB
user = settings.POSTGRES_USER
password = settings.POSTGRES_PASSWORD
server = settings.POSTGRES_HOST
port = settings.POSTGRES_PORT
