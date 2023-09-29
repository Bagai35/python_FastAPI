from fastapi import FastAPI, Query, Path
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import sessionmaker
from urllib.parse import unquote
from typing import List

# FastAPI app instance
app = FastAPI()

# SQLAlchemy database models
Base = declarative_base()

class Author(Base):
    __tablename__ = 'Authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
class Book(Base):
    __tablename__ = 'Books'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    isbn = Column(String(255))  # Добавьте столбец isbn
    pageCount = Column(Integer)  # Добавьте столбец pageCount
    publishedDate = Column(DateTime)  # Добавьте столбец publishedDate
    # Добавьте другие столбцы, если они есть в вашей базе данных
    authors = relationship('Author', secondary='BookAuthor')
    categories = relationship('Category', secondary='BookCategory')

class BookAuthor(Base):
    __tablename__ = 'BookAuthor'
    BookId = Column(Integer, ForeignKey('Books.id'), primary_key=True)
    AuthorId = Column(Integer, ForeignKey('Authors.id'), primary_key=True)

class Category(Base):
    __tablename__ = 'Categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

class BookCategory(Base):
    __tablename__ = 'BookCategory'
    BookId = Column(Integer, ForeignKey('Books.id'), primary_key=True)
    CategoryId = Column(Integer, ForeignKey('Categories.id'), primary_key=True)



# Database connection
DATABASE_URL = "mysql+pymysql://root@localhost/books"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



# Controllers
def get_books_by_author(author_id: int, db):
    books = db.query(Book).filter(Book.authors.any(Author.id == author_id)).all()
    return books

def get_books_by_category(category: str, db):
    books = db.query(Book).filter(Book.categories.any(Category.name == category)).all()
    return books

def get_books_by_keyword(keyword: str, db):
    books = db.query(Book).filter(Book.title.ilike(f"%{keyword}%")).all()
    return books

def get_categories_with_book_count(db):
    categories = db.query(Category).all()
    categories_with_count = []
    for category in categories:
        books_in_category = db.query(Book).filter(Book.categories.any(Category.id == category.id)).all()
        books_info = []
        for book in books_in_category:
            authors = [author.name for author in book.authors]
            books_info.append({
                "id": book.id,
                "title": book.title,
                "authors": authors,
                "categories": [category.name for category in book.categories]
                # Добавьте другие атрибуты книги, если они есть в базе данных
            })
        categories_with_count.append({"category": category.name, "books": books_info})
    return categories_with_count




# Routes
@app.get("/")
def read_root():
    return {"message": "Welcome to the Book API!"}


# Гет-запрос для показа всех книг
@app.get("/books")
def get_all_books():
    db = SessionLocal()
    books = db.query(Book).all()
    db.close()
    return books

# Гет-запрос для показа книг с определенным словом в названии
@app.get("/books/search")
def get_books_by_keyword(keyword: str = Query(..., min_length=3)):
    db = SessionLocal()
    books = db.query(Book).filter(Book.title.like(f"%{keyword}%")).all()
    db.close()
    return books

# Гет-запрос для показа книг определенного автора
@app.get("/books/author/{author_id}")
def get_books_by_author(author_id: int):
    db = SessionLocal()
    author_books = db.query(Book).join(Book.authors).filter(Author.id == author_id).all()
    db.close()
    return author_books

# Гет-запрос для показа книг определенной категории
@app.get("/books/category/{category}")
def get_books_by_category(category: str):
    db = SessionLocal()
    category_books = db.query(Book).join(Book.categories).filter(Category.name == category).all()
    db.close()
    return category_books

# Гет-запрос для показа категорий и количества книг в каждой категории
@app.get("/categories")
def get_categories_with_book_count():
    db = SessionLocal()
    categories = db.query(Category).all()
    categories_with_count = []
    for category in categories:
        book_count = db.query(Book).join(Book.categories).filter(Category.id == category.id).count()
        categories_with_count.append({"category": category.name, "book_count": book_count})
    db.close()
    return categories_with_count



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)