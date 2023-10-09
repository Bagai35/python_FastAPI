from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Author(Base):
    __tablename__ = 'Authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    books = relationship('Book', secondary='BookAuthor')

class Book(Base):
    __tablename__ = 'Books'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    authors = relationship('Author', secondary='BookAuthor', cascade='all, delete', back_populates='books')
    categories = relationship('Category', secondary='BookCategory', cascade='all, delete')



class BookCategory(Base):
    __tablename__ = 'BookCategory'
    BookId = Column(Integer, ForeignKey('Books.id', ondelete='CASCADE'), primary_key=True)
    CategoryId = Column(Integer, ForeignKey('Categories.id', ondelete='CASCADE'), primary_key=True)


class BookAuthor(Base):
    __tablename__ = 'BookAuthor'
    BookId = Column(Integer, ForeignKey('Books.id', ondelete='CASCADE'), primary_key=True)
    AuthorId = Column(Integer, ForeignKey('Authors.id', ondelete='CASCADE'), primary_key=True)


class Category(Base):
    __tablename__ = 'Categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    books = relationship('Book', secondary='BookCategory', cascade='all, delete', back_populates='categories')