import os
from fastapi import APIRouter, HTTPException, status
from app.api_utils import as_dict
from app.dao import TABLE, db
from app.api_security import api_keys

route = APIRouter(prefix = "/api/v1/token")    #APİ ROUTERA route ile erişiyoruz ve arayüzdeki yolu route ile verioruz


@route.post("/generate", tags=["Authorization"])
def generate(username, password):
    
    for _, u in db(TABLE.USER).items():  #for dan  sonraki değişkenlr key (id) , value ise (u) oluyuor

        user  = as_dict(u)

        if username == user["username"] and password == user["password"]:
            
            #burada u ile user_map dictiıanrymiz yani veritabanımızdaki itemslerın valuesini yani usernmame ve passwwoprdu çağırıyoruz.
            yeni_token = os.urandom(32).hex()
            api_keys[yeni_token] = user
            return  yeni_token #os kütüphanesini import ettik ve rastgele id üretmesi için bu kodu kullandık

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )
