from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
    owner_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


class Item(Base):
    __tablename__ = 'item'
    user = relationship(User)
    id = Column(Integer, primary_key=True)
    title = Column(String(60), nullable=False)
    description = Column(String(260))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    owner_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


engine = create_engine('sqlite:///opencatalog.db')
Base.metadata.create_all(engine)
