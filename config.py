from prettyconf import config


class Settings(object):
    SMTP_SERVER = config('SMTP_SERVER')
    SMTP_PORT = config('SMTP_PORT')
    SMTP_USER = config('SMTP_USER')
    SMTP_PASS = config('SMTP_PASS')
    SMTP_USE_TLS = config('SMTP_USE_TLS', default=True)

    EMAIL_FROM = config('EMAIL_FROM')
    EMAIL_TO = config('EMAIL_TO')
    EMAIL_SUBJECT = config('EMAIL_SUBJECT')

    CV2_CLASSIFIER = config('CV2_CLASSIFIER')
    CV2_SCALE_FACTOR = config('CV2_SCALE_FACTOR', default='1.1', cast=config.eval)
    CV2_MIN_NEIGHBORS = config('CV2_MIN_NEIGHBORS', default='5', cast=config.eval)

    CAMERA_RESOLUTION = config('CAMERA_RESOLUTION', cast=config.tuple)
    CAMERA_CAPTURE_INTERVAL = config('CAMERA_CAPTURE_INTERVAL', default='0', cast=config.eval)


settings = Settings()
