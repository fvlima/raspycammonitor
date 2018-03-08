# raspycammonitor

A simple and experimental python script to run on raspberry, that uses picamera and opencv-python to detect human presence by face recognition, taking a photo and sending it through email. 

It uses the haar-cascade [1] classifier for face detection and some configurations to improve the classifier type and detection scale can be made by envvars configured in .env file.

1 - http://bit.ly/2FjyYB5

## Installation and usage

This project requires `pipenv`.

1. Clone the project `git clone https://github.com/fvlima/raspycammonitor.git`
2. `pipenv install` (if any error occurs, try `pipenv install --skip-lock`)
3. `cp default.env .env`
4. Edit the `.env` file with your email credentials and other configuration if necessary
5. Run `python monitor.py`


## Using as a background service

It's possible to configure it as a  service, to run in background and automatic launch on system boot, example:


Create the service file
```
vim /lib/systemd/system/raspycammonitor.service
```

Edit this file like the lines bellow (change the venv and project location)
```
[Unit]
Description=Raspberry Py Camera Monitor
After=multi-user.target

[Service]
Type=simple
ExecStart=/your/venv/path/bin/python /your/local/path/raspycammonitor/monitor.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

And run the follow comands in terminal (change the project location)

```
sudo chmod 644 /lib/systemd/system/raspycammonitor.service
chmod +x /your/local/path/raspycammonitor.py
sudo systemctl daemon-reload
sudo systemctl enable raspycammonitor.service
sudo systemctl start raspycammonitor.service
``` 

After it, the project is already ready to run. It's possible to see the service status with the follow command

```
sudo systemctl status raspycammonitor.service
```

More information about systemd can be found here https://wiki.debian.org/systemd

## Configuration file

Here the envvars configuration options are described
```
SMTP_SERVER=smtp.some-domain.com # the smtp server
SMTP_PORT=587 # the smtp port
SMTP_USER=user@some-domin.com # the user for smtp login
SMTP_PASS='password' # the user smtp password between single quotes
SMT_USE_TLS=True # if the smpt uses TLS or not

EMAIL_FROM=user@some-domin.com # the email that will send the captured image
EMAIL_TO=user@another-domin.com # the email that will receive the captured image
EMAIL_SUBJECT=Face detection # the email subject

CV2_CLASSIFIER=/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml # the classifier location
CV2_SCALE_FACTOR=1.1 # cv2 scale factor image detection
CV2_MIN_NEIGHBORS=5 # cv2 min neighbors image detection

CAMERA_RESOLUTION=1024,768 # the picamera resolution
CAMERA_CAPTURE_INTERVAL=2 # the interval in seconds between image capture 
``` 

## Notes

- This project was tested with python 2.7+ and 3.5+
- Maybe you need to install libopencv-dev
