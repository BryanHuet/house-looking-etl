from datetime import datetime
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

# Define the SQLAlchemy Base
Base = declarative_base()


class House(Base):
    __tablename__ = 'house'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Integer)
    photo = Column(String)
    size = Column(String)
    ground = Column(String)
    address = Column(String)
    link = Column(String)
    create_date = Column(String)

    def __init__(self, title, price, photo, size,
                 ground, address, link):
        self.title = title
        self.price = price
        self.photo = photo
        self.size = size
        self.ground = ground
        self.address = address
        self.link = link
        self.create_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return self.price

    def __repr__(self) -> str:
        return f"House({self.title}, {self.price}, {self.address}, \
          {self.size}, {self.ground}, {self.photo}, {self.link}"
