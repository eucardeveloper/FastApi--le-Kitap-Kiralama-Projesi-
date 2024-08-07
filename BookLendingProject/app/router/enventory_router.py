from uuid import uuid4
from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.dao import TABLE, db, idgen
from app.models import Enventory, EnventoryRequest
from app.api_security import get_api_key, require_admin
from app.api_utils import as_dict, mapper, timestamp


route = APIRouter(prefix = "/api/v1/enventory", dependencies=[Depends(get_api_key)])

@route.post("/", tags=["Enventory"])   #data kaydetmek istiyorsan post
def add_enventory(request: EnventoryRequest, r: Request):

    operation_user = require_admin(r)

    be = mapper.map(request, Enventory)
    be.enventory_id = idgen()
    be.user_id = as_dict(operation_user)["user_id"]
    be.update_date = timestamp()
    
    db(TABLE.ENVENTORY)[str(be.enventory_id)] = be

    return be

@route.delete("/", tags=["Enventory"])   #data kaydetmek istiyorsan post
def remove_enventory(request: EnventoryRequest, r: Request):

    operation_user = require_admin(r)

    be = mapper.map(request, Enventory)
    be.quantity = -be.quantity
    be.enventory_id = idgen()
    be.user_id = as_dict(operation_user)["user_id"]
    be.update_date = timestamp()
    
    db(TABLE.ENVENTORY)[str(be.enventory_id)] = be

    return be


@route.get("/", tags=["Enventory"])   
def list_enventory(r: Request):

    operation_user = require_admin(r)

    return JSONResponse(content=jsonable_encoder(list(db(TABLE.ENVENTORY).values())), status_code=200)


@route.get("/{book_id:int}", tags=["Enventory"]) 
def get_book_enventory(book_id:int, r: Request):

    operation_user = require_admin(r)

    for book_enventory in db(TABLE.ENVENTORY).values():

        temp  = as_dict(book_enventory)

        if temp["book_id"] == book_id:
            return temp

    return None