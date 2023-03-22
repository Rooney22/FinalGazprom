from pydantic import BaseSettings


class Settings(BaseSettings):
    host: str
    port: int
    login: str
    password: str
    base_host: str
    base_port: int
    base_name: str
    jwt_secret: str
    jwt_algorithm: str
    jwt_expires_seconds: int
    admin_username: str
    admin_password: str


settings = Settings(
    _env_file='../.env',
    _env_file_encoding='utf-8',
)
