from sqlalchemy import Column, Integer , String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Valentine(Base):
    __tablename__ = 'valentines'

    id = Column(Integer,primary_key=True,index= True)
    user = Column(Integer, ForeignKey('users.id'))
    name = Column(String, index=False)

    users = relationship('User', back_populates='valentines')

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    Fullname = Column(String, nullable=True)
    email = Column(String, unique=True, index=True)
    password = Column(String,nullable=False)

    valentines = relationship('Valentine', back_populates='users')
