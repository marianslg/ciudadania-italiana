from dotenv import dotenv_values

config = dotenv_values(".env")

EMAIL = config.get("EMAIL")
PRENOTAME_PASSWORD = config.get("PRENOTAME_PASSWORD")
EMAIL_PASSWORD = config.get("EMAIL_PASSWORD")

PRENOTAME_USER_AREA_URL = config.get("PRENOTAME_USER_AREA_URL")
PRENOTAME_BOOKING_URL = config.get("PRENOTAME_BOOKING_URL")
TEXT_NOT_TURNS = config.get("TEXT_NOT_TURNS")
TEXT_NOT_TURNS_ID = config.get("TEXT_NOT_TURNS_ID")
TEXT_TURN_ID = config.get("TEXT_TURN_ID")
ERROR_ID = config.get("ERROR_ID")
TIMEOUT = int(config.get("TIMEOUT"))
SLEEP_EVERY_TAB = float(config.get("SLEEP_EVERY_TAB"))
NOTE = config.get("NOTE")