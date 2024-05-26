from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from backend.database.base_class import BaseSql

class User(BaseSql):
    __tablename__ = "users"

    user_email = Column(String, nullable = False, primary_key = True)
    user_name = Column(String, nullable = False)
    password = Column(String, nullable = False)

    registration_plates = relationship("RegistrationPlate", back_populates="user")

    def __init__(
        self,
        user_email,
        user_name,
        password
    ):
        self.user_email = user_email
        self.user_name = user_name
        self.password = password