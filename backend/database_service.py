import importlib
import tomllib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from backend.database.base_class import BaseSql

class DatabaseService(object):
    """
    Database service class
    """

    postgres_user = None
    postgres_password = None
    postgres_host = None
    postgres_port = None
    postgres_database = None

    engine = None

    def __init__(
        self,
    ) -> None:
        DatabaseService.create_database_session()

    @staticmethod
    def create_database_session() -> Session:
        if None in [
            DatabaseService.postgres_user,
            DatabaseService.postgres_password,
            DatabaseService.postgres_host,
            DatabaseService.postgres_port,
            DatabaseService.postgres_database
        ]:
            config_file = importlib.resources.files("backend") / "environment.toml"

            with open(config_file, "rb") as toml_config:
                data = tomllib.load(toml_config)
                toml_config.close()

            DatabaseService.postgres_user     = data["database_user"]
            DatabaseService.postgres_password = data["database_password"]
            DatabaseService.postgres_host     = data["database_host"]
            DatabaseService.postgres_port     = data["database_port"]
            DatabaseService.postgres_database = data["database_name"]

        # Create session
        if DatabaseService.engine is None:
            DatabaseService.engine = create_engine(
                f'postgresql://{DatabaseService.postgres_user}:{DatabaseService.postgres_password}' +
                f'@{DatabaseService.postgres_host}:{DatabaseService.postgres_port}/{DatabaseService.postgres_database}',
                echo=False
            )
        BaseSql.metadata.create_all(bind=DatabaseService.engine)
        session = sessionmaker(bind=DatabaseService.engine)()

        # Session settings
        session.expire_on_commit = False

        return session
