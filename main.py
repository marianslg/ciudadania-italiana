from datetime import datetime, timedelta
import random
from log import save_file, save_log
import time
from driver import SeleniumDriver
from decorators import log, try_except
from popup import showPopup

TRYES = 10
PRENOTAME_USER_AREA_URL = 'https://prenotami.esteri.it/UserArea'
PRENOTAME_BOOKING_URL = 'https://prenotami.esteri.it/Services/Booking/224'


def start():
    driver = SeleniumDriver()

    time  = datetime.now()

    while True:
        try:
            programm_execution(time, process2, driver)

            time = calculate_new_execution_time(10, 40)
            save_log(f'Next execution time: {time}')
        except Exception as e:
            save_log(f'Error: {e}')



@log
@try_except
def process2(driver: SeleniumDriver):
    id = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    driver.go_to_url(PRENOTAME_USER_AREA_URL)

    if driver.need_login():
        driver.login()

    wait_until_7()

    for i in range(1, TRYES+1):
        driver.execute_script(PRENOTAME_BOOKING_URL)
    
    # for i in range(6*10):
    #     for e in range(1, TRYES+1):
    #         # Cambia a la nueva pestaña
    #         print(1)
    #         driver.change_tab(e)
    #         print(2)
    #         time.sleep(1)
    #         print(3)
    #         driver.save_screenshot(f'TAB_{id}_', 'PRENOTAME_BOOKING_URL')
    #         print(4)


        # Toma una captura de la segunda página
        # driver.save_screenshot("captura_pagina2.png")

    # driver.go_to_url(PRENOTAME_BOOKING_URL)

    time.sleep(60*10)

    # jconfirm-box85508

    # driver.wait_for_load()

    # if not driver.are_there_turns():
    #     save_log("Sin turnos")
    #     return
    #     # showPopup("prenotami", "Sin turnos")

    # driver.save_screenshot(id, 'PRENOTAME_BOOKING_URL')
    # showPopup("prenotami", "Con turno!")

@log
@try_except
def process(driver: SeleniumDriver):
    id = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    driver.go_to_url(PRENOTAME_USER_AREA_URL)

    if driver.need_login():
        driver.login()

    if is_the_time_close():
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

def is_the_time_close():
    actual_time = datetime.now()

    print(f'Actual time: {actual_time}')
    print(actual_time.hour, actual_time.minute)
    return actual_time.hour == 18 and actual_time.minute > 56

def wait_until_7():
    actual_time = datetime.now()
    hora_objetivo = datetime.combine(actual_time.date(), datetime.min.time()) + timedelta(hours=18, minutes=59, seconds=58)
    diferencia = (hora_objetivo - actual_time).total_seconds()
    save_log(f'Voy a dormir {diferencia} segundos hasta las {hora_objetivo}')
    time.sleep(diferencia)
   


start()
