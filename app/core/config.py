from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str
    app_description: str
    secret: str
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_container: str
    postgres_port: int

    class Config:
        env_file = '.env'
        extra = 'ignore'

    def get_db_url(self):
        return (
            f'postgresql+asyncpg://'
            f'{self.postgres_user}:{self.postgres_password}@'
            f'{self.postgres_container}:{self.postgres_port}/'
            f'{self.postgres_db}'
        )


settings = Settings()
