from datetime import datetime, timedelta
import random
from log import save_file, save_log
import time
from driver import SeleniumDriver
from decorators import log, try_except
from popup import showPopup


PRENOTAME_USER_AREA_URL = 'https://prenotami.esteri.it/UserArea'
PRENOTAME_BOOKING_URL = 'https://prenotami.esteri.it/Services/Booking/224'


def start():
    driver = SeleniumDriver()

    while True:
        try:
            time = calculate_new_execution_time(10, 40)
            save_log(f'Next execution time: {time}')
            programm_execution(time, process, driver)
        except Exception as e:
            save_log(f'Error: {e}')


@log
@try_except
def process(driver: SeleniumDriver):
    id = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    driver.go_to_url(PRENOTAME_USER_AREA_URL)

    if driver.need_login():
        driver.login()

    wait_until_7()

    driver.go_to_url(PRENOTAME_BOOKING_URL)

    # jconfirm-box85508

    driver.wait_for_load()

    if not driver.are_there_turns():
        save_log("Sin turnos")
        return
        # showPopup("prenotami", "Sin turnos")

    driver.save_screenshot(id, 'PRENOTAME_BOOKING_URL')
    showPopup("prenotami", "Con turno!")


def calculate_new_execution_time(min_seconds, max_seconds) -> datetime:
    random_seconds = random.randint(min_seconds, max_seconds)

    now = datetime.now()

    future_time = now + timedelta(seconds=random_seconds)

    return future_time


def programm_execution(execution_time, task, *args, **kwargs):
    now = datetime.now()

    wait_time = (execution_time - now).total_seconds()

    if wait_time > 0:
        time.sleep(wait_time)

    task(*args, **kwargs)

def wait_until_7():
    actual_time = datetime.now()

    print(f'Actual time: {actual_time}')
    print(actual_time.hour, actual_time.minute)
    if actual_time.hour == 18 and actual_time.minute > 56:
        hora_objetivo = datetime.combine(actual_time.date(), datetime.min.time()) + timedelta(hours=18, minutes=59, seconds=58)
        diferencia = (hora_objetivo - actual_time).total_seconds()
        save_log(f'Voy a dormir {diferencia} segundos')
        time.sleep(diferencia)
   


start()
