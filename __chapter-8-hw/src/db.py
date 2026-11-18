import os
from collections.abc import Iterator
from contextlib import contextmanager
from functools import lru_cache
from pathlib import Path
from typing import Any

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import Connection, Engine, create_engine, text
from sqlalchemy.engine import URL

# ../.env
load_dotenv(Path(__file__).resolve().parents[1] / ".env")


def _server_url() -> URL:
  return URL.create(
    "mysql+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "3306")),
  )


def ensure_database() -> None:
  name = os.getenv("DB_NAME")
  if not name:
    return
  server_engine = create_engine(_server_url())
  try:
    with server_engine.begin() as conn:
      conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{name}`"))
  finally:
    server_engine.dispose()


@lru_cache(maxsize=1)
def get_engine() -> Engine:
  url = _server_url().set(database=os.getenv("DB_NAME") or None)
  return create_engine(url)


@contextmanager
def db_connection(commit: bool = False) -> Iterator[Connection]:
  engine = get_engine()
  with engine.begin() if commit else engine.connect() as conn:
    yield conn


def query_df(
  sql: str,
  params: dict[str, Any] | None = None,
  conn: Connection | None = None,
) -> pd.DataFrame:
  if conn is not None:
    return pd.read_sql(text(sql), conn, params=params)
  with db_connection() as own_conn:
    return pd.read_sql(text(sql), own_conn, params=params)


def close_engine() -> None:
  if get_engine.cache_info().currsize:
    get_engine().dispose()
    get_engine.cache_clear()
