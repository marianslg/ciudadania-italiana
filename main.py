from datetime import datetime, timedelta
import random
from log import save_log, save_result_operation, get_result_operation
import time
from driver import SeleniumDriver, next_service, Service
from decorators import log, try_except
from popup import showPopup
from enum import Enum

TRYES = 5
PRENOTAME_USER_AREA_URL = 'https://prenotami.esteri.it/UserArea'
PRENOTAME_BOOKING_URL = 'https://prenotami.esteri.it/Services/Booking/224'
TEXT_NOT_TURNS = 'i posti disponibili per il servizio scelto sono esauriti'
TEXT_NOT_TURNS_ID = 'WlNotAvailable'
TEXT_TURN_ID = 'typeofbookingddl'
ERROR_ID = 'error-information-popup-container'
TIMEOUT = 180
SLEEP_EVERY_TAB = 0.3

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
        p1 = multiprocessing.Process(
            target=process_seven, args=(Service.CHROME,))
        p2 = multiprocessing.Process(
            target=process_seven, args=(Service.EDGE,))

        p1.start()
        p2.start()

        p1.join()
        p2.join()

    except Exception as e:
        print(f'Error: {e}')

def print_execution(service, executions):
    for execution in executions:
        print(f"{service} Tab: {execution['tab']}, Start: {execution['start']}, Finish: {execution['finish']} result: {execution['result']}")

@try_except
def process_seven(service: Service):
    executions = []

    driver = SeleniumDriver(TIMEOUT, service=service)

    id = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if login_and_go_to_service(driver) == LoginResult.UNAVAILABLE:
        print(service.name, f'Unavailable')
        return

    # wait_until(18,59,58)
    wait_until(18,49,59)


    for i in range(1, TRYES+1):
        time.sleep(SLEEP_EVERY_TAB)
        executions.append({'tab': i, 'start': datetime.now(),
                          'finish': None, 'isFinished': False, 'result': None})
        driver.open_tab(PRENOTAME_BOOKING_URL)

    # driver.click_prenota()

    # time.sleep(60*10)
    print_execution(service.name, executions)

    for e in range(0, len(executions)):
        print(service.name, f'Execution {e}')
        if (not executions[e]['isFinished']):
            print(service.name,f'change_tab: {e}')
            driver.change_tab(e+1)
            print(service.name,f'change_tab end: {e}')

            if driver.is_load(1):
                print(service.name, f'if isload {e}')
                executions[e]['finish'] = datetime.now()
                executions[e]['isFinished'] = True
                executions[e]['result'] = get_result_prenota(driver).name
                driver.save_screenshot(f'{id}_TAB_{e}_{service.name}', '')
                print(service.name, f'if isload end {e}')

            time.sleep(1)
        
        if all(item['isFinished'] for item in executions):
            print(service.name, f'isFinished {e}')
            break
    
    print_execution(service.name, executions)

    time.sleep(10000)

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


class PRENOTA_RESULT(Enum):
    OK = 1
    ERROR_CONNECTION_RESET = 2
    NO_TURNS = 3
    UNKNOWN = 4



def get_result_prenota(driver: SeleniumDriver, timeout=0) -> PRENOTA_RESULT:
    if driver.exists_id(TEXT_TURN_ID, timeout):
        return PRENOTA_RESULT.OK
    elif driver.exists_id(TEXT_NOT_TURNS_ID, timeout):
        return PRENOTA_RESULT.NO_TURNS
    elif driver.exists_id(ERROR_ID, timeout):
        return PRENOTA_RESULT.ERROR_CONNECTION_RESET
    else:
        return PRENOTA_RESULT.UNKNOWN

class LoginResult(Enum):
    OK = 1
    UNAVAILABLE = 2
    UNKNOWN = 3

def login_and_go_to_service(driver: SeleniumDriver) -> LoginResult:
    try:
        driver.go_to_url(PRENOTAME_USER_AREA_URL)

        if driver.need_login():
            time.sleep(2)
            driver.login()

        time.sleep(5)

        if (driver.is_unavailable()):
            return LoginResult.UNAVAILABLE

        driver.click_services()
        driver.wait_for_load_fully()
        time.sleep(5)

        return LoginResult.OK
    except Exception as e:
        return LoginResult.UNKNOWN

def process(driver: SeleniumDriver):
    from selenium.common.exceptions import TimeoutException

    _id = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    _date = _id.split()[0]
    _time = _id.split()[1]
    _result = None

    try:
        login_and_go_to_service(driver)

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


def wait_until(hours, minutes, seconds):
    actual_time = datetime.now()
    hora_objetivo = datetime.combine(actual_time.date(
    ), datetime.min.time()) + timedelta(hours=hours, minutes=minutes, seconds=seconds)
    diferencia = (hora_objetivo - actual_time).total_seconds()

    if(diferencia > 0):
        print(f'Voy a dormir {diferencia} segundos hasta las {hora_objetivo}')
        time.sleep(diferencia)
    else:
        print(f'No voy a dormir, ya paso la hora {hora_objetivo}')
