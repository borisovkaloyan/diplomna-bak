from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from backend.models import CreateEntryModel, CreatePlateModel, CreateUserModel, EntryDataModel, ExitEntryModel, PayEntryModel, RegistrationModel, UserDataModel, UserModel
import backend.service as service

router = APIRouter()

@router.post(
    "/users/new",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Created new user",
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid data provided for user",
        },
        status.HTTP_409_CONFLICT: {
            "description": "User with provided data already exists",
        }
    }
)
async def create_new_user(create_user: CreateUserModel) -> JSONResponse:
    """
    Creates a new user

    Args:
        create_user (CreateUserModel): Data

    Returns:
        JSONResponse: Response
    """
    return service.create_new_user(create_user)

@router.get(
    "/users/data",
    responses={
        status.HTTP_200_OK: {
            "description": "Got user data",
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid data provided for user",
        }
    }
)
async def get_user_data(user: UserModel) -> UserDataModel:
    """
    Gets user data

    Args:
        user (UserModel): Input data

    Returns:
        UserDataModel: User data
    """
    return service.get_user_data(user)

@router.post(
    "/plates/new",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Created new registration plate",
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid data provided",
        },
        status.HTTP_409_CONFLICT: {
            "description": "Plate with provided data already exists",
        }
    }
)
async def create_new_plate(create_plate: CreatePlateModel) -> JSONResponse:
    """
    Creates a new registration plate

    Args:
        create_plate (CreatePlateModel): Data

    Returns:
        JSONResponse: Response
    """
    return service.create_new_plate(create_plate)

@router.post(
    "/entry/in",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Created new parking entry",
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid data",
        },
        status.HTTP_409_CONFLICT: {
            "description": "Plate with provided data already parked",
        },
        status.HTTP_402_PAYMENT_REQUIRED: {
            "description": "Previous parking has not been paid. Vehilcle cannot enter"
        }
    }
)
async def create_new_entry(create_entry: CreateEntryModel) -> JSONResponse:
    """
    Creates a new parking entry

    Args:
        create_entry (CreateEntryModel): Data

    Returns:
        JSONResponse: Response
    """
    return service.create_new_entry(create_entry)

@router.post(
    "/entry/out",
    responses={
        status.HTTP_200_OK: {
            "description": "Exited successfully",
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid data",
        },
        status.HTTP_409_CONFLICT: {
            "description": "Plate with provided data never parked",
        },
    }
)
async def entry_exit(exit_entry: ExitEntryModel) -> JSONResponse:
    """
    Exit entered car

    Args:
        exit_entry (ExitEntryModel): Data

    Returns:
        JSONResponse: Response
    """
    return service.entry_exit(exit_entry)

@router.post(
    "/entry/pay",
    responses={
        status.HTTP_200_OK: {
            "description": "Paid successfully",
        },
        status.HTTP_202_ACCEPTED: {
            "description": "Entry already paid",
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid data",
        }
    }
)
async def pay_entry(pay_entry: PayEntryModel) -> JSONResponse:
    """
    Pay exited car to allow next entry

    Args:
        pay_entry (PayEntryModel): Data

    Returns:
        JSONResponse: Response
    """
    return service.pay_entry(pay_entry)

@router.get(
    "/entry/data",
    responses={
        status.HTTP_200_OK: {
            "description": "Got entry data",
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid data provided for entry",
        }
    }
)
async def get_entry_data(registration: RegistrationModel) -> list[EntryDataModel]:
    """
    Gets entry data

    Args:
        registration (RegistrationModel): Input data

    Returns:
        list[EntryDataModel]: Entry data
    """
    return service.get_entry_data(registration)
