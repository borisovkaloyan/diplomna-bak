from datetime import datetime, timedelta
from backend.config import MAX_PARKING_HOURS
import backend.database.all_tables
from backend.database.entry import ParkingEntry
from backend.database.registration_plate import RegistrationPlate
from backend.database.user import User
from backend.database_service import DatabaseService
from backend.models import CreateEntryModel, CreatePlateModel, CreateUserModel, EntryDataModel, ExitEntryModel, PayEntryModel, RegistrationModel, UserDataModel, UserModel
from fastapi.responses import JSONResponse
from fastapi import status

import re

def create_new_user(create_user: CreateUserModel) -> JSONResponse:
    """
    Service for user creation

    Args:
        create_user (CreateUserModel): Required user data

    Returns:
        JSONResponse: Creation status
    """
    http_code = status.HTTP_201_CREATED
    message = "Created new user"

    # Check user is valid
    mail_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    session = DatabaseService.create_database_session()

    if not mail_regex.match(create_user.email):
        http_code = status.HTTP_400_BAD_REQUEST
        message = "Email is not valid"
    elif session.query(User).filter(User.user_email == create_user.email).first():
        http_code = status.HTTP_409_CONFLICT
        message = "Email already belongs to user"
    else:
        new_user = User(
            create_user.email,
            create_user.username,
            create_user.password
        )
        session.add(new_user)
        session.commit()

    session.close()

    return JSONResponse(
        status_code=http_code,
        content={"message": message}
    )

def get_user_data(user: UserModel) -> UserDataModel:
    """
    Service for getting user data

    Args:
        user (UserModel): User to get data for

    Returns:
        UserDataModel: User data
    """
    user_return_data = UserDataModel()
    session = DatabaseService.create_database_session()

    if user_database_data := session.query(User).filter(User.user_email == user.email).first():
        for plate in user_database_data.registration_plates:
            user_return_data.registration_plates.append(plate.plate_text)
        user_return_data.username = user_database_data.user_name
        user_return_data.email = user.email

    session.close()

    return user_return_data

def verify_registration_plate(registration_plate: str) -> bool:
    """
    Verification for plate validity

    Args:
        registration_plate (str): Plate to check

    Returns:
        bool: Validity status
    """
    plate_regex = re.compile(r"[A-Z]{2}\d{4}[A-Z]{2}")
    if plate_regex.match(registration_plate):
        return True
    return False

def create_new_plate(create_plate: CreatePlateModel) -> JSONResponse:
    """
    Service to create new license plate

    Args:
        create_plate (CreatePlateModel): Plate to create

    Returns:
        JSONResponse: Creation status
    """
    http_code = status.HTTP_201_CREATED
    message = "Created new registration plate"

    # Check validity
    session = DatabaseService.create_database_session()

    if not verify_registration_plate(create_plate.registration_plate):
        http_code = status.HTTP_400_BAD_REQUEST
        message = "Registration plate is not valid"
    elif not session.query(User).filter(User.user_email == create_plate.email).first():
        http_code = status.HTTP_400_BAD_REQUEST
        message = "User with that email is not registered"
    elif session.query(RegistrationPlate).filter(RegistrationPlate.plate_text == create_plate.registration_plate).first():
        http_code = status.HTTP_409_CONFLICT
        message = "Registration plate already belongs to user"
    else:
        new_plate = RegistrationPlate(
            create_plate.registration_plate,
            create_plate.email
        )
        session.add(new_plate)
        session.commit()

    session.close()

    return JSONResponse(
        status_code=http_code,
        content={"message": message}
    )

