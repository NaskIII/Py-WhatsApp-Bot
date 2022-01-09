from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

import requests
import os
from platform import system
import pathlib
from io import BytesIO

from pyautogui import hotkey
import win32clipboard
from PIL import Image

from core.Exceptions import InternetExeption
from selenium.common.exceptions import TimeoutException, NoSuchElementException


URL: str = 'https://web.whatsapp.com'
CHECK_CONNECTION_URL = 'https://www.google.com'
TIMEOUT: int = 5
LOADING_TIME: int = 20
LAST_MESSAGE: str = ''

HTML_FIRST_TIME: str = '_1N3oL'
HTML_CONTACTS_TEXTBOX: str = '//*[@id="side"]/div[1]/div/label/div/div[2]'
HTML_BALOON_MESSAGE: str = 'Nm1g1'
HTML_MESSAGE: str = '_1Gy50'
HTML_HOUR_MESSAGE: str = 'kOrB_'
HTML_IMAGE_BOX_CLASS: str = '_1N4rE'
HTML_IMAGE_CLASS: str = '_3IfUe'
HTML_XPATH_TEXTBOX: str = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]'
HTML_SEND_XPATH_BUTTON: str = '//span[@data-testid="send"]'
HTML_X_XPATH_BUTTON: str = '//span[@data-testid="x-viewer"]'


