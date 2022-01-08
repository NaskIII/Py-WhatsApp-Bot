from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager

import requests
import os
import time

from webdriver_manager.utils import File

from core.Exceptions import InternetExeption


URL: str = 'https://web.whatsapp.com'
CHECK_CONNECTION_URL = 'https://www.google.com'
TIMEOUT: int = 5
INIT_TIMEOUT: int = 15
LAST_MESSAGE: str = ''

HTML_BALOON_MESSAGE: str = 'Nm1g1'
HTML_MESSAGE: str = '_1Gy50'
HTML_HOUR_MESSAGE: str = 'kOrB_'
HTML_XPATH_TEXTBOX: str = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]'
HTML_SEND_BUTTON: str = '_4sWnG'


class Whatsapp_API(object):
    def __init__(self, width: int = 800, height: int = 600, window_position_x: int = 50, window_position_y: int = 50) -> None:
        """Init the class with the webdriver objects"""
        super().__init__()
        options: object = webdriver.ChromeOptions()
        options.add_argument(r"user-data-dir=" + os.getcwd() + r"\profile")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(
            executable_path=ChromeDriverManager(log_level=0).install(), chrome_options=options)
        self.driver.set_window_size(width=width, height=height)
        self.driver.set_window_position(
            x=window_position_x, y=window_position_y)

    def check_internet_connection(self, url: str = CHECK_CONNECTION_URL):
        """Check the Internet connection of the Host Machine"""
        try:
            requests.get(url)
        except requests.RequestException:
            raise InternetExeption(
                "Error while connecting. Make sure you are connected to the Internet!")

    def web(self, time_to_login: int) -> None:
        """Start browser with whatsapp web"""
        global URL, INIT_TIMEOUT
        self.driver.get(URL)
        try:
            self.driver.implicitly_wait(INIT_TIMEOUT)
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
        global HTML_XPATH_TEXTBOX
        chat_box = self.driver.find_element(by=By.XPATH,
                                            value=HTML_XPATH_TEXTBOX)
        chat_box.send_keys('Cortana: %s' % (text))
        return True

    def send_message(self) -> bool:
        """Send message"""
        global TIMEOUT, HTML_SEND_BUTTON
        try:
            element_present = EC.presence_of_element_located(
                (By.CLASS_NAME, HTML_SEND_BUTTON))
            WebDriverWait(self.driver, TIMEOUT).until(element_present)
            send_button = self.driver.find_element(
                by=By.CLASS_NAME, value=HTML_SEND_BUTTON)
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
        global LAST_MESSAGE, HTML_MESSAGE, HTML_BALOON_MESSAGE, HTML_HOUR_MESSAGE
        message = self.driver.find_elements(
            by=By.CLASS_NAME, value=HTML_BALOON_MESSAGE)[-1]
        if time.strftime(message.find_element(by=By.CLASS_NAME, value=HTML_HOUR_MESSAGE).text) >= time.strftime("%H:%M"):
            if message.find_element(by=By.CLASS_NAME, value=HTML_MESSAGE).text[0] == trigger and message.find_element(by=By.CLASS_NAME, value=HTML_MESSAGE).text != LAST_MESSAGE:
                _LAST_MESSAGE = message.find_element(
                    by=By.CLASS_NAME, value=HTML_MESSAGE).text
                print(_LAST_MESSAGE)
                return message.find_element(by=By.CLASS_NAME, value=HTML_MESSAGE).text
        return ''

    def read_image(self, fileName: str, triggerMessage: str, dir: str = os.getcwd()) -> bool:
        try:
            with open(dir + '/' + fileName + '.png', 'wb') as file:
                self.driver.find_elements(
                    by=By.XPATH, value="//img[@alt='%s']" % (triggerMessage))[-1].click()
                time.sleep(2)
                image = self.driver.find_element(
                    by=By.CLASS_NAME, value="_1N4rE").find_elements(by=By.CLASS_NAME, value='_3IfUe')[-1].screenshot_as_png
                file.write(image)
                self.driver.find_element(
                    by=By.XPATH, value='//span[@data-testid="x-viewer"]').click()
                return True
        except:
            return False

    def quit(self) -> None:
        self.driver.quit()
