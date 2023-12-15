import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, func, DateTime, ForeignKey, Column, Integer

POSTGRES_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
POSTGRES_USER = os.getenv('DB_USER', 'postgres')
POSTGRES_DB = os.getenv('DB_NAME', 'adv_db')
POSTGRES_HOST = os.getenv('DB_HOST', '127.0.0.1')
POSTGRES_PORT = os.getenv('DB_PORT', '5432')


PG_DSN = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100),index=True ,unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(), nullable=False)
    e_mail: Mapped[str] = mapped_column(String(100))

    advertisements = relationship('Advertisement', back_populates='user')

    @property
    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'password': self.password,
            'e_mail': self.e_mail
        }


class Advertisement(Base):
    __tablename__ = 'advertisement'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    header: Mapped[str] = mapped_column(String(200),index=True, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    date_of_create: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    author: [int] = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    user = relationship('User', back_populates='advertisements')

    @property
    def dict(self):
        return {
            'id': self.id,
            'header': self.header,
            'description': self.description,
            'date': self.date_of_create.isoformat(),
            'author': self.author,
        }


Base.metadata.create_all(bind=engine)
