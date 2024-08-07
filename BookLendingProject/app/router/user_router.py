from uuid import uuid4  # Bu format normal bir id 'yi şifreleme gibi uzun
from fastapi import APIRouter, Depends, HTTPException, status, Security
from app.api_security import get_api_key
from app.api_utils import as_dict
from app.models import User
from app.dao import TABLE, db


# APİ ROUTERA route ile erişiyoruz ve arayüzdeki yolu route ile verioruz
route = APIRouter(prefix="/api/v1/user", dependencies=[Depends(get_api_key)])
# GET_APİ_KEYİ EKLEDİK V DEPENDENCİES ÖZELLİĞİ İLE GET APİ KEYİ AKTİF ETTİK. VE BU SAYFADAKİ TÜM ROUTE İLE ÇALIŞAN ERİŞİLENLER BU GÜVENLİK SİSTEMİNE MARUZ KALACAK.


# data sorgulamak istiyorsan get
@route.get("/customer/{username}", tags=["User"])
def find(username: str):

    for user in db(TABLE.USER).values():

        temp = as_dict(user)

        if temp["username"] == username and temp["role"] == "customer":
            return temp

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Customer not found",
    )


# data silmek istiyorsan delete
@route.delete("/customer/{user_id}", tags=["User"])
def unregister(user_id: str):

    user: User = db(TABLE.USER)[user_id]

    temp = as_dict(user)

    if temp["role"] != "customer":
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized access",
    )

    temp["is_active"] = False

    return {"status": "done"}