from playwright import Page
import time 

TEXT_NOT_TURNS_ID = 'WlNotAvailable'
ERROR_ID = 'error-information-popup-container'

def send_OTP(page: Page):
    while True:
        if page.locator(TEXT_NOT_TURNS_ID).is_visible():
            raise RuntimeError('No hay turnos disponibles')
        elif page.locator(ERROR_ID).is_visible():
            raise RuntimeError('Error de conexion')
        elif page.locator('otp-send').is_visible():
            page.click('otp-send')
            break
        else:
            time.sleep(1)




   