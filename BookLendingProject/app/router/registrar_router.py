from uuid import uuid4 #Bu format normal bir id 'yi şifreleme gibi uzun  
from fastapi import APIRouter

from app.models import User, UserRequest
from app.dao import TABLE, db, idgen
from app.api_utils import mapper


route = APIRouter(prefix = "/api/v1/register")    #APİ ROUTERA route ile erişiyoruz ve arayüzdeki yolu route ile verioruz

@route.post("/customer", tags=["Registrar"])   #data kaydetmek istiyorsan post
def register(request:UserRequest):
    
    user = mapper.map(request, User)
    user.user_id = idgen()
    user.is_active = True
    user.role = "customer"

    db(TABLE.USER)[user.user_id] = user
    
    return user