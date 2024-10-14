from selenium import webdriver
from dotenv import dotenv_values
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from decorators import try_except
from log import save_file, create_folder_if_not_exists
from decorators import log
import os

SCREENSHOT_FOLDER_NAME = 'screenshots'
TIMEOUT = 60*5


class SeleniumDriver:
    def __init__(self):
        service = Service()
        self.config = dotenv_values(".env")
        self.driver = webdriver.Chrome(service=service)
        self.driver.implicitly_wait(60*5)

    @log
    @try_except
    def go_to_url(self, url):
        self.driver.get(url)

    @try_except
    def need_login(self):
        return "login-email" in self.driver.page_source

    @log
    @try_except
    def login(self):
        user_elem = self.driver.find_element(By.ID, "login-email")
        user_elem.send_keys(self.config.get("EMAIL"))
        # time.sleep(1)
        password_elem = self.driver.find_element(By.ID, "login-password")
        password_elem.send_keys(self.config.get("PRENOTAME_PASSWORD"))
        # time.sleep(1)
        password_elem.send_keys(Keys.RETURN)

    @log
    @try_except
    def exist_text(self, text):
        return text in self.driver.page_source

    @log
    def exists_id(self, id):
        elementos = self.driver.find_elements(By.ID, id)  # Devuelve una lista

        if elementos:
            print(f"Elemento con ID '{id}' encontrado.")
            return True
        else:
            print(f"Elemento con ID '{id}' no encontrado.")
            return False
        # WebDriverWait(self.driver, 2).until(
        #     EC.presence_of_element_located((By.ID, id))
        # )
        # try:
        #     elemento = self.driver.find_element("id", id)
        #     return True
        # except:
        #     return False

    @try_except
    def save_screenshot(self, id, step):
        screenshot_url = os.path.join(os.getcwd(), SCREENSHOT_FOLDER_NAME)

        create_folder_if_not_exists(screenshot_url)
        self.driver.save_screenshot(f'{screenshot_url}/{id}_{step}.png')
        save_file(f'{screenshot_url}/{id}_{step}.html',
                  self.driver.page_source)

    @log
    @try_except
    def wait_for_load_fully(self):
        # while not self.is_load():
        #     pass
        WebDriverWait(self.driver, TIMEOUT).until(
            lambda d: d.execute_script(
                "return document.readyState") == "complete"
        )

    def is_load(self):
        status = self.driver.execute_script("return document.readyState")
        print(status)
        return status == "complete"

    @try_except
    def execute_script(self, url):
        self.driver.execute_script(f"window.open('{url}');")

    @log
    @try_except
    def change_tab(self, tab: int):
        self.driver.switch_to.window(self.driver.window_handles[tab])
