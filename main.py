from datetime import datetime, timedelta
import random
from log import save_log, save_result_operation, get_result_operation
import time
from driver import SeleniumDriver, next_service, Service
from decorators import log, try_except
from popup import showPopup
from enum import Enum
from mail import get_OTP
import threading

TRYES = 5
PRENOTAME_USER_AREA_URL = 'https://prenotami.esteri.it/UserArea'
PRENOTAME_BOOKING_URL = 'https://prenotami.esteri.it/Services/Booking/224'
TEXT_NOT_TURNS = 'i posti disponibili per il servizio scelto sono esauriti'
TEXT_NOT_TURNS_ID = 'WlNotAvailable'
TEXT_TURN_ID = 'typeofbookingddl'
ERROR_ID = 'error-information-popup-container'
TIMEOUT = 180
SLEEP_EVERY_TAB = 0.3
NOTE = 'Richiedo gentilmente un appuntamento per avviare la pratica di cittadinanza italiana.'

otp_already_click = threading.Event()

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

def get_time(hours, minutes, seconds):

    if hours != 18 or minutes != 59 or seconds != 59:
        print(f'------------------------- CUIDADO! HORA INCORRECTA -------------------------')
    
    print(f'HORA CONFIGURADA: {hours}:{minutes}:{seconds}')
    actual_time = datetime.now()
    return datetime.combine(actual_time.date(
        ), datetime.min.time()) + timedelta(hours=hours, minutes=minutes, seconds=seconds)

def start_process_7(num_processes = 6):
    import multiprocessing

    # EDGE Tab: 1, Start: 2024-10-28 18:59:58.313707, Finish: 2024-10-28 19:01:24.057974 result: ERROR_CONNECTION_RESET
    # EDGE Tab: 2, Start: 2024-10-28 18:59:58.680350, Finish: 2024-10-28 19:02:09.588163 result: ERROR_CONNECTION_RESET
    # EDGE Tab: 3, Start: 2024-10-28 18:59:59.011949, Finish: 2024-10-28 19:02:11.165630 result: ERROR_CONNECTION_RESET
    # EDGE Tab: 4, Start: 2024-10-28 18:59:59.345237, Finish: 2024-10-28 19:02:12.336065 result: ERROR_CONNECTION_RESET
    # EDGE Tab: 5, Start: 2024-10-28 18:59:59.670937, Finish: 2024-10-28 19:02:13.510546 result: OK

    # CHROME Tab: 1, Start: 2024-10-28 18:59:58.313908, Finish: 2024-10-28 19:01:05.786782 result: ERROR_CONNECTION_RESET
    # CHROME Tab: 2, Start: 2024-10-28 18:59:58.674917, Finish: 2024-10-28 19:01:06.991002 result: ERROR_CONNECTION_RESET
    # CHROME Tab: 3, Start: 2024-10-28 18:59:58.998767, Finish: 2024-10-28 19:01:08.163938 result: ERROR_CONNECTION_RESET
    # CHROME Tab: 4, Start: 2024-10-28 18:59:59.326222, Finish: 2024-10-28 19:01:09.350535 result: ERROR_CONNECTION_RESET
    # CHROME Tab: 5, Start: 2024-10-28 18:59:59.656950, Finish: 2024-10-28 19:02:15.766849 result: OK

    try:
        processes = []

        print(f'Se van a ejecutar {num_processes} procesos')
        target_datetime = get_time(18, 59, 59)
        # target_datetime = get_time(18, 54, 59)

        for i in range(num_processes):
            p = multiprocessing.Process(
                target=process_seven, args=(Service.CHROME, target_datetime, i))
            processes.append(p)
            p.start()

            # p2 = multiprocessing.Process(
            #     target=process_seven, args=(Service.EDGE, target_datetime, i))
            # processes.append(p2)
            # p2.start()

            target_datetime += timedelta(milliseconds=200)

        for p in processes:
            p.join()

    except Exception as e:
        print(f'Error: {e}')


def ___start_process_7():
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


