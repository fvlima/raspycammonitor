from __future__ import print_function

import io
import os
import picamera
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from pathlib import Path

import cv2
import numpy

from config import settings


BASE_DIR = Path(__file__).absolute().parent
PICS_DIR = '{}/pics'.format(BASE_DIR)


def create_msg(image_path):
    msg = MIMEMultipart()
    msg['Subject'] = settings.EMAIL_SUBJECT
    msg['From'] = settings.EMAIL_FROM
    msg['To'] = settings.EMAIL_TO

    mime = MIMEBase('application', 'octet-stream')
    with open(image_path, 'rb') as image:
        mime.set_payload(image.read())

    encoders.encode_base64(mime)
    filename = image_path.split('/')[-1]

    mime.add_header('Content-Disposition', 'attachment; filename={}'.format(filename))
    msg.attach(mime)

    return msg


def send_email(image_path):
    msg = create_msg(image_path)
    smtp = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
    if settings.SMTP_USE_TLS:
        smtp.ehlo()
        smtp.starttls()
    smtp.login(settings.SMTP_USER, settings.SMTP_PASS)
    smtp.sendmail(settings.EMAIL_FROM, settings.EMAIL_TO, msg.as_string())
    smtp.quit()


def get_image_name():
    name = datetime.now().strftime('%Y%m%d%H%M%S')
    return '{}/{}.jpg'.format(PICS_DIR, name)


def create_image(image):
    image_name = get_image_name()
    if not os.path.exists(PICS_DIR):
        os.makedirs(PICS_DIR)

    cv2.imwrite(image_name, image)
    return image_name


def analyze_image(buffer):
    img_array = numpy.fromstring(buffer.getvalue(), dtype=numpy.uint8)
    image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    classifier = cv2.CascadeClassifier(settings.CV2_CLASSIFIER)
    gray_color = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    detection = classifier.detectMultiScale(
        gray_color,
        settings.CV2_SCALE_FACTOR,
        settings.CV2_MIN_NEIGHBORS
    )

    if isinstance(detection, numpy.ndarray):
        image_name = create_image(image)
        send_email(image_name)
        print('Found', image_name)


def take_snapshot(camera):
    buffer = io.BytesIO()
    camera.capture(buffer, format='jpeg')
    analyze_image(buffer)
    buffer.close()


def main():
    monitoring = True
    with picamera.PiCamera() as camera:
        camera.resolution = tuple(int(r) for r in settings.CAMERA_RESOLUTION)
        while monitoring:
            try:
                time.sleep(settings.CAMERA_CAPTURE_INTERVAL)
                take_snapshot(camera)
            except KeyboardInterrupt:
                monitoring = False
                print('Bye')


if __name__ == '__main__':
    main()
