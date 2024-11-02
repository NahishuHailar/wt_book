import uuid

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column


# Base class for all models, setting common attributes.
class Base:
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
