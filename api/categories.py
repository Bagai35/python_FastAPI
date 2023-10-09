from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from cfg import SessionLocal
from controllers.controllers import add_category, delete_category, update_category

router = APIRouter()

@router.post("/add")
def add_new_category(name: str, db: Session = Depends(SessionLocal)):
    category = add_category(name, db)
    return category

@router.delete("/delete")
def delete_existing_category(name: str, db: Session = Depends(SessionLocal)):
    result = delete_category(name, db)
    if "message" in result:
        raise HTTPException(status_code=404, detail=result["message"])
    return {"message": f"Category {name} deleted successfully"}

@router.put("/update")
def update_existing_category(name: str, new_name: str, db: Session = Depends(SessionLocal)):
    category = update_category(name, new_name, db)
    if "message" in category:
        raise HTTPException(status_code=404, detail=category["message"])
    return category
