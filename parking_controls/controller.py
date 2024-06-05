from http import HTTPStatus
from ultralytics import YOLO
import cv2

import easyocr
import json

from backend_client import Client
from backend_client.models import create_entry_model
from backend_client.api.default import create_new_entry_entry_in_post
from backend_client.types import Response

client = Client("http://34.118.78.253")

# Initialize the OCR reader
reader = easyocr.Reader(['en'], gpu=False)

results = {}

# load models
license_plate_detector = YOLO('./parking_controls/plate_model.pt')
import re
# load video
cap = cv2.VideoCapture('./parking_controls/test_video.mp4')


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

def read_license_plate(license_plate_crop):
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

frame_nmr = -1
ret = True
best_text = ""
best_score = 0.0
try_enter = True
backend_message = ""
with client as client:
    while ret:
        frame_nmr += 1
        ret, frame = cap.read()
        if ret:
            results[frame_nmr] = {}
            detections = license_plate_detector(frame)[0]

            for plate in detections.boxes.data.tolist():
                x1, y1, x2, y2, score, _ = plate
                if score > 0.3:

                    license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]
                    license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                    _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)

                    plate_height, plate_width = license_plate_crop_thresh.shape

                    license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_thresh)
                    print(f"Text: {license_plate_text} Score: {license_plate_text_score}")

                    if license_plate_text_score and license_plate_text_score > best_score:
                        best_text = license_plate_text
                        best_score = license_plate_text_score

                    print(f"Best Text: {best_text} Best Score: {best_score}")

                    if best_score > 0.8 and try_enter:
                        try_enter = False
                        response: Response = create_new_entry_entry_in_post.sync_detailed(client=client, body=create_entry_model.CreateEntryModel(best_text))
                        print(response)
                        if (response.status_code == HTTPStatus.CREATED) or (response.status_code == HTTPStatus.OK):
                            door_message = "Barrier lifted!"
                        else:
                            door_message = "Barrier closed!"
                        backend_message = json.loads(response.content.decode("utf-8"))["message"]

                    if backend_message:
                        cv2.putText(
                            frame,
                            backend_message,
                            (40, 180 + plate_height),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 0, 0),
                            2
                        )
                        cv2.putText(
                            frame,
                            door_message,
                            (40, 220 + plate_height),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 0, 0),
                            2
                        )

                    frame[ 40 : plate_height + 40, 40 : plate_width + 40, : ] = cv2.cvtColor(license_plate_crop_thresh,cv2.COLOR_GRAY2RGB)
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 5)
                    if best_score > 0.0:
                        cv2.putText(
                            frame,
                            f"Text: {best_text}",
                            (40, 100 + plate_height),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 0, 0),
                            2
                        )
                        cv2.putText(
                            frame,
                            f"Confidence: {round(best_score, 2)}",
                            (40, 140 + plate_height),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 0, 0),
                            2
                        )

            cv2.imshow('frame', frame)
            cv2.waitKey(1)
