from sqlalchemy import Column, ForeignKeyConstraint, String
from backend.database.base_class import BaseSql
from sqlalchemy.orm import relationship

class RegistrationPlate(BaseSql):
    __tablename__ = "registration_plates"

    plate_text = Column(String, nullable = False, primary_key = True)
    user_email = Column(String, nullable = False)

    user = relationship("User", back_populates="registration_plates")

    __table_args__ = (
        ForeignKeyConstraint(
            ["user_email"],
            ["users.user_email"]
        ),
    )

    def __init__(
        self,
        plate_text,
        user_email
    ):
        self.plate_text = plate_text
        self.user_email = user_email