def create_new_entry(create_entry: CreateEntryModel) -> JSONResponse:
    """
    Service to create new parking entry

    Args:
        create_entry (CreateEntryModel): Required creation data

    Returns:
        JSONResponse: Creation status
    """
    http_code = status.HTTP_201_CREATED
    message = "Created new parking entry"

    session = DatabaseService.create_database_session()

    if not verify_registration_plate(create_entry.registration_plate):
        http_code = status.HTTP_400_BAD_REQUEST
        message = "Registration plate is not valid"
    elif not session.query(RegistrationPlate).filter(RegistrationPlate.plate_text == create_entry.registration_plate).first():
        http_code = status.HTTP_400_BAD_REQUEST
        message = "Registration plate not registered"
    elif session.query(ParkingEntry).filter(
        (ParkingEntry.registration_plate == create_entry.registration_plate) &
        (ParkingEntry.exit_time == None)).first():
        http_code = status.HTTP_409_CONFLICT
        message = "Vehicle with this registration is already parked"
    elif session.query(ParkingEntry).filter(
        (ParkingEntry.registration_plate == create_entry.registration_plate) &
        (ParkingEntry.exit_time != None) &
        (ParkingEntry.is_paid == False)).first():
        http_code = status.HTTP_402_PAYMENT_REQUIRED
        message = "Previous parking has not been paid. Vehilcle cannot enter"
    else:
        new_park = ParkingEntry(
            create_entry.registration_plate
        )
        session.add(new_park)
        session.commit()

    session.close()

    return JSONResponse(
        status_code=http_code,
        content={"message": message}
    )

def entry_exit(exit_entry: ExitEntryModel) -> JSONResponse:
    """
    Service to update entry with exit status

    Args:
        exit_entry (ExitEntryModel): Required data for exit

    Returns:
        JSONResponse: Exit status
    """
    http_code = status.HTTP_200_OK
    message = "Exited Successfully"

    session = DatabaseService.create_database_session()

    if not verify_registration_plate(exit_entry.registration_plate):
        http_code = status.HTTP_400_BAD_REQUEST
        message = "Registration plate is not valid"
    elif not session.query(RegistrationPlate).filter(RegistrationPlate.plate_text == exit_entry.registration_plate).first():
        http_code = status.HTTP_400_BAD_REQUEST
        message = "Registration plate not registered"
    else:
        last_park = session.query(ParkingEntry).filter(
            (ParkingEntry.registration_plate == exit_entry.registration_plate) &
            (ParkingEntry.exit_time == None)).first()

        if last_park:
            last_park.exit_time = datetime.now()

            time_parked: timedelta = last_park.exit_time - last_park.entry_time

            # Check if time parked is more than MAX_PARKING_HOURS hours, converted to seconds
            if time_parked.seconds < (MAX_PARKING_HOURS*60*60):
                last_park.is_paid = True

            session.add(last_park)
            session.commit()
        else:
            http_code = status.HTTP_409_CONFLICT
            message = "Vehicle with this registration has never parked"

    session.close()

    return JSONResponse(
        status_code=http_code,
        content={"message": message}
    )

def pay_entry(pay_entry: PayEntryModel) -> JSONResponse:
    """
    Service for entry payment

    Args:
        pay_entry (PayEntryModel): Required data for payment

    Returns:
        JSONResponse: Payment status
    """
    http_code = status.HTTP_200_OK
    message = "Paid Successfully"

    session = DatabaseService.create_database_session()

    entry_to_be_paid = session.query(ParkingEntry).filter(ParkingEntry.id == pay_entry.entry_id).first()

    if not entry_to_be_paid:
        http_code = status.HTTP_400_BAD_REQUEST
        message = "Could not find parking entry with such ID"
    else:
        if entry_to_be_paid.is_paid == True:
            http_code = status.HTTP_202_ACCEPTED
            message = "Entry is already paid"
        else:
            entry_to_be_paid.is_paid = True
            session.add(entry_to_be_paid)
            session.commit()

    session.close()

    return JSONResponse(
        status_code=http_code,
        content={"message": message}
    )

def get_entry_data(registration: RegistrationModel) -> list[EntryDataModel]:
    """
    Service to get data for entry

    Args:
        registration (RegistrationModel): Plate for which to get data

    Returns:
        list[EntryDataModel]: List of entry data
    """
    entries = []

    session = DatabaseService.create_database_session()

    registration_entries = session.query(ParkingEntry).filter(ParkingEntry.registration_plate == registration.registration_plate).all()
    for entry in registration_entries:
        entry_data = EntryDataModel()

        entry_data.id = entry.id
        entry_data.entry_time = entry.entry_time
        entry_data.exit_time = entry.exit_time
        entry_data.is_paid = entry.is_paid
        entry_data.registration_plate = registration.registration_plate

        entries.append(entry_data)

    session.close()

    return entries
