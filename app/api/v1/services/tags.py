from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagUpdate
from .base_crud import CRUDBase


# CRUD class for Tag model
class CRUDTag(CRUDBase[Tag, TagCreate, TagUpdate]):
    pass


# Instantiate the CRUD class for use in API routes
tag_crud = CRUDTag(Tag)
