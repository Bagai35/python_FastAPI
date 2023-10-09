from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from cfg import get_db
from controllers.controllers import add_author, delete_author, update_author

router = APIRouter()

@router.post("/add")
def add_new_author(name: str, db: Session = Depends(get_db)):
    author = add_author(name, db)
    return author

@router.delete("/delete")
def delete_existing_author(name: str, db: Session = Depends(get_db)):
    result = delete_author(name, db)
    if "message" in result:
        raise HTTPException(status_code=404, detail=result["message"])
    return {"message": f"Author {name} deleted successfully"}

@router.put("/update")
def update_existing_author(name: str, new_name: str, db: Session = Depends(get_db)):
    author = update_author(name, new_name, db)
    if "message" in author:
        raise HTTPException(status_code=404, detail=author["message"])
    return author
