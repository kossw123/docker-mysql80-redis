from sqlalchemy import Column, Integer, String
from db import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    price = Column(Integer)