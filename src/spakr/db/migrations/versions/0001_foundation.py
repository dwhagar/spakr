"""Foundation: schema version, site config, accounts, roles, permissions, settings, audit log.

Revision ID: 0001
Revises:
"""
import sqlalchemy as sa
from alembic import op

from spakr.db.types import BigId, DateTime, SmallId, TABLE_OPTIONS

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

PERMISSIONS = [
    ("page.read", "Read public pages"),
    ("page.read_gm", "Read GM-only pages"),
    ("page.edit", "Create and edit pages"),
    ("page.delete", "Delete and restore pages"),
    ("media.upload", "Upload media"),
    ("media.review", "Review and publish uploaded media"),
    ("user.manage", "Invite, edit and suspend users"),
    ("role.manage", "Change role assignments"),
    ("apikey.create_own", "Create API keys limited to the owner's permissions"),
    ("apikey.create_any", "Create API keys with any permission and service accounts"),
    ("site.configure", "Change site settings"),
]

ROLES = {
    "reader": ("Read public pages", ["page.read", "apikey.create_own"]),
    "editor": ("Write pages and upload media",
               ["page.read", "page.edit", "media.upload", "apikey.create_own"]),
    "gm": ("Game master: also reads GM-only pages",
           ["page.read", "page.read_gm", "page.edit", "media.upload", "apikey.create_own"]),
    "mod": ("Moderator: also deletes pages and reviews media",
            ["page.read", "page.read_gm", "page.edit", "page.delete", "media.upload",
             "media.review", "apikey.create_own"]),
    "admin": ("Administrator: everything", [code for code, _ in PERMISSIONS]),
}

SETTINGS = [
    ("high_fantasy", "High fantasy", 1),
    ("modern_horror", "Modern / cosmic horror", 2),
    ("scifi", "Science fiction", 3),
]


def upgrade() -> None:
    schema_version = op.create_table(
        "schema_version",
        sa.Column("id", sa.SmallInteger, primary_key=True),
        sa.Column("version", sa.Integer, nullable=False),
        sa.Column("updated_at", DateTime, nullable=False, server_default=sa.func.now()),
        **TABLE_OPTIONS,
    )
    op.bulk_insert(schema_version, [{"id": 1, "version": 1}])

    op.create_table(
        "config",
        sa.Column("key", sa.String(100), primary_key=True),
        sa.Column("value", sa.JSON, nullable=False),
        sa.Column("updated_by", BigId, nullable=True),
        sa.Column("updated_at", DateTime, nullable=False, server_default=sa.func.now()),
        **TABLE_OPTIONS,
    )

    permission = op.create_table(
        "permission",
        sa.Column("id", SmallId, primary_key=True, autoincrement=True),
        sa.Column("code", sa.String(60), nullable=False, unique=True),
        sa.Column("description", sa.String(255), nullable=False),
        **TABLE_OPTIONS,
    )
    role = op.create_table(
        "role",
        sa.Column("id", BigId, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(40), nullable=False, unique=True),
        sa.Column("description", sa.String(255), nullable=False),
        sa.Column("is_system", sa.Boolean, nullable=False, server_default=sa.true()),
        **TABLE_OPTIONS,
    )
    role_permission = op.create_table(
        "role_permission",
        sa.Column("role_id", BigId, sa.ForeignKey("role.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("permission_id", SmallId, sa.ForeignKey("permission.id", ondelete="CASCADE"),
                  primary_key=True),
        **TABLE_OPTIONS,
    )

    op.create_table(
        "user",
        sa.Column("id", BigId, primary_key=True, autoincrement=True),
        sa.Column("email", sa.String(254), nullable=False, unique=True),
        sa.Column("username", sa.String(40), nullable=False, unique=True),
        sa.Column("display_name", sa.String(100), nullable=False, server_default=""),
        sa.Column("password_hash", sa.String(255), nullable=True),
        sa.Column("status", sa.Enum("invited", "active", "suspended", "deleted", name="user_status"),
                  nullable=False, server_default="invited"),
        sa.Column("is_service", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column("email_verified_at", DateTime, nullable=True),
        sa.Column("created_at", DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("last_login_at", DateTime, nullable=True),
        sa.Column("deleted_at", DateTime, nullable=True),
        **TABLE_OPTIONS,
    )
    op.create_table(
        "user_role",
        sa.Column("user_id", BigId, sa.ForeignKey("user.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("role_id", BigId, sa.ForeignKey("role.id", ondelete="CASCADE"), primary_key=True),
        **TABLE_OPTIONS,
    )

    setting = op.create_table(
        "setting",
        sa.Column("id", SmallId, primary_key=True, autoincrement=True),
        sa.Column("code", sa.String(40), nullable=False, unique=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("sort", sa.SmallInteger, nullable=False, server_default="0"),
        **TABLE_OPTIONS,
    )

    op.create_table(
        "audit_log",
        sa.Column("id", BigId, primary_key=True, autoincrement=True),
        sa.Column("actor_id", BigId, sa.ForeignKey("user.id"), nullable=True),
        sa.Column("action", sa.String(60), nullable=False),
        sa.Column("target_type", sa.String(40), nullable=True),
        sa.Column("target_id", sa.String(64), nullable=True),
        sa.Column("detail", sa.JSON, nullable=True),
        sa.Column("ip", sa.String(45), nullable=True),
        sa.Column("created_at", DateTime, nullable=False, server_default=sa.func.now()),
        **TABLE_OPTIONS,
    )
    op.create_index("ix_audit_log_actor", "audit_log", ["actor_id", "created_at"])
    op.create_index("ix_audit_log_target", "audit_log", ["target_type", "target_id"])

    # Seed data
    op.bulk_insert(permission, [{"code": c, "description": d} for c, d in PERMISSIONS])
    op.bulk_insert(role, [{"name": n, "description": d, "is_system": True}
                          for n, (d, _) in ROLES.items()])
    op.bulk_insert(setting, [{"code": c, "name": n, "sort": s} for c, n, s in SETTINGS])

    conn = op.get_bind()
    perm_ids = dict(conn.execute(sa.select(permission.c.code, permission.c.id)).all())
    role_ids = dict(conn.execute(sa.select(role.c.name, role.c.id)).all())
    op.bulk_insert(role_permission, [
        {"role_id": role_ids[name], "permission_id": perm_ids[code]}
        for name, (_, codes) in ROLES.items() for code in codes
    ])
