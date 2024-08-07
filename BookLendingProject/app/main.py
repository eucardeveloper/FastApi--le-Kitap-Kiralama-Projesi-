from fastapi import FastAPI, Request
from pydantic import BaseConfig

from app.memo import instance
from app.router.book_router import route as book_router
from app.router.enventory_router import route as enventory_router    #router classlarına gidiyor çünkü main metodundan çalıştırıyoruz
from app.router.lending_router import route as lending_router
from app.router.user_router import route as user_router
from app.router.token_router import route as token_router
from app.router.registrar_router import route as registrar_router


app = FastAPI()

app.include_router(book_router)
app.include_router(enventory_router)
app.include_router(lending_router)
app.include_router(user_router)
app.include_router(token_router)
app.include_router(registrar_router)

BaseConfig.arbitrary_types_allowed = True


@app.on_event('startup')
def on_startup():
    instance.load_snapshot()

@app.middleware("http")
async def request_interceptor(request: Request, call_next):
    
    response = await call_next(request)
    instance.save_snapshot()
    
    return response

def start():
    return app
