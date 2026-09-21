"""Example models — add your own models here.

Each model should inherit from `db.Model`.  The `TimestampMixin` adds
`created_at` and `updated_at` columns automatically.

Example
-------
    from app.db import db
    from app.db.models import TimestampMixin

    class MyResource(TimestampMixin, db.Model):
        __tablename__ = 'my_resources'

        id    = db.Column(db.Integer, primary_key=True)
        name  = db.Column(db.String(128), nullable=False)
"""
from datetime import datetime, timezone
from app.db import db


class TimestampMixin:
    """Mixin that adds created_at / updated_at columns to any model."""
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


# ---------------------------------------------------------------------------
# Add your models below, e.g.:
#
# class User(TimestampMixin, db.Model):
#     __tablename__ = 'users'
#     id       = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), unique=True, nullable=False, index=True)
#     email    = db.Column(db.String(120), unique=True, nullable=False, index=True)
# ---------------------------------------------------------------------------

