from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote import webelement
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

from pyautogui import hotkey
import win32clipboard
from PIL import Image

import time
import requests
import os
from platform import system
import pathlib
from io import BytesIO

from core.Exceptions import InternetExeption, InvalidParameterException
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
    TimeoutException,
    NoSuchElementException)


URL: str = 'https://web.whatsapp.com'
CHECK_CONNECTION_URL = 'https://www.google.com'
TIMEOUT: int = 5
LOADING_TIME: int = 20

HTML_FIRST_TIME_CHECK_CLASS_NAME: str = '_1N3oL'
HTML_BALOON_MESSAGE_CLASS_NAME: str = 'Nm1g1'
HTML_MESSAGE_CLASS_NAME: str = '_1Gy50'
HTML_HOUR_MESSAGE_CLASS_NAME: str = 'kOrB_'
HTML_IMAGE_BOX_CLASS_NAME: str = '_1N4rE'
HTML_IMAGE_CLASS_NAME: str = '_3IfUe'
HTML_NEW_MESSAGE_CLASS_NAME: str = 'Hy9nV'

HTML_SEARCH_CONTACTS_TEXTBOX_XPATH: str = '//*[@id="side"]/div[1]/div/label/div/div[2]'
HTML_XPATH_TEXTBOX_XPATH: str = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]'
HTML_SEND_BUTTON_XPATH: str = '//span[@data-testid="send"]'
HTML_CLOSE_IMAGE_BUTTON_XPATH: str = '//span[@data-testid="x-viewer"]'


