from datetime import datetime
from pydantic import BaseModel

class CreateUserModel(BaseModel):
    username: str
    password: str
    email: str

class UserModel(BaseModel):
    email: str
    password: str

class UserDataModel(BaseModel):
    username: str = ""
    email: str
    registration_plates: list[str] = []

class CreatePlateModel(BaseModel):
    email: str
    registration_plate: str

class CreateEntryModel(BaseModel):
    registration_plate: str

class ExitEntryModel(BaseModel):
    registration_plate: str

class PayEntryModel(BaseModel):
    entry_id: int

class RegistrationModel(BaseModel):
    registration_plate: str

class EntryDataModel(BaseModel):
    id: int = 0
    entry_time: datetime = datetime.now()
    exit_time: datetime = datetime.now()
    is_paid: bool = False
    registration_plate: str
