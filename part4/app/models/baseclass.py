from app.extensions import db
from datetime import datetime, timezone
import uuid


class BaseModel(db.Model):
    """Base model providing unique ID and timestamp management."""
    __abstract__ = True  # This ensures SQLAlchemy does not create a table for BaseModel

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate= lambda: datetime.now(timezone.utc))

    def save(self):
        """
        Update the `updated_at` timestamp to the current time.
        """
        self.updated_at = datetime.now(timezone.utc)
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """
        Update attributes of the instance based on a dictionary.

        Args:
            data (dict): Dictionary of attributes to update.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        """
        Convertit l'objet en dictionnaire avec ses colonnes de base.
        Utile pour sérialisation JSON simple.
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns} # type: ignore

