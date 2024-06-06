import re
import PIL
import easyocr

from argparse import ArgumentParser

from parking_controls.backend_client.models.create_entry_model import CreateEntryModel
from parking_controls.backend_client.models.exit_entry_model import ExitEntryModel
from parking_controls.backend_client.api.default import create_new_entry_entry_in_post
from parking_controls.backend_client.api.default import entry_exit_entry_out_post
from parking_controls.backend_client import Client
from parking_controls.backend_client.types import Response

# Initialize the OCR reader
reader = easyocr.Reader(['en'], gpu=False)

def call_backend(client: Client, plate_text: str) -> Response:
    """
    Call backend service depending on what type of request we want

    Args:
        client (Client): Backend client
        plate_text (str): Registration plate

    Returns:
        Response: Response from backend
    """

    arg_parser = ArgumentParser(
    description="Parking controller"
    )

    arg_parser.add_argument(
        "--type",
        type=str,
        help="<REQUIRED> Type of parking controller used in simulation",
        required=True
    )

    args = arg_parser.parse_args()

    if args.type == "entrance":
        return create_new_entry_entry_in_post.sync_detailed(client=client, body=CreateEntryModel(plate_text))
    else:
        return entry_exit_entry_out_post.sync_detailed(client=client, body=ExitEntryModel(plate_text))

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

def read_license_plate(license_plate_crop: PIL.Image.Image) -> tuple:
    """
    Read the license plate text from the given cropped image.

    Args:
        license_plate_crop (PIL.Image.Image): Cropped image containing the license plate.

    Returns:
        tuple: Tuple containing the formatted license plate text and its confidence score.
    """

    detections = reader.readtext(license_plate_crop)

    for detection in detections:
        _, text, score = detection

        text = text.upper().replace(' ', '')

        if verify_registration_plate(text):
            return text, score

    return None, None
