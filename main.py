from fastapi import FastAPI
from api.books import router as books_router
from api.authors import router as authors_router
from api.categories import router as categories_router

app = FastAPI()

app.include_router(books_router, prefix="/books", tags=["books"])
app.include_router(authors_router, prefix="/authors", tags=["authors"])
app.include_router(categories_router, prefix="/categories", tags=["categories"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Book API!"}

