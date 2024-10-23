from datetime import datetime, timedelta
import random
from log import save_log, save_result_operation, get_result_operation
import time
from driver import SeleniumDriver, next_service, Service
from decorators import log, try_except
from popup import showPopup

TRYES = 5
PRENOTAME_USER_AREA_URL = 'https://prenotami.esteri.it/UserArea'
PRENOTAME_BOOKING_URL = 'https://prenotami.esteri.it/Services/Booking/224'
TEXT_NOT_TURNS = 'i posti disponibili per il servizio scelto sono esauriti'
TEXT_NOT_TURNS_ID = 'WlNotAvailable'
TEXT_TURN_ID = 'typeofbookingddl'
TIMEOUT = 180


def start_process_day():
    service = Service.CHROME
    while True:
        try:
            driver = SeleniumDriver(TIMEOUT, service=service)
            service = next_service[service]

            process(driver)

        except Exception as e:
            print(f'Error: {e}')

        wait(10, 40)


def start_process_7():
    import multiprocessing

    try:
        p1 = multiprocessing.Process(target=process2, args=(Service.CHROME,))
        p2 = multiprocessing.Process(target=process2, args=(Service.EDGE,))

        # Iniciar procesos
        p1.start()
        p2.start()

        # Esperar a que los procesos terminen
        p1.join()
        p2.join()

    except Exception as e:
        print(f'Error: {e}')


@log
@try_except
def process2(service: Service):
    print(service.name)
    driver = SeleniumDriver(TIMEOUT, service=service)

    id = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    login_and_service(driver)

    driver.click_prenota()
    driver.wait_for_load_fully()

    wait_until_7()

    driver.click_prenota()

    for i in range(1, TRYES+1):
        time.sleep(0.2)
        driver.open_tab(PRENOTAME_BOOKING_URL)

    time.sleep(60*10)

    for e in range(1, TRYES+1):
        driver.change_tab(e)
        driver.save_screenshot(f'TAB_{e}_{service.name}_{id}_', 'PRENOTAME_BOOKING_URL')

    # for i in range(6*10):
    #     for e in range(1, TRYES+1):
    #         driver.change_tab(e)
    #         if driver.is_load():
    #             driver.save_screenshot(f'TAB_{service.name}_{id}_', 'PRENOTAME_BOOKING_URL')

        # Toma una captura de la segunda página
        # driver.save_screenshot("captura_pagina2.png")

    # driver.go_to_url(PRENOTAME_BOOKING_URL)

    # time.sleep(60*1000)

    # jconfirm-box85508

    # driver.wait_for_load_fully()

    # if not driver.are_there_turns():
    #     save_log("Sin turnos")
    #     return
    #     # showPopup("prenotami", "Sin turnos")

    # driver.save_screenshot(id, 'PRENOTAME_BOOKING_URL')
    # showPopup("prenotami", "Con turno!")

# @log
# @try_except


def login_and_service(driver: SeleniumDriver):
    driver.go_to_url(PRENOTAME_USER_AREA_URL)

    if driver.need_login():
        time.sleep(2)
        driver.login()

    time.sleep(5)
    driver.click_services()
    driver.wait_for_load_fully()
    time.sleep(5)


def process(driver: SeleniumDriver):
    from selenium.common.exceptions import TimeoutException

    _id = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    _date = _id.split()[0]
    _time = _id.split()[1]
    _result = None

    try:
        login_and_service(driver)

        driver.click_prenota()
        driver.wait_for_load_fully()
        time.sleep(5)

        if driver.exists_id(TEXT_TURN_ID):
            save_log("Con turnos!")
            driver.save_screenshot(_id, 'PRENOTAME_BOOKING_URL')
            _result = 'OK'
            # showPopup("prenotami", "Con turno!")
        elif driver.exists_id(TEXT_NOT_TURNS_ID):
            save_log("Sin turnos")
            _result = 'NO_TURNS'
            # showPopup("prenotami", "Sin turnos")
        else:
            _result = 'UNKNOWN'
    except TimeoutException:
        _result = 'TIMEOUT'
    except Exception as e:
        driver.save_screenshot(_id, 'Exception')
        _result = 'EXC'
        time.sleep(10)
    finally:
        driver.close()
        save_result_operation(_date, _time, _result, driver.service.name)
        print(get_result_operation())


def calculate_new_execution_time(min_seconds, max_seconds) -> datetime:
    random_seconds = random.randint(min_seconds, max_seconds)

    now = datetime.now()

    future_time = now + timedelta(seconds=random_seconds)

    return future_time


def wait(min, max):
    time.sleep(random.randint(min, max))


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
    hora_objetivo = datetime.combine(actual_time.date(
    ), datetime.min.time()) + timedelta(hours=18, minutes=59, seconds=58)
    diferencia = (hora_objetivo - actual_time).total_seconds()
    print(f'Voy a dormir {diferencia} segundos hasta las {hora_objetivo}')
    time.sleep(diferencia)
