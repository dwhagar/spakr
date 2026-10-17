"""Alembic environment: runs on a connection handed in by spakr.db.migrate."""

from alembic import context

connection = context.config.attributes.get("connection")
if connection is None:
    raise RuntimeError("Run migrations through spakr.db.migrate (spakr init-db), not the alembic CLI.")

context.configure(connection=connection, target_metadata=None, transaction_per_migration=True)
with context.begin_transaction():
    context.run_migrations()
