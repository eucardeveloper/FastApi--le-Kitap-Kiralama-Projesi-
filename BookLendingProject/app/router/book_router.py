import json
from uuid import uuid4
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.api_security import get_api_key, require_admin, require_authenticated
from app.models import Book, BookRequest
from app.dao import TABLE, db, idgen
from app.api_utils import as_dict, mapper

route = APIRouter(prefix="/api/v1/book", dependencies=[Depends(get_api_key)])


@route.post("/", tags=["Book"])  # data kaydetmek istiyorsan post
def add_book(request: BookRequest, r: Request):

    operation_user = require_admin(r)

    book = mapper.map(request, Book)
    book.book_id = idgen()
    book.user_id = as_dict(operation_user)["user_id"]

    db(TABLE.BOOK)[str(book.book_id)] = book

    return book


# data sorgulamak istiyorsan get
@route.get("/find", tags=["Book"])
def find_book(book_id: str, r: Request):

    return db(TABLE.BOOK)[book_id]


@route.delete("/{book_id}", tags=["Book"])  # data silmek istiyorsan delete
def remove_book(book_id: str, r: Request):

    operation_user = require_admin(r)

    book: Book = db(TABLE.BOOK)[book_id]
    del db(TABLE.BOOK)[book_id]

    return {"status": "done", "deleted": book}


@route.get("/", tags=["Book"])  # data sorgulamak istiyorsan get
def list_books(r: Request):

    return JSONResponse(content=jsonable_encoder(list(db(TABLE.BOOK).values())), status_code=200)


@route.get("/search", tags=["Book"])  # data sorgulamak istiyorsan get
# None textboxdaki zorunlu girişi kaldırmak için yani kırmızu yıldız için kullanıldı
def search(r: Request, author: str = None, isbn: str = None, title: str = None):

    hits = []
    for book in db(TABLE.BOOK).values():

        temp = as_dict(book)

        if (author is not None and author in temp["author"]) or (isbn is not None and isbn == temp["isbn"]) or (title is not None and title in temp["title"]):

            hits.append(book)

    return {"hits": hits}
