from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

import requests
import os
import time

from webdriver_manager.utils import File

from core.Exceptions import InternetExeption


_URL: str = 'https://web.whatsapp.com'
_TIMEOUT: int = 5
_INIT_TIMEOUT: int = 15
_LAST_MESSAGE: str = ''

_HTML_BALOON_MESSAGE: str = '_22Msk'
_HTML_MESSAGE: str = '_1Gy50'
_HTML_HOUR_MESSAGE: str = 'kOrB_'
_HTML_XPATH_TEXTBOX: str = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]'


class Whatsapp_API(object):
    def __init__(self, size: dict = {"width": 800, "height": 600}, window_position: dict = {"x": 50, "y": 50}) -> None:
        """Init the class with the webdriver objects"""
        super().__init__()
        dir_path: str = os.getcwd()
        options: object = webdriver.ChromeOptions()
        options.add_argument(r"user-data-dir=" + dir_path + r"\profile")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(
            executable_path=ChromeDriverManager(log_level=0).install(), chrome_options=options)
        self.driver.set_window_size(width=size['width'], height=size['height'])
        self.driver.set_window_position(
            x=window_position["x"], y=window_position["y"])

    def check_internet_connection(self, url: str = 'https://www.google.com'):
        """Check the Internet connection of the Host Machine"""
        try:
            requests.get(url)
        except requests.RequestException:
            raise InternetExeption(
                "Error while connecting to the Internet. Make sure you are connected to the Internet!")

    def web(self, time_to_login: int) -> None:
        """Start browser with whatsapp web"""
        global _URL, _INIT_TIMEOUT
        self.driver.get(_URL)
        try:
            self.driver.implicitly_wait(_INIT_TIMEOUT)
            time.sleep(time_to_login)
        except:
            self.driver.quit()

    def contacts(self, target: str) -> bool:
        """Go into target chat in whatsapp"""
        chat = self.driver.find_element(by=By.XPATH,
                                        value="//span[@title='%s']" % (target))
        chat.click()
        return True

    def message(self, text: str) -> bool:
        """Send text to whatsapp textbox"""
        global _HTML_XPATH_TEXTBOX
        chat_box = self.driver.find_element(by=By.XPATH,
                                            value=_HTML_XPATH_TEXTBOX)
        chat_box.send_keys('Cortana: %s' % (text))
        return True

    def send_message(self) -> bool:
        """Send message"""
        global _TIMEOUT
        try:
            element_present = EC.presence_of_element_located(
                (By.CLASS_NAME, '_4sWnG'))
            WebDriverWait(self.driver, _TIMEOUT).until(element_present)
            send_button = self.driver.find_element(
                by=By.CLASS_NAME, value='_4sWnG')
            send_button.click()
            return True
        except TimeoutException:
            print('TimeoutException')
            return False

    def answer_message(self, text: str) -> bool:
        """Send text to whatsapp textbox and send message"""
        result: bool = self.message(text=text)
        if result:
            result = self.send_message()
            return result
        else:
            return False

    def read_message(self, trigger: str = '!') -> str:
        """
        Read and return the received message.

        params: trigger: str - The trigger command, default '!'.
        """
        global _LAST_MESSAGE, _HTML_MESSAGE, _HTML_BALOON_MESSAGE, _HTML_HOUR_MESSAGE
        messages = self.driver.find_elements(
            by=By.CLASS_NAME, value=_HTML_BALOON_MESSAGE)
        for message in messages:
            if time.strftime(message.find_element(by=By.CLASS_NAME, value=_HTML_HOUR_MESSAGE).text) >= time.strftime("%H:%M"):
                if message.find_element(by=By.CLASS_NAME, value=_HTML_MESSAGE).text[0] == trigger and message.find_element(by=By.CLASS_NAME, value=_HTML_MESSAGE).text != _LAST_MESSAGE:
                    _LAST_MESSAGE = message.find_element(
                        by=By.CLASS_NAME, value=_HTML_MESSAGE).text
                    print(_LAST_MESSAGE)
                    return message.find_element(by=By.CLASS_NAME, value=_HTML_MESSAGE).text
    
    def read_image(self, fileName: str = 'Image.png', triggerMessage: str = '!image') -> File:
        with open(fileName, 'wb') as file:
            image = self.driver.find_elements(by=By.XPATH, value="//img[@alt='%s']" %(triggerMessage))
            file.write(image)

    def quit(self) -> None:
        self.driver.quit()
