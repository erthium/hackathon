import os
from logging.config import fileConfig

import alembic_postgresql_enum  # noqa: F401 # Required for PostgreSQL ENUM support
import dotenv
from alembic import context
from app.models import Base  # noqa: F401 # __init__.py imports all models
from sqlalchemy import engine_from_config, pool

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
  fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# Load environemnt variables from .env for the DB URL
# https://alembic.sqlalchemy.org/en/latest/tutorial.html#:~:text=If%20the%20SQLAlchemy,URL%20or%20URLs.
DOTENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")
dotenv.load_dotenv(DOTENV_PATH)
DB_URL = os.environ.get("DB_URL")
assert DB_URL, "DB URL not found in environment variables"

# Seemed nice:
# https://stackoverflow.com/questions/37890284/ini-file-load-environment-variable
config.set_main_option("sqlalchemy.url", DB_URL)


def run_migrations_offline() -> None:
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


def run_migrations_online() -> None:
  """Run migrations in 'online' mode.

  In this scenario we need to create an Engine
  and associate a connection with the context.

  """
  connectable = engine_from_config(
    config.get_section(config.config_ini_section, {}),
    prefix="sqlalchemy.",
    poolclass=pool.NullPool,
  )

  with connectable.connect() as connection:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
      context.run_migrations()


if context.is_offline_mode():
  run_migrations_offline()
else:
  run_migrations_online()