# def print_execution(service, executions):
#     for execution in executions:
#         print(f"{service} Tab: {execution['tab']}, Start: {execution['start']}, Finish: {
#               execution['finish']} result: {execution['result']}")

class Log():
    def __init__(self, id):
        self.id = id
    
    def info(self, text):
        print(f'{datetime.now()} - {self.id}: {text}')

@try_except
def booking_turn_load(driver: SeleniumDriver):
    print('otp_already_click', otp_already_click.is_set())
    while True:
        otp_button = driver.is_load()

        if otp_button is None:
            pass
        elif isinstance(otp_button, str):
            return otp_button
        else:
            if not otp_already_click.is_set():
                otp_button.click()
                otp_already_click.set()
                return True
            else:
                return 'OTP_ALREADY_CLICK'

    
@try_except
def process_seven(service: Service, execution_time, id):
    # id = f'{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}___{service.name}_{id}___'
    id = f'{service.name}_{id}'

    log = Log(id)
    print('otp_already_click', otp_already_click.is_set())

    driver = SeleniumDriver(TIMEOUT, service=service, log=log)

    if login_and_go_to_service(driver) == LoginResult.UNAVAILABLE:
        print(service.name, f'Unavailable')
        return

    sleep_until(execution_time)

    log.info(f'Execution programming: {execution_time}. Execution date: {datetime.now()}')

    driver.go_to_url(PRENOTAME_BOOKING_URL)

    log.info(f'Trying OTP...')

    result = booking_turn_load(driver)

    if(isinstance(result, str)):
        log.info(f'Booking Error: {result}')
        return
    
    log.info('Booking OK. OTP enviado!')

    time.sleep(5)

    otp = None

    while True:
        otp = get_OTP()

        if otp is None:
            log.info('No se encontró código OTP en mail.')
        else:
            log.info(f'Se encontró un nuevo código OTP!: {otp}')
            break
    
    try:
        driver.complete_and_send_form(otp, NOTE)
    except Exception as e:
        pass

    time.sleep(3)

    driver.book()

    for i in range(10):
        time.sleep(5)
        driver.save_screenshot(id, f'CALENDAR_{i}')

    time.sleep(60*10)



    # driver.click_prenota()

    # time.sleep(60*10)
    # print_execution(service.name, executions)

    # for e in range(0, len(executions)):
    #     print(service.name, f'Execution {e}')
    #     if (not executions[e]['isFinished']):
    #         print(service.name, f'change_tab: {e}')
    #         driver.change_tab(e+1)
    #         print(service.name, f'change_tab end: {e}')

    #         if driver.is_load(1):
    #             print(service.name, f'if isload {e}')
    #             executions[e]['finish'] = datetime.now()
    #             executions[e]['isFinished'] = True
    #             executions[e]['result'] = get_result_prenota(driver).name
    #             driver.save_screenshot(f'{id}_TAB_{e}_{service.name}', '')
    #             print(service.name, f'if isload end {e}')

    #         time.sleep(1)

    #     if all(item['isFinished'] for item in executions):
    #         print(service.name, f'isFinished {e}')
    #         break

    # print_execution(service.name, executions)



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

        time.sleep(3)

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


def _wait_until(hours, minutes, seconds):
    actual_time = datetime.now()
    hora_objetivo = datetime.combine(actual_time.date(
    ), datetime.min.time()) + timedelta(hours=hours, minutes=minutes, seconds=seconds)
    diferencia = (hora_objetivo - actual_time).total_seconds()

    if (diferencia > 0):
        print(f'Voy a dormir {diferencia} segundos hasta las {hora_objetivo}')
        time.sleep(diferencia)
    else:
        print(f'No voy a dormir, ya paso la hora {hora_objetivo}')


def sleep_until(target_datetime):
    current_time = datetime.now()
    milliseconds_until = (
        target_datetime - current_time).total_seconds() * 1000

    print(f"Esperando hasta {target_datetime}")

    if milliseconds_until > 0:
        # Convertir milisegundos a segundos
        time.sleep(milliseconds_until / 1000)

    return True
