from app.memo import instance

class TABLE:
    LENDING = "LENDING"
    BOOK = "BOOK"
    ENVENTORY = "ENVENTORY"
    PAYMENT= "PAYMENT"
    USER = "USER"

def db(ctx):
    if ctx not in instance.memo:
        instance.memo[ctx] = {}
    return instance.memo[ctx]


def idgen() -> int:

    try:
        instance.memo["COUNTER"] = instance.memo["COUNTER"]  + 1
        return instance.memo["COUNTER"] 
    except:
        return 1