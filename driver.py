from selenium import webdriver
from dotenv import dotenv_values
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from decorators import try_except
from log import save_file, create_folder_if_not_exists
from decorators import log
import os

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from enum import Enum
from selenium import webdriver
import time

from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium_stealth import stealth


SCREENSHOT_FOLDER_NAME = 'screenshots'


class Service(Enum):
    CHROME = 1
    FIREFOX = 2
    EDGE = 3


chrome_service = ChromeService()
firefox_service = FirefoxService()
edge_service = EdgeService()

next_service = {
    # Service.CHROME: Service.FIREFOX,
    # Service.FIREFOX: Service.EDGE,
    # Service.EDGE: Service.CHROME
    Service.CHROME: Service.EDGE,
    Service.EDGE: Service.CHROME
}


class SeleniumDriver:
    @try_except
    def __init__(self, timeout=60, show_logs=False, service=Service.CHROME):
        if service == Service.CHROME:
            chrome_options = ChromeOptions()
            chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--incognito")
            self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

            stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True)

        elif service == Service.FIREFOX:
            self.driver = webdriver.Firefox(service=firefox_service)
        elif service == Service.EDGE:
            egde_options = EdgeOptions()
            egde_options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Safari/537.36 Edg/117.0.2045.43")
            egde_options.add_argument("--inprivate")
            egde_options.add_argument("--disable-gpu")
            egde_options.add_argument("--no-sandbox")
            egde_options.add_argument("--disable-dev-shm-usage")
            self.driver = webdriver.Edge(service=edge_service, options=egde_options)

            # stealth(self.driver,
            #     languages=["en-US", "en"],
            #     vendor="Google Inc.",
            #     platform="Win32",
            #     webgl_vendor="Intel Inc.",
            #     renderer="Intel Iris OpenGL Engine",
            #     fix_hairline=True)

        self.timeout = timeout
        self.show_logs: bool = show_logs
        self.config = dotenv_values(".env")
        self.service = service

        self.driver.set_page_load_timeout(timeout)
    
    def close(self):
        self.driver.quit()

    @try_except
    def go_to_url(self, url):
        self.driver.get(url)

    @try_except
    def need_login(self):
        return "login-email" in self.driver.page_source
    
    @try_except
    def click_services(self):
        advanced_link = self.driver.find_element(By.ID, "advanced")
        advanced_link.click()
    
    @try_except
    def click_prenota(self):
        button = self.driver.find_element(By.XPATH, "//tr[td[contains(text(),'Ricostruzione Cittadinanza')]]//button[@class='button primary']")
        button.click()

    @try_except
    def login(self):
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        user_elem = self.driver.find_element(By.ID, "login-email")
        user_elem.send_keys(self.config.get("EMAIL"))
        time.sleep(1)
        password_elem = self.driver.find_element(By.ID, "login-password")
        password_elem.send_keys(self.config.get("PRENOTAME_PASSWORD"))
        time.sleep(1)
        password_elem.send_keys(Keys.RETURN)

    @try_except
    def exist_text(self, text):
        return text in self.driver.page_source

    @try_except
    def exists_id(self, id: str):
        # elementos = self.driver.find_element(By.ID, id)
        elemento = self.driver.execute_script(
            f"return document.getElementById('{id}');")

        if elemento:
            return True
        else:
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

    @try_except
    def wait_for_load_fully(self):
        # while not self.is_load():
        #     pass
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: d.execute_script(
                "return document.readyState") == "complete"
        )

    @try_except
    def is_load(self):
        status = self.driver.execute_script("return document.readyState")
        print(status)
        return status == "complete"

    @try_except
    def open_tab(self, url):
        self.driver.execute_script(f"window.open('{url}');")

    @try_except
    def change_tab(self, tab: int):
        self.driver.switch_to.window(self.driver.window_handles[tab])
