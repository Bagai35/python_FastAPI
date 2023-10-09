from sqlalchemy.orm import joinedload, Session
from models.models import Book, Author, Category
from fastapi import HTTPException


def get_books_by_author(author_id: int, db):
    books = db.query(Book).filter(Book.authors.any(Author.id == author_id)).all()
    return books


def get_author_by_name(author_name: str, db):
    author = (
        db.query(Author)
        .filter(Author.name.ilike(f"%{author_name}%"))
        .options(joinedload(Author.books))
        .first()
    )
    return author


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
            })
        categories_with_count.append({"category": category.name, "books": books_info})
    return categories_with_count


def add_category(category_name: str, db: Session):
    new_category = Category(name=category_name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


def delete_category(category_name: str, db: Session):
    category = db.query(Category).filter(Category.name.ilike(f"%{category_name}%")).first()
    if category:
        db.delete(category)
        db.commit()
        return {"message": f"Category {category_name} deleted successfully"}
    return {"message": "Category not found"}


def update_category(category_name: str, new_name: str, db: Session):
    category = db.query(Category).filter(Category.name.ilike(f"%{category_name}%")).first()
    if category:
        category.name = new_name
        db.commit()
        db.refresh(category)
        return category
    return {"message": "Category not found"}

def add_book(title: str, isbn: str, pageCount: int, publishedDate: str, category_name: str, db: Session):
    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        category = Category(name=category_name)
        db.add(category)
        db.commit()
        db.refresh(category)

    new_book = Book(title=title, isbn=isbn, pageCount=pageCount, publishedDate=publishedDate)
    new_book.categories.append(category)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def delete_book(title: str, db: Session):
    book = db.query(Book).filter(Book.title.ilike(f"%{title}%")).first()
    if book:
        db.delete(book)
        db.commit()
        return {"message": f"Book {title} deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Book with title '{title}' not found")

def update_book(title: str, new_title: str, new_isbn: str, new_pageCount: int, new_publishedDate: str, db: Session):
    book = db.query(Book).filter(Book.title.ilike(f"%{title}%")).first()
    if book:
        book.title = new_title
        book.isbn = new_isbn
        book.pageCount = new_pageCount
        book.publishedDate = new_publishedDate
        db.commit()
        db.refresh(book)
        return book
    return {"message": "Book not found"}

def add_author(name: str, db: Session):
    new_author = Author(name=name)
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author

def delete_author(name: str, db: Session):
    author = db.query(Author).filter(Author.name.ilike(f"%{name}%")).first()
    if author:
        db.delete(author)
        db.commit()
        return {"message": f"Author {name} deleted successfully"}
    return {"message": "Author not found"}

def update_author(name: str, new_name: str, db: Session):
    author = db.query(Author).filter(Author.name.ilike(f"%{name}%")).first()
    if author:
        author.name = new_name
        db.commit()
        db.refresh(author)
        return author
    return {"message": "Author not found"}