class Whatsapp_API(object):
    def __init__(self, width: int = 800, height: int = 600, window_position_x: int = 50, window_position_y: int = 50, bot_name: str = 'Cortana') -> None:
        """
        Start the class with webdriver objects

        params:
            width: int - the browser width
            height: int - the height of the browser
            window_position_x: int - browser's starting position in quadrant x
            window_position_y: int - browser start position in y quadrant
            bot_name: str - name for the bot, by default the name is set to Cortana 
        """
        super().__init__()
        options: Options = webdriver.ChromeOptions()
        options.add_argument(r"user-data-dir=" + os.getcwd() + r"\profile")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(
            executable_path=ChromeDriverManager(log_level=0).install(), chrome_options=options)
        self.driver.set_window_size(width=width, height=height)
        self.driver.set_window_position(
            x=window_position_x, y=window_position_y)
        self.bot_name = bot_name

    def check_internet_connection(self, url: str = CHECK_CONNECTION_URL) -> None:
        """Check the Internet connection of the Host Machine"""
        try:
            requests.get(url)
        except requests.RequestException:
            raise InternetExeption(
                "Error while connecting. Make sure you are connected to the Internet!")

    def first_time_check(self) -> bool:
        """
        Checks if this is the first time the login is being done

        raise - NoSuchElementException
                TimeoutException
        """
        global HTML_FIRST_TIME_CHECK_CLASS_NAME

        try:
            element_present = EC.presence_of_element_located(
                (By.CLASS_NAME, HTML_FIRST_TIME_CHECK_CLASS_NAME))
            WebDriverWait(self.driver, TIMEOUT).until(element_present)
            self.driver.find_element(
                by=By.CLASS_NAME, value=HTML_FIRST_TIME_CHECK_CLASS_NAME)
            return True
        except NoSuchElementException:
            return False
        except TimeoutException:
            return False

    def open_whatsapp_web(self, time_to_login: int = 120) -> None:
        """
        Open Whatsapp web, if it is the first time the system will wait 120 seconds for the login to be done.

        params:
            time_to_login: int - time to read whatsapp web QRCode
        """
        global URL, LOADING_TIME

        self.driver.get(URL)

        if self.first_time_check():
            print(
                'Use your cellphone to login in WhatsApp Web, you have by default 120 seconds to do it.')
            time.sleep(time_to_login)
            self.driver.implicitly_wait(LOADING_TIME)
        else:
            print('Login successfully.')
            self.driver.implicitly_wait(LOADING_TIME)

    def listen(self, list_commands: list[str]) -> list[WebElement]:
        """
        Checks if other conversations are executing commands

        params:
            list_commands: list[str] - list of commands for checking

        raise - StaleElementReferenceException
        """
        global HTML_NEW_MESSAGE_CLASS_NAME
        queue: list[WebElement] = []

        try:
            new_messages: list[WebElement] = self.driver.find_elements(
                by=By.CLASS_NAME, value=HTML_NEW_MESSAGE_CLASS_NAME)
            for message in new_messages:
                if message.find_element(by=By.TAG_NAME, value='span').text in list_commands:
                    queue.append(message.find_element(
                        by=By.TAG_NAME, value='span'))
            return queue
        except StaleElementReferenceException:
            return queue

    def find_contact(self, contact_name: str) -> WebElement:
        """
        Find and return a contact on Whatsapp Web

        params:
            contact_name: str - the contact's name

        raise - TimeoutException
        """
        try:
            element_present = EC.presence_of_element_located(
                (By.XPATH, "//span[@title='%s']" % (contact_name)))
            WebDriverWait(self.driver, TIMEOUT).until(element_present)
            return self.driver.find_element(by=By.XPATH, value="//span[@title='%s']" % (contact_name))
        except TimeoutException:
            raise TimeoutException(
                "Error trying to find the html element"
            )
    
    def search_contact(self, contact_name: str) -> None:
        """
        Search and select a contact on Whatsapp Web

        params:
            contact_name: str - contact name. Note: does not accept emojis
        """
        global HTML_SEARCH_CONTACTS_TEXTBOX_XPATH

        self.find_chat_box(HTML_SEARCH_CONTACTS_TEXTBOX_XPATH).send_keys(
            contact_name)
        self.find_contact(contact_name).click()

    def find_chat_box(self, chat_box_xpath: str) -> WebElement:
        """
        Finds and returns the Whatsapp Web textbox

        params:
            chat_box: str - the XPath to the textbox

        raise - TimeoutException
        """
        global TIMEOUT

        try:
            element_present = EC.presence_of_element_located(
                (By.XPATH, chat_box_xpath))
            WebDriverWait(self.driver, TIMEOUT).until(element_present)
            return self.driver.find_element(by=By.XPATH, value=chat_box_xpath)
        except TimeoutException:
            raise TimeoutException(
                "Error trying to find the html element"
            )

    def read_message(self, trigger_message: str = '!') -> str:
        """
        Read and return the received message.

        params: 
            trigger_message: str - The trigger command, default '!'.
        """
        global HTML_MESSAGE_CLASS_NAME, HTML_BALOON_MESSAGE_CLASS_NAME, HTML_HOUR_MESSAGE

        message = self.driver.find_elements(
            by=By.CLASS_NAME, value=HTML_BALOON_MESSAGE_CLASS_NAME)[-1]
        if message.find_element(by=By.CLASS_NAME, value=HTML_MESSAGE_CLASS_NAME).text[0] == trigger_message:
            return message.find_element(by=By.CLASS_NAME, value=HTML_MESSAGE_CLASS_NAME).text
        return ''

    def read_image(self, triggerMessage: str, dir: str, file_name: str = 'image') -> bool:
        """
        Receive an image from a contact and save then in a specific location.

        params:
             file_name: str - name of the image, by default is 'image'
             triggerMessage: str - the message that trigger the command
             dir: str - the path to save the image
        """
        global HTML_IMAGE_BOX_CLASS_NAME, HTML_IMAGE_CLASS_NAME

        try:
            self.get_image_by_xpath(
                "//img[@alt='%s']" % (triggerMessage))[-1].click()
        except IndexError:
            return False
        except ElementClickInterceptedException:
            return False

        self.driver.implicitly_wait(1)
        image = self.get_image_by_class_name(HTML_IMAGE_BOX_CLASS_NAME)[-1].find_elements(
            by=By.CLASS_NAME, value=HTML_IMAGE_CLASS_NAME)[-1].screenshot_as_png

        try:
            with open(dir + '/' + file_name + '.png', 'wb') as file:
                file.write(image)
                self.close_image().click()
                return True
        except IOError:
            return False
        except Exception:
            return False

    def get_image_by_xpath(self, xpath: str) -> list[WebElement]:
        """
        Find and return an image by its XPath

        params:
            xpath: src - the XPath to the image
        """
        global TIMEOUT

        try:
            element_present = EC.presence_of_element_located(
                (By.XPATH, xpath))
            WebDriverWait(self.driver, TIMEOUT).until(element_present)
            return self.driver.find_elements(
                by=By.XPATH, value=xpath)
        except TimeoutException:
            print(TimeoutException(
                "Error trying to find image in selected message, make sure there is an image to be received."
            ))
            return []

    def get_image_by_class_name(self, class_name: str) -> list[WebElement]:
        """
        Find and return an image by its class name

        params:
            class_name: src - the class name of the image
        """
        global TIMEOUT

        try:
            element_present = EC.presence_of_element_located(
                (By.CLASS_NAME, class_name))
            WebDriverWait(self.driver, TIMEOUT).until(element_present)
            return self.driver.find_elements(
                by=By.CLASS_NAME, value=class_name)
        except TimeoutException:
            print(TimeoutException(
                "Error trying to find image in selected message, make sure there is an image to be received."
            ))
            return []

    def write_message(self, text: str) -> None:
        """
        Write a message in the Whatsapp Web text box

        params:
            text: str - text to be written  
        """
        global HTML_XPATH_TEXTBOX_XPATH

        self.find_chat_box(HTML_XPATH_TEXTBOX_XPATH).send_keys(
            '%s: %s' % (self.bot_name, text))

    def write_text_with_emoji(self, text: str, text_box: int = 2) -> None:
        """
        Write a message with emoji in the Whatsapp Web text box. It can also be used to search for contacts on WhatsApp Web.

        params:
        text: str - the text to be written
        text_box: int - 1 to write in the contact search box
                        2 to write in the message text box

        raise - InvalidParameterException
        """
        global HTML_XPATH_TEXTBOX_XPATH, HTML_SEARCH_CONTACTS_TEXTBOX_XPATH

        if text_box == 1:
            chat_box: webelement = self.find_chat_box(
                HTML_SEARCH_CONTACTS_TEXTBOX_XPATH)
            self.driver.execute_script(
                "arguments[0].innerHTML = '{}'".format(text), chat_box)
        elif text_box == 2:
            chat_box: webelement = self.find_chat_box(HTML_XPATH_TEXTBOX_XPATH)
            self.driver.execute_script(
                "arguments[0].innerHTML = '{}'".format(text), chat_box)
            self.write_message('')
        else:
            raise InvalidParameterException(
                "The parameter received is invalid. Choose between 1 to write in the contact search box or 2 to write in the message text box")

    def find_send_button(self) -> WebElement:
        """
        Finds and returns the send button on Whatsapp Web

        raise - TimeoutException
        """
        global TIMEOUT, HTML_SEND_BUTTON_XPATH

        try:
            element_present = EC.presence_of_element_located(
                (By.XPATH, HTML_SEND_BUTTON_XPATH))
            WebDriverWait(self.driver, TIMEOUT).until(element_present)
            return self.driver.find_element(by=By.XPATH, value=HTML_SEND_BUTTON_XPATH)
        except TimeoutException:
            raise TimeoutException(
                "Error trying to find the html element"
            )

    def click_send_message_button(self) -> None:
        """Find and click the send message button on Whatsapp Web"""
        self.find_send_button().click()

    def write_and_send_message(self, text: str) -> None:
        """Write and send a message in the current conversation"""
        self.write_message(text=text)
        self.find_send_button().click()

    def send_image(self, dir: str) -> bool:
        """
        Send an image to the current conversation

        params:
            dir: str - the path the image is located
        """
        global HTML_XPATH_TEXTBOX_XPATH

        try:
            self.find_chat_box(HTML_XPATH_TEXTBOX_XPATH).click()
            self.copy_image(dir)
            hotkey("ctrl", "v")
            self.driver.implicitly_wait(1)
            self.find_send_button().click()
            time.sleep(2)
            return True
        except Exception as err:
            raise err

    def close_image(self) -> WebElement:
        """
        Finds the close button on the image when it is full screen

        raise - TimeoutException
        """
        global TIMEOUT, HTML_CLOSE_IMAGE_BUTTON_XPATH

        try:
            element_present = EC.presence_of_element_located(
                (By.XPATH, HTML_CLOSE_IMAGE_BUTTON_XPATH))
            WebDriverWait(self.driver, TIMEOUT).until(element_present)
            return self.driver.find_element(
                by=By.XPATH, value=HTML_CLOSE_IMAGE_BUTTON_XPATH)
        except TimeoutException:
            raise TimeoutException(
                "Error trying to find the html element."
            )

    def copy_image(self, path: str) -> None:
        """
        Copy the Image to Clipboard based on the Platform

        raise - Exception("File Format is not Supported)
                FileNotFoundError
                Exception("Unsupported System")
        """
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
            try:
                with Image.open(path) as image:
                    output = BytesIO()
                    image.convert("RGB").save(output, "BMP")
                    data = output.getvalue()[14:]
                    output.close()
                    win32clipboard.OpenClipboard()
                    win32clipboard.EmptyClipboard()
                    win32clipboard.SetClipboardData(
                        win32clipboard.CF_DIB, data)
                    win32clipboard.CloseClipboard()
            except FileNotFoundError:
                print(FileNotFoundError('File not Found'))
            except Exception as err:
                raise err
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

    def quit(self) -> None:
        """Ends all Chrome processes"""
        self.driver.implicitly_wait(1)
        self.driver.quit()
