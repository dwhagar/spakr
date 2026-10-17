"""Column types and table options shared by migrations (MySQL 8 first, SQLite for fast tests)."""

import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# BIGINT UNSIGNED on MySQL; plain INTEGER on SQLite so primary keys auto-increment there.
BigId = (
    sa.BigInteger()
    .with_variant(mysql.BIGINT(unsigned=True), "mysql")
    .with_variant(sa.Integer(), "sqlite")
)
SmallId = (
    sa.SmallInteger()
    .with_variant(mysql.SMALLINT(unsigned=True), "mysql")
    .with_variant(sa.Integer(), "sqlite")
)
# All timestamps are UTC with microseconds.
DateTime = sa.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql")

TABLE_OPTIONS = {
    "mysql_engine": "InnoDB",
    "mysql_charset": "utf8mb4",
    "mysql_collate": "utf8mb4_0900_ai_ci",
}

PAGE_TYPES = ("character", "item", "place", "spell", "ability", "skill",
              "entity", "race", "nation_state", "free")
