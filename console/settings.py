from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    class Config:
        env_prefix = "CONSOLE_"

    debug: bool = False
    bind_address: str = "127.0.0.1"
    port: int = 3000
    pg_dsn: PostgresDsn = "postgres://postgres:postgres@localhost:5432/postgres"
