from logging.config import fileConfig

from sqlalchemy import create_engine
from alembic import context
import os

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

db_cluster_arn = os.getenv('DB_CLUSTER_ARN')
secret_arn = os.getenv('DB_SECRET_ARN')
database_name = os.getenv('DB_NAME')

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    if db_cluster_arn:
        db_connection_string = 'postgresql+auroradataapi://:@/' + database_name
        connectable = create_engine(
            db_connection_string,
            echo=True,
            connect_args=dict(aurora_cluster_arn=db_cluster_arn, secret_arn=secret_arn))
    else:
        db_connection_string = config.get_main_option("sqlalchemy.url")
        connectable = create_engine(
            db_connection_string,
            echo=True)         

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