class Whatsapp_API(object):
    def __init__(self, width: int = 800, height: int = 600, window_position_x: int = 50, window_position_y: int = 50) -> None:
        """Init the class with the webdriver objects"""
        super().__init__()
        options: Options = webdriver.ChromeOptions()
        options.add_argument(r"user-data-dir=" + os.getcwd() + r"\profile")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(
            executable_path=ChromeDriverManager(log_level=0).install(), chrome_options=options)
        self.driver.set_window_size(width=width, height=height)
        self.driver.set_window_position(
            x=window_position_x, y=window_position_y)

    def check_internet_connection(self, url: str = CHECK_CONNECTION_URL) -> None:
        """Check the Internet connection of the Host Machine"""
        try:
            requests.get(url)
        except requests.RequestException:
            raise InternetExeption(
                "Error while connecting. Make sure you are connected to the Internet!")

    def first_time(self) -> bool:
        """
        Checks if this is the first time the login is done
        """
        global HTML_FIRST_TIME
        try:
            element_present = EC.presence_of_element_located(
                (By.CLASS_NAME, HTML_FIRST_TIME))
            WebDriverWait(self.driver, TIMEOUT).until(element_present)
            self.driver.find_element(by=By.CLASS_NAME, value=HTML_FIRST_TIME)
            return True
        except NoSuchElementException:
            return False
        except TimeoutException:
            return False

    def web(self, time_to_login: int = 120) -> None:
        """
        Start browser with whatsapp web, if your first time, by default you have 120 seconds.

        args - time_to_login: time that you have to read the qrcode in whatsapp web.
        """
        global URL, LOADING_TIME

        self.driver.get(URL)

        if self.first_time():
            print(
                'Use your cellphone to login in WhatsApp Web, you have by default 120 seconds to do it.')
            self.driver.implicitly_wait(120)
            self.driver.implicitly_wait(LOADING_TIME)
        else:
            print('Login successfully.')
            self.driver.implicitly_wait(LOADING_TIME)

    def send_button(self) -> WebElement:
        """Find the send button to send text and images to a contact."""
        global TIMEOUT, HTML_SEND_XPATH_BUTTON

        try:
            element_present = EC.presence_of_element_located(
                (By.XPATH, HTML_SEND_XPATH_BUTTON))
            WebDriverWait(self.driver, TIMEOUT).until(element_present)
            return self.driver.find_element(by=By.XPATH, value=HTML_SEND_XPATH_BUTTON)
        except TimeoutException:
            raise TimeoutException(
                "Error trying to find the html element, please check html xPath."
            )

    def chat_box(self, chat_box: str) -> WebElement:
        """
        Find the chatbox of whatsapp.

        args chat_box: str - the xPath of the element
        """
        global TIMEOUT

        try:
            element_present = EC.presence_of_element_located(
                (By.XPATH, chat_box))
            WebDriverWait(self.driver, TIMEOUT).until(element_present)
            return self.driver.find_element(by=By.XPATH, value=chat_box)
        except TimeoutException:
            raise TimeoutException(
                "Error trying to find the html element, please check html xPath."
            )

    def find_contact(self, contact_name: str) -> WebElement:
        """
        Find a contact by their name.

        args contact_name: str - the name of contact.
        """
        try:
            element_present = EC.presence_of_element_located(
                (By.XPATH, "//span[@title='%s']" % (contact_name)))
            WebDriverWait(self.driver, TIMEOUT).until(element_present)
            return self.driver.find_element(by=By.XPATH, value="//span[@title='%s']" % (contact_name))
        except TimeoutException:
            raise TimeoutException(
                "Error trying to find the html element, please check html xPath."
            )

    def close_image(self) -> WebElement:
        """Close the image"""
        global TIMEOUT, HTML_X_XPATH_BUTTON

        try:
            element_present = EC.presence_of_element_located(
                (By.XPATH, HTML_X_XPATH_BUTTON))
            WebDriverWait(self.driver, TIMEOUT).until(element_present)
            return self.driver.find_element(
                by=By.XPATH, value=HTML_X_XPATH_BUTTON)
        except TimeoutException:
            raise TimeoutException(
                "Error trying to find the html element, please check html xPath."
            )

    def get_image_by_xpath(self, message: str) -> list[WebElement]:
        """
        Get the image by Xpath

        args value: str - the Xpath of the image.
        """
        global TIMEOUT

        try:
            element_present = EC.presence_of_element_located(
                (By.XPATH, message))
            WebDriverWait(self.driver, TIMEOUT).until(element_present)
            return self.driver.find_elements(
                by=By.XPATH, value=message)
        except TimeoutException:
            raise TimeoutException(
                "Error trying to find the html element, please check html xPath."
            )

    def get_image_by_class_name(self, value: str) -> list[WebElement]:
        """
        Get the image by class name

        args value: str - class name of the image.
        """
        global TIMEOUT

        try:
            element_present = EC.presence_of_element_located(
                (By.CLASS_NAME, value))
            WebDriverWait(self.driver, TIMEOUT).until(element_present)
            return self.driver.find_elements(
                by=By.CLASS_NAME, value=value)
        except TimeoutException:
            raise TimeoutException(
                "Error trying to find the html element, please check html xPath."
            )

    def contacts(self, contact_name: str) -> None:
        """Go into target chat in whatsapp"""
        global HTML_CONTACTS_TEXTBOX

        self.chat_box(HTML_CONTACTS_TEXTBOX).send_keys(contact_name)
        self.find_contact(contact_name).click()

    def message(self, text: str, bot_name: str = 'Cortana') -> None:
        """Send text to whatsapp textbox"""
        global HTML_XPATH_TEXTBOX

        self.chat_box(HTML_XPATH_TEXTBOX).send_keys(
            '%s: %s' % (bot_name, text))

    def send_message(self) -> None:
        """Send message"""
        self.send_button().click()

    def answer_message(self, text: str) -> None:
        """Send text to whatsapp textbox and send message"""
        self.message(text=text)
        self.send_button().click()

    def read_message(self, trigger: str = '!') -> str:
        """
        Read and return the received message.

        params: trigger: str - The trigger command, default '!'.
        """
        global LAST_MESSAGE, HTML_MESSAGE, HTML_BALOON_MESSAGE, HTML_HOUR_MESSAGE

        message = self.driver.find_elements(
            by=By.CLASS_NAME, value=HTML_BALOON_MESSAGE)[-1]
        if message.find_element(by=By.CLASS_NAME, value=HTML_MESSAGE).text[0] == trigger and message.find_element(by=By.CLASS_NAME, value=HTML_MESSAGE).text != LAST_MESSAGE:
            _LAST_MESSAGE = message.find_element(
                by=By.CLASS_NAME, value=HTML_MESSAGE).text
            print(_LAST_MESSAGE)
            return message.find_element(by=By.CLASS_NAME, value=HTML_MESSAGE).text
        return ''

    def read_image(self, triggerMessage: str, dir: str = os.getcwd() + r'/images', fileName: str = 'image') -> bool:
        """
        Receive a image from a contact and save then n a especific location.

        args fileName: str - name of the image
             triggerMessage: str - the message that trigger the command
             dir: str - the path to save the image, by default ir the root directory
        """
        global HTML_IMAGE_BOX_CLASS, HTML_IMAGE_CLASS

        try:
            with open(dir + '/' + fileName + '.png', 'wb') as file:
                self.get_image_by_xpath(
                    "//img[@alt='%s']" % (triggerMessage))[-1].click()
                self.driver.implicitly_wait(0.5)
                image = self.get_image_by_class_name(HTML_IMAGE_BOX_CLASS)[-1].find_elements(
                    by=By.CLASS_NAME, value=HTML_IMAGE_CLASS)[-1].screenshot_as_png
                file.write(image)
                self.close_image().click()
                return True
        except IOError as err:
            print(err)
            return False
        except Exception as err:
            print(err)
            return False

    def copy_image(self, path: str) -> None:
        """Copy the Image to Clipboard based on the Platform"""
        if system().lower() == "linux":
            if pathlib.Path(path).suffix in (".PNG", ".png"):
                os.system(f"copyq copy image/png - < {path}")
            elif pathlib.Path(path).suffix in (".jpg", ".JPG", ".jpeg", ".JPEG"):
                os.system(f"copyq copy image/jpeg - < {path}")
            else:
                raise Exception(
                    f"File Format {pathlib.Path(path).suffix} is not Supported!"
                )
        elif system().lower() == "windows":
            image = Image.open(path)
            output = BytesIO()
            image.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:]
            output.close()
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()
        elif system().lower() == "darwin":
            if pathlib.Path(path).suffix in (".jpg", ".jpeg", ".JPG", ".JPEG"):
                os.system(
                    f"osascript -e 'set the clipboard to (read (POSIX file \"{path}\") as JPEG picture)'"
                )
            else:
                raise Exception(
                    f"File Format {pathlib.Path(path).suffix} is not Supported!"
                )
        else:
            raise Exception(f"Unsupported System: {system().lower()}")

    def send_image(self, dir: str) -> bool:
        """
        Send image to a contact.
        
        args dir: str - the path to image
        """
        global HTML_XPATH_TEXTBOX

        try:
            self.chat_box(HTML_XPATH_TEXTBOX).click()
            self.copy_image(dir)
            hotkey("ctrl", "v")
            self.send_button().click()
            self.driver.implicitly_wait(0.5)
            return True
        except:
            return False

    def quit(self) -> None:
        """Close all chrome process"""
        self.driver.implicitly_wait(1)
        self.driver.quit()
