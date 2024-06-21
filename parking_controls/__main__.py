from http import HTTPStatus
import time
from ultralytics import YOLO

import cv2
import json
import parking_controls.utils as utils

from parking_controls.backend_client import Client
from parking_controls.backend_client.types import Response

# Load backend client
client = Client("http://34.118.78.253")

# Store results here
results = {}

# Config
nano = True
resize = True
active_backend = True

# Load models
if nano:
    license_plate_detector = YOLO('./parking_controls/plate_model_light.pt')
    min_confidence = 0.32
else:
    license_plate_detector = YOLO('./parking_controls/plate_model.pt')
    min_confidence = 0.3

# Load video
cap = cv2.VideoCapture('./parking_controls/test_video.mp4')

# Frame management
frame_nmr = -1
ret = True

# Best output so far
best_text = ""
best_score = 0.0

# Backend stuff
try_backend = True
backend_message = ""

# Main video loop
with client as client:
    while ret:
        frame_nmr += 1
        ret, frame = cap.read()
        if ret:
            results[frame_nmr] = {}
            detections = license_plate_detector(frame, iou=0.1)[0]

            for plate in detections.boxes.data.tolist():
                x1, y1, x2, y2, score, _ = plate

                if score > min_confidence:

                    print(f"Detection confidence: {score}")

                    license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]
                    if resize:
                        license_plate_crop = cv2.resize(license_plate_crop, (150, 40))

                    license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                    _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)

                    plate_height, plate_width = license_plate_crop_thresh.shape

                    license_plate_text, license_plate_text_score = utils.read_license_plate(license_plate_crop_thresh)

                    print(f"Text: {license_plate_text} Score: {license_plate_text_score}")

                    if license_plate_text_score and license_plate_text_score > best_score:
                        best_text = license_plate_text
                        best_score = license_plate_text_score

                    print(f"Best Text: {best_text} Best Score: {best_score}")

                    if best_score > 0.8 and try_backend:
                        try_backend = False
                        if active_backend:
                            response: Response = utils.call_backend(client, best_text)
                            print(f"Backend response: {response}")
                            if (response.status_code == HTTPStatus.CREATED) or (response.status_code == HTTPStatus.OK):
                                door_message = "Barrier lifted!"
                            else:
                                door_message = "Barrier closed!"
                            backend_message = "Backend response: " + str(json.loads(response.content.decode("utf-8"))["message"])

                    if backend_message:
                        cv2.putText(
                            frame,
                            backend_message,
                            (40, 180 + plate_height),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (255, 255, 255),
                            2
                        )
                        cv2.putText(
                            frame,
                            door_message,
                            (40, 220 + plate_height),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (255, 255, 255),
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
                            (255, 255, 255),
                            2
                        )
                        cv2.putText(
                            frame,
                            f"Confidence: {round(best_score, 2)}",
                            (40, 140 + plate_height),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (255, 255, 255),
                            2
                        )

            cv2.imshow('frame', frame)
            cv2.waitKey(1)
