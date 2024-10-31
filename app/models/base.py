from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr


# Base class for all models, setting common attributes and table names
@as_declarative()
class Base:
    id = Column(Integer, primary_key=True, index=True)

    # Automatically generate table names based on class name
    @declared_attr
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"
