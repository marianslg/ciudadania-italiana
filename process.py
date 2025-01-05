from playwright.sync_api import sync_playwright
from log import Log
import config
import time
from playwright.sync_api import Page, Playwright
from mail import get_OTP
import json

TEXT_NOT_TURNS_ID = '.jconfirm-content'
ERROR_ID = '.error-information-popup-container'


class Process:
    def __init__(self, name, execution_time):
        self.name = name
        self.execution_time = execution_time
        self.log: Log = Log(name)

    def run(self):
        with sync_playwright() as p:
            try:
                page = self.new_page(p)

                self.login(page)

                page.click('id=advanced')  # click prenota

                time.sleep(5)

                self.sleep(self.execution_time)  # sleep until execution time
                print('1')
                page.goto(config.PRENOTAME_BOOKING_URL)  # go to booking page
                print('2')

                self.send_OTP(page)  # send OTP

                time.sleep(5)

                otp = None

                while True:
                    otp = get_OTP()

                    if otp is None:
                        self.log.info('No se encontró código OTP en mail.')
                    else:
                        self.log.info(
                            f'Se encontró un nuevo código OTP!: {otp}')
                        break

                self.complete_and_send_form(page, otp, config.NOTE)

                time.sleep(3)

                self.book(page)

            except Exception as e:
                self.log.error(e)

    def new_page(self, p: Playwright):
        browser = p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-extensions'
            ]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            locale='es-AR',
            timezone_id='America/Argentina/Buenos_Aires',
            geolocation={'longitude': -58.3816, 'latitude': -34.6037},
            permissions=['geolocation']
        )
        context.set_default_timeout(300000)
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)
        page = context.new_page()

        # page.on("console", lambda msg: print(f"Console log: {msg.text}"))

        return page

    def login(self, page: Page):
        page.goto(config.PRENOTAME_USER_AREA_URL)

        if page.locator('id=login-email').is_visible():
            page.fill('id=login-email', config.EMAIL)
            page.fill('id=login-password', config.PRENOTAME_PASSWORD)
            page.press('id=login-password', 'Enter')

        time.sleep(5)

        if 'Unavailable' in page.content():
            raise RuntimeError('Unavailable')

    def sleep(self, execution_time):
        from datetime import datetime

        current_time = datetime.now()
        milliseconds_until = (
            execution_time - current_time).total_seconds() * 1000

        self.log.info(f"Sleep until {execution_time}")

        if milliseconds_until > 0:
            time.sleep(milliseconds_until / 1000)

        self.log.info(f"I wake up at {datetime.now()}")

    def send_OTP(self, page):
        while True:
            if page.locator(TEXT_NOT_TURNS_ID).is_visible():
                raise RuntimeError('There are no available turns')
            elif page.locator(ERROR_ID).is_visible():
                raise RuntimeError('Connection error')
            elif 'Unavailable' in page.content():
                raise RuntimeError('Unavailable')
            elif page.locator('.otp-send').is_visible():
                page.click('otp-send')
                self.log.info('OTP sent')
                break
            else:
                time.sleep(1)

    def complete_and_send_form(self, page, otp, note):
        self.log.info('Note per la sede')

        # Agrega una nota en "Note per la sede"
        note_field = page.locator('#BookingNotes')
        note_field.fill(note)

        self.log.info('OTP')

        # Introduce el código OTP (si lo tienes)
        otp_input = page.locator('#otp-input')
        otp_input.fill(otp)  # Reemplaza con el código OTP real
        self.log.info('Acepta la política de privacidad')

        # Acepta la política de privacidad
        privacy_checkbox = page.locator('#PrivacyCheck')
        privacy_checkbox.click()
        self.log.info('Send!')

        # Envía el formulario
        submit_button = page.locator('#btnAvanti')
        submit_button.click()

        page.on("dialog", lambda dialog: dialog.accept())

    def book(self, page):
            self.log.info(f'Waiting for button next')
            next_month_button = page.wait_for_selector('[data-action="next"]', timeout=120000)
            next_month_button.click()
            self.log.info(f'NEXT click!')

            page.route("**/*", self.handle_route)

            self.log.info(f'Waiting for button next')
            next_month_button = page.wait_for_selector('[data-action="next"]', timeout=120000)
            next_month_button.click()
            self.log.info(f'NEXT click!')

    def handle_route(route, request):
        """Intercepta solicitudes y modifica el body si apunta a /posts."""
        if request.method == "POST" and "RetrieveCalendarAvailability" in request.url:
            # Leer el body actual (es un string JSON).
            original_body = request.post_data or ""

            # Convertirlo a diccionario para modificarlo fácilmente.
            data = json.loads(original_body)

            # Modificar algún valor. Por ejemplo, cambiar el 'title' y 'userId'.
            data["selectedDay"] = sumar_8_meses(data["selectedDay"])

            # Reconstruir el body con la modificación.
            nuevo_body = json.dumps(data)

            # Continuar la solicitud con la data cambiada.
            route.continue_(post_data=nuevo_body)
        else:
            # Para cualquier otra solicitud, no hacer nada.
            route.continue_()


def sumar_8_meses(fecha: str) -> str:
    from datetime import datetime
    from dateutil.relativedelta import relativedelta

    formatos = ["%d/%m/%Y", "%Y-%m-%dT%H:%M:%S.%fZ"]
    fecha_original = None

    # Intentar parsear la fecha con cada formato
    for formato in formatos:
        try:
            fecha_original = datetime.strptime(fecha, formato)
            break
        except ValueError:
            continue

    # Si no se pudo interpretar la fecha, lanzar error
    if not fecha_original:
        print("Formato de fecha no válido. Use 'dd/mm/yyyy' o 'yyyy-mm-ddTHH:MM:SS.sssZ'.")
        return '16/08/2025'

    # Sumar 8 meses
    nueva_fecha = fecha_original + relativedelta(months=8)

    # Devolver la fecha en el mismo formato de entrada
    if "/" in fecha:
        return nueva_fecha.strftime("%d/%m/%Y")
    else:
        return nueva_fecha.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
