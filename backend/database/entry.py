from datetime import datetime
from sqlalchemy import DateTime, Integer, Column, String, Boolean
from backend.database.base_class import BaseSql

class ParkingEntry(BaseSql):
    __tablename__ = "parking_entries"

    id = Column(Integer, nullable = False, primary_key = True, autoincrement = True)
    entry_time = Column(DateTime, nullable = False)
    exit_time = Column(DateTime)
    registration_plate = Column(String, nullable = False)
    is_paid = Column(Boolean, nullable=False, default=False)

    def __init__(
        self,
        registration_plate
    ):
        self.registration_plate = registration_plate
        self.entry_time = datetime.now()
