from selenium import webdriver
from dotenv import dotenv_values
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from decorators import try_except
from log import save_file
from decorators import log

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

    @try_except
    def are_there_turns(self):
        return "Stante l'elevata richiesta i posti disponibili per il servizio scelto sono esauriti" in self.driver.page_source

    @try_except
    def save_screenshot(self, id, step):
        self.driver.save_screenshot(f'{id}_{step}.png')
        save_file(f'{id}_{step}.html', self.driver.page_source)

    @try_except
    def wait_for_load(self):
        while self.driver.execute_script("return document.readyState") != "complete":
            pass
    
    @try_except
    def execute_script(self, url):
        self.driver.execute_script(f"window.open('{url}');")
    
    @log
    @try_except
    def change_tab(self, tab: int):
        self.driver.switch_to.window(self.driver.window_handles[tab])
