from pydantic import BaseModel


class Book(object):
    def __init__(self):
        self.book_id: int = None
        self.isbn: str = None
        self.author: str = None
        self.title: str = None
        self.price: float = None
        self.user_id: str = None


class BookRequest(BaseModel):
    isbn: str
    author: str
    title: str
    price: float


class Enventory(object):
    def __init__(self):
        self.enventory_id: int = None
        self.book_id: int = None
        self.user_id: str = None
        self.quantity: int = None
        self.update_date: str = None


class EnventoryRequest(BaseModel):
    book_id: int
    quantity: int


class Payment(object):
    def __init__(self):
        self.payment_id: str = None
        self.card_no: str = None
        self.cvc: str = None
        self.skt: str = None


class User(object):
    def __init__(self):
        self.user_id: str = None
        self.username: str = None
        self.password: str = None
        self.name: str = None
        self.surname: str = None
        self.gsm_no: str = None
        self.location: str = None
        self.is_active: bool = None
        self.role: str = None


class UserRequest(BaseModel):
    username: str
    password: str
    name: str
    surname: str
    gsm_no: str
    location: str


class Lending(object):
    def __init__(self):
        self.lending_id: int = None
        self.user_id: int = None
        self.payment_id: int = None
        self.book_id: int = None
        self.lending_date: str = None
        self.lending_period: int = None
        self.total_fee: float = None
        

class LendingRequest(BaseModel):

    book_id: int = None
    lending_period: int = None
    card_no: str
    cvc: str
    skt: str
