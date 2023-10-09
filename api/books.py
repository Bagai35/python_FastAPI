from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from cfg import get_db
from controllers.controllers import add_book, delete_book, update_book

router = APIRouter()


@router.post("/add")
def add_new_book(title: str, isbn: str, pageCount: int, publishedDate: str, category_name: str, db: Session = Depends(get_db)):
    book = add_book(title, isbn, pageCount, publishedDate, category_name, db)
    return book


@router.delete("/delete")
def delete_existing_book(title: str, db: Session = Depends(get_db)):
    result = delete_book(title, db)
    if "message" in result:
        raise HTTPException(status_code=404, detail=result["message"])
    return {"message": f"Book {title} deleted successfully"}


@router.put("/update")
def update_existing_book(title: str, new_title: str, new_isbn: str, new_pageCount: int, new_publishedDate: str, db: Session = Depends(get_db)):
    book = update_book(title, new_title, new_isbn, new_pageCount, new_publishedDate, db)
    if "message" in book:
        raise HTTPException(status_code=404, detail=book["message"])
    return book
