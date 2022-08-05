from alembic import command
from alembic.config import Config
from decouple import config


db_connection_string = config("DATABASE_URL")

def execute_migration():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", db_connection_string)
    alembic_cfg.set_main_option("script_location", "migrations")

    print("Execution upgrade to Head")
    command.upgrade(alembic_cfg, "head")        
    print("Head upgrade executed")