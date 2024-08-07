import datetime
from uuid import uuid4
from fastapi import APIRouter, Depends, Request
from app.api_security import get_api_key, require_customer
from app.api_utils import as_dict, timestamp
from app.models import EnventoryRequest, Lending, LendingRequest, Payment

from app.router.enventory_router import get_book_enventory, remove_enventory
from app.dao import TABLE, db, idgen
from app.api_security import api_keys
from app.api_utils import as_dict, mapper

route = APIRouter(prefix="/api/v1/lending",
                  dependencies=[Depends(get_api_key)])


@route.post("/order", tags=["Lending"])
def make_lending_order(request: LendingRequest, r: Request):

    operation_user = require_customer(r)

    lending = mapper.map(request, Lending)

    book = as_dict(db(TABLE.BOOK)[str(request.book_id)])

    be = None
    for book_enventory in db(TABLE.ENVENTORY).values():

        temp = as_dict(book_enventory)

        if temp["book_id"] == request.book_id:
            be = temp

    if be["quantity"] > 0:

        payment = create_payment(request.card_no, request.cvc, request.skt)

        lending_fee = book["price"] * request.lending_period

        user_id = as_dict(operation_user)["user_id"]

        be["book_id"] = request.book_id
        be["quantity"] = -1
        be["enventory_id"] = idgen()
        be["user_id"] = user_id
        be["update_date"] = timestamp()

        db(TABLE.ENVENTORY)[str(be["enventory_id"])] = be

        lending.lending_id = idgen()
        lending.lending_date = datetime.date.today().strftime("%d-%m-%Y")
        lending.book_id = request.book_id
        lending.user_id = user_id
        lending.lending_period = request.lending_period
        lending.total_fee = lending_fee
        lending.payment_id = payment["payment_id"]

        db(TABLE.LENDING)[str(lending.lending_id)] = lending

    else:
        return {"status": "kitap stok durumu yetersiz"}

    return lending


@route.get("/{customer_id}", tags=["Lending"])
def list_lended_books(customer_id: str):
    # TODO implement
    return None


@route.post("/return-book", tags=["Lending"])
def return_book(book_id: str, quantity: int):
    # TODO implement
    return None


def create_payment(cc, cvc, skt):

    payment = Payment()
    payment.card_no = cc
    payment.cvc = cvc
    payment.skt = skt
    payment.payment_id = idgen()

    db(TABLE.PAYMENT)[str(payment.payment_id)] = payment

    return as_dict(payment)
