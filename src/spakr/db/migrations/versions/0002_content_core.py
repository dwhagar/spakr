"""Content core: page, aliases, revisions, tags, page settings, relation kinds, relations, links.

Revision ID: 0002
Revises: 0001
"""
import sqlalchemy as sa
from alembic import op

from spakr.db.types import BigId, DateTime, PAGE_TYPES, SmallId, TABLE_OPTIONS

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None

PAGE_TYPE = sa.Enum(*PAGE_TYPES, name="page_type")

RELATION_KINDS = [
    ("member_of", "member of", "has member"),
    ("located_in", "located in", "contains"),
    ("grants", "grants", "granted by"),
    ("requires", "requires", "required by"),
    ("rules", "rules", "ruled by"),
    ("allied_with", "allied with", "allied with"),
    ("owns", "owns", "owned by"),
    ("created_by", "created by", "created"),
]


def upgrade() -> None:
    op.create_table(
        "page",
        sa.Column("id", BigId, primary_key=True, autoincrement=True),
        sa.Column("type", PAGE_TYPE, nullable=False),
        sa.Column("slug", sa.String(160), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("summary", sa.String(500), nullable=False, server_default=""),
        sa.Column("visibility", sa.Enum("public", "gm", name="page_visibility"),
                  nullable=False, server_default="public"),
        # Reserved for later per-group visibility: unused and NULL in 1.0, no FK until groups exist.
        sa.Column("visibility_group_id", BigId, nullable=True),
        sa.Column("current_commit", sa.CHAR(40), nullable=True),
        sa.Column("created_by", BigId, sa.ForeignKey("user.id"), nullable=True),
        sa.Column("updated_by", BigId, sa.ForeignKey("user.id"), nullable=True),
        sa.Column("created_at", DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", DateTime, nullable=True),
        sa.UniqueConstraint("type", "slug", name="uq_page_type_slug"),
        **TABLE_OPTIONS,
    )
    op.create_index("ix_page_visibility_updated", "page", ["visibility", "updated_at"])

    op.create_table(
        "page_alias",
        sa.Column("page_id", BigId, sa.ForeignKey("page.id", ondelete="CASCADE"), nullable=False),
        sa.Column("type", PAGE_TYPE, nullable=False),
        sa.Column("slug", sa.String(160), nullable=False),
        sa.PrimaryKeyConstraint("type", "slug"),
        **TABLE_OPTIONS,
    )
    op.create_index("ix_page_alias_page", "page_alias", ["page_id"])

    op.create_table(
        "page_revision",
        sa.Column("id", BigId, primary_key=True, autoincrement=True),
        sa.Column("page_id", BigId, sa.ForeignKey("page.id", ondelete="CASCADE"), nullable=False),
        sa.Column("commit_sha", sa.CHAR(40), nullable=False),
        sa.Column("author_id", BigId, sa.ForeignKey("user.id"), nullable=True),
        sa.Column("summary", sa.String(300), nullable=False, server_default=""),
        sa.Column("created_at", DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("reverts_commit", sa.CHAR(40), nullable=True),
        **TABLE_OPTIONS,
    )
    op.create_index("ix_page_revision_page", "page_revision", ["page_id", "created_at"])

    op.create_table(
        "tag",
        sa.Column("id", BigId, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(60), nullable=False, unique=True),
        **TABLE_OPTIONS,
    )
    op.create_table(
        "page_tag",
        sa.Column("page_id", BigId, sa.ForeignKey("page.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("tag_id", BigId, sa.ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True),
        **TABLE_OPTIONS,
    )
    op.create_table(
        "page_setting",
        sa.Column("page_id", BigId, sa.ForeignKey("page.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("setting_id", SmallId, sa.ForeignKey("setting.id", ondelete="CASCADE"),
                  primary_key=True),
        **TABLE_OPTIONS,
    )

    relation_kind = op.create_table(
        "relation_kind",
        sa.Column("id", SmallId, primary_key=True, autoincrement=True),
        sa.Column("code", sa.String(40), nullable=False, unique=True),
        sa.Column("label", sa.String(80), nullable=False),
        sa.Column("inverse_label", sa.String(80), nullable=False),
        # JSON list of page types, or NULL to allow any (MySQL SET is awkward to migrate).
        sa.Column("from_types", sa.JSON, nullable=True),
        sa.Column("to_types", sa.JSON, nullable=True),
        sa.Column("sort", sa.SmallInteger, nullable=False, server_default="0"),
        sa.Column("retired_at", DateTime, nullable=True),
        **TABLE_OPTIONS,
    )
    op.bulk_insert(relation_kind, [
        {"code": c, "label": a, "inverse_label": b, "sort": i}
        for i, (c, a, b) in enumerate(RELATION_KINDS, start=1)
    ])

    op.create_table(
        "relation",
        sa.Column("id", BigId, primary_key=True, autoincrement=True),
        sa.Column("from_page_id", BigId, sa.ForeignKey("page.id", ondelete="CASCADE"), nullable=False),
        sa.Column("to_page_id", BigId, sa.ForeignKey("page.id", ondelete="CASCADE"), nullable=False),
        sa.Column("relation_kind_id", SmallId, sa.ForeignKey("relation_kind.id"), nullable=False),
        sa.Column("note", sa.String(300), nullable=True),
        sa.UniqueConstraint("from_page_id", "to_page_id", "relation_kind_id", name="uq_relation"),
        **TABLE_OPTIONS,
    )
    op.create_index("ix_relation_backlinks", "relation", ["to_page_id", "relation_kind_id"])

    op.create_table(
        "page_link",
        sa.Column("from_page_id", BigId, sa.ForeignKey("page.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("to_page_id", BigId, sa.ForeignKey("page.id", ondelete="CASCADE"), primary_key=True),
        **TABLE_OPTIONS,
    )
    op.create_index("ix_page_link_to", "page_link", ["to_page_id"])
