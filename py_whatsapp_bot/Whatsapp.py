# Beta Version 0.5.1 by Nask
# Beta version 0.5.1
#
# Version prepared to deal with scenarios designed for testing, where basic WhatsApp functions can be performed, such as:
#
# Receive messages from multiple chats
# Send messages to multiple chats
# Send images to multiple chats
# Receive images from multiple chats
# Send emojis to a contact or the search bar
# Turn images into stickers
# Send links
# Send files
# Send Videos
# Who sent the message
# When they sent the message

# This version is not production ready!

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
import warnings

from py_whatsapp_bot.Exceptions import InternetExeption, InvalidParameterException
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
    TimeoutException,
    NoSuchElementException)

from message_type.Message_Data import Message


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
HTML_LOADING_IMAGE_CLASS_NAME: str = 'MVKjw'
HTML_MESSAGE_SENDER_CLASS_NAME: str = 'copyable-text'
HTML_LOADING_VIDEO_CLASSNAME: str = 'pzFG8'

HTML_LINK_CONFIRMATED_XPATH: str = '//div[@style="height: 88px;"]'
HTML_SEARCH_CONTACTS_TEXTBOX_XPATH: str = '//*[@id="side"]/div[1]/div/label/div/div[2]'
HTMLTEXTBOX_XPATH: str = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]'
HTML_SEND_BUTTON_XPATH: str = '//span[@data-testid="send"]'
HTML_CLOSE_IMAGE_BUTTON_XPATH: str = '//span[@data-testid="x-viewer"]'
HTML_CLIP_BUTTON_XPATH: str = '//span[@data-testid="clip"]'
HTML_SEND_FILE_BUTTON_XPATH: str = '//input[@accept="*"]'
HTML_SEND_STICKER_BUTTON_XPATH: str = '//input[@accept="image/*"]'
HTML_SEND_IMAGE_VIDEO_BUTTON_XPATH: str = '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'

IMAGE_SIZE: tuple[int] = (521, 521)


class Whatsapp_API(object):
    def __init__(self, width: int = 800, height: int = 600, window_position_x: int = 50, window_position_y: int = 50, full_screen: bool = True, bot_name: str = 'Cortana') -> None:
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
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(
            executable_path=ChromeDriverManager(log_level=0).install(), chrome_options=options)
        if not full_screen:
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
            WebDriverWait(self.driver, TIMEOUT, ignored_exceptions=StaleElementReferenceException).until(
                element_present)
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
                for commands in list_commands:
                    if message.find_elements(by=By.TAG_NAME, value='span')[-1].text.__contains__(commands):
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
            WebDriverWait(self.driver, TIMEOUT, ignored_exceptions=StaleElementReferenceException).until(
                element_present)
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
            WebDriverWait(self.driver, TIMEOUT, ignored_exceptions=StaleElementReferenceException).until(
                element_present)
            return self.driver.find_element(by=By.XPATH, value=chat_box_xpath)
        except TimeoutException:
            raise TimeoutException(
                "Error trying to find the html element"
            )

    def read_text(self, trigger_message: str = '!') -> str:
        """
        Read and return the received message.

        params: 
            trigger_message: str - The trigger command, default '!'.
        """
        warnings.warn(
            "read_text() -> str will be deleted in future versions, use read_message() -> Message instead", DeprecationWarning)
        global HTML_MESSAGE_CLASS_NAME, HTML_BALOON_MESSAGE_CLASS_NAME

        try:
            list_mesage: WebElement = self.driver.find_elements(
                by=By.CLASS_NAME, value=HTML_BALOON_MESSAGE_CLASS_NAME)[-1]

            message: WebElement = list_mesage.find_element(
                by=By.CLASS_NAME, value=HTML_MESSAGE_CLASS_NAME).text
            if message[0] == trigger_message:
                return message
            else:
                return ''
        except IndexError:
            return ''
        except NoSuchElementException:
            return ''

    def read_message(self, trigger_message: str = '!') -> Message:
        """
        Reads and returns an object containing the message and message information

        params: 
            trigger_message: str - The trigger command, default '!'.
        """
        global HTML_MESSAGE_CLASS_NAME, HTML_BALOON_MESSAGE_CLASS_NAME, HTML_MESSAGE_SENDER_CLASS_NAME

        try:
            element_present = EC.presence_of_element_located(
                (By.CLASS_NAME, HTML_BALOON_MESSAGE_CLASS_NAME))
            WebDriverWait(self.driver, TIMEOUT, ignored_exceptions=StaleElementReferenceException).until(
                element_present)

            list_mesage: WebElement = self.driver.find_elements(
                by=By.CLASS_NAME, value=HTML_BALOON_MESSAGE_CLASS_NAME)[-1]

            message_info: dict = self.clean_message(list_mesage.find_element(
                by=By.CLASS_NAME, value=HTML_MESSAGE_SENDER_CLASS_NAME).get_attribute('data-pre-plain-text'))

            message: str = list_mesage.find_element(
                by=By.CLASS_NAME, value=HTML_MESSAGE_CLASS_NAME).text
            if message[0] == trigger_message:
                return Message(
                    message_info["message_sender"], message_info["message_date"], message_info["message_hour"], message)
            else:
                return None
        except IndexError:
            return None
        except NoSuchElementException:
            return None

    def clean_message(self, message_data: str) -> dict:
        """
        Receive message data and remove unwanted characters

        params: 
            message_data: str - message data
        """

        message_data = message_data.replace('[', '')
        message_data = message_data.replace(']', '')
        message_data = message_data.replace(',', '')

        message_data = message_data.split()
        message_info: dict = {
            "message_sender": "".join(message_data[2:]).replace(':', '').replace('-', ''),
            "message_date": message_data[1],
            "message_hour": message_data[0],
        }
        return message_info

    def read_image(self, triggerMessage: str, dir: str, file_name: str = 'image') -> str:
        """
        Receive an image from a contact and save then in a specific location.

        params:
             file_name: str - name of the image, by default is 'image'
             triggerMessage: str - the message that trigger the command
             dir: str - the path to save the image
        """
        global TIMEOUT, HTML_IMAGE_BOX_CLASS_NAME, HTML_IMAGE_CLASS_NAME, HTML_LOADING_IMAGE_CLASS_NAME

        time.sleep(1.5)

        try:
            self.get_image_by_xpath(
                "//img[@alt='%s']" % (triggerMessage))[-1].click()
            time.sleep(0.5)
        except IndexError:
            return ''
        except ElementClickInterceptedException:
            return ''

        self.driver.implicitly_wait(1)
        image = self.get_image_by_class_name(HTML_IMAGE_BOX_CLASS_NAME)[-1].find_elements(
            by=By.CLASS_NAME, value=HTML_IMAGE_CLASS_NAME)[-1].screenshot_as_png

        try:
            with open(dir + '/' + file_name + '.png', 'wb') as file:
                file.write(image)
                self.close_image().click()
                return dir + '/' + file_name + '.png'
        except IOError:
            return ''
        except Exception:
            return ''

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
            WebDriverWait(self.driver, TIMEOUT, ignored_exceptions=StaleElementReferenceException).until(
                element_present)
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
            WebDriverWait(self.driver, TIMEOUT, ignored_exceptions=StaleElementReferenceException).until(
                element_present)
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
        global HTMLTEXTBOX_XPATH

        self.find_chat_box(HTMLTEXTBOX_XPATH).send_keys(
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
        global HTMLTEXTBOX_XPATH, HTML_SEARCH_CONTACTS_TEXTBOX_XPATH

        if text_box == 1:
            chat_box: webelement = self.find_chat_box(
                HTML_SEARCH_CONTACTS_TEXTBOX_XPATH)
            self.driver.execute_script(
                "arguments[0].innerHTML = '{}'".format(text), chat_box)
        elif text_box == 2:
            chat_box: webelement = self.find_chat_box(HTMLTEXTBOX_XPATH)
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
            WebDriverWait(self.driver, TIMEOUT, ignored_exceptions=StaleElementReferenceException).until(
                element_present)
            time.sleep(0.5)
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

    def send_link(self, link: str) -> None:
        """Send a link in the chat and wait for Whatsapp to create the content preview"""
        global HTML_LINK_CONFIRMATED_XPATH

        self.write_message(link)
        try:
            element_present = EC.presence_of_element_located(
                (By.XPATH, HTML_LINK_CONFIRMATED_XPATH))
            WebDriverWait(self.driver, TIMEOUT).until(element_present)
            self.click_send_message_button()
        except TimeoutException:
            print(TimeoutException(
                "Error trying to create embed link."
            ))
            self.click_send_message_button()

    def send_image(self, dir: str) -> bool:
        """
        Send an image to the current conversation

        params:
            dir: str - the path the image is located
        """
        global HTMLTEXTBOX_XPATH

        try:
            self.find_chat_box(HTMLTEXTBOX_XPATH).click()
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

    def find_clip_button(self) -> WebElement:
        """
        Search and return button to submit content

        raise - TimeoutException
        """
        global HTML_CLIP_BUTTON_XPATH

        try:
            element_present = EC.presence_of_element_located(
                (By.XPATH, HTML_CLIP_BUTTON_XPATH))
            WebDriverWait(self.driver, TIMEOUT, ignored_exceptions=StaleElementReferenceException).until(
                element_present)
            return self.driver.find_element(by=By.XPATH, value=HTML_CLIP_BUTTON_XPATH)
        except TimeoutException:
            raise TimeoutException(
                "Error trying to find the html element."
            )

    def find_file_input(self) -> WebElement:
        """
        Search and return button to send files

        raise - TimeoutException
        """
        global HTML_SEND_FILE_BUTTON_XPATH

        try:
            element_present = EC.presence_of_element_located(
                (By.XPATH, HTML_SEND_FILE_BUTTON_XPATH))
            WebDriverWait(self.driver, TIMEOUT, ignored_exceptions=StaleElementReferenceException).until(
                element_present)
            return self.driver.find_element(by=By.XPATH, value=HTML_SEND_FILE_BUTTON_XPATH)
        except TimeoutException:
            raise TimeoutException(
                "Error trying to find the html element."
            )

    def find_sticker_input(self) -> WebElement:
        """
        Search and return button to send stickers

        raise - TimeoutException
        """
        global HTML_SEND_STICKER_BUTTON_XPATH

        try:
            element_present = EC.presence_of_element_located(
                (By.XPATH, HTML_SEND_STICKER_BUTTON_XPATH))
            WebDriverWait(self.driver, TIMEOUT, ignored_exceptions=StaleElementReferenceException).until(
                element_present)
            return self.driver.find_element(by=By.XPATH, value=HTML_SEND_STICKER_BUTTON_XPATH)
        except TimeoutException:
            raise TimeoutException(
                "Error trying to find the html element."
            )

    def find_video_image_input(self) -> WebElement:
        """
        Search and return button to send videoss.

        raise - TimeoutException
        """
        global HTML_SEND_IMAGE_VIDEO_BUTTON_XPATH

        try:
            element_present = EC.presence_of_element_located(
                (By.XPATH, HTML_SEND_IMAGE_VIDEO_BUTTON_XPATH))
            WebDriverWait(self.driver, TIMEOUT, ignored_exceptions=StaleElementReferenceException).until(
                element_present)
            return self.driver.find_element(by=By.XPATH, value=HTML_SEND_IMAGE_VIDEO_BUTTON_XPATH)
        except TimeoutException:
            raise TimeoutException(
                "Error trying to find the html element."
            )

    def send_file(self, path: str) -> bool:
        """
        Send a file to the current conversation

        params: path: str - the path of the file to send

        raise - Not specified, under investigation
        """
        try:
            self.find_clip_button().click()
            time.sleep(1)
            self.find_file_input().send_keys(path)
            time.sleep(1)
            self.click_send_message_button()
            return True
        except Exception as err:
            print(err)
            return False

    def to_sticker(self, path: str) -> bool:
        """
        Send a sticker to the current conversation

        params: 
            path: str - The path to the image

        raise - Not specified, under investigation
        """
        try:
            self.find_clip_button().click()
            self.driver.implicitly_wait(1)
            self.find_sticker_input().send_keys(path)
            time.sleep(1)
            self.click_send_message_button()
            return True
        except Exception as err:
            print(err)
            return False

    def resize_image(self, path_to_open: str, path_to_save) -> str:
        """
        Altera o tamanho da imagem para cobrir todo o campo do sticker

        params: 
            path_to_open: str - caminho para abrir a imagem
            path_to_save: str - Caminho para salvar a imagem
        """
        global IMAGE_SIZE

        try:
            image: Image = Image.open(path_to_open)
            image = image.resize(IMAGE_SIZE, Image.ANTIALIAS)
            image.save(path_to_save)
            return path_to_save
        except WindowsError:
            print(WindowsError)
            return ''

    def is_loading(self, html_element: str, by: str) -> bool:
        """
        Check if an html element is loading

        params:
            html_element: str - Path to the web element
            by: str - defines the pricura method
        """
        try:
            element_present = EC.presence_of_element_located(
                (by, html_element))
            WebDriverWait(self.driver, TIMEOUT, ignored_exceptions=StaleElementReferenceException).until(
                element_present)
            return True
        except TimeoutException:
            return False

    def send_video(self, path: str, wait: int) -> bool:
        """
        Send a video to the current conversation

        params: 
            path: str - The path to the video
            wait: int - tentative

        raise - Not specified, under investigation
        """
        global HTML_LOADING_VIDEO_CLASSNAME
        count: int = 0

        try:
            self.find_clip_button().click()
            self.driver.implicitly_wait(1)
            self.find_video_image_input().send_keys(path)
            while count <= wait:
                if self.is_loading(HTML_LOADING_VIDEO_CLASSNAME, By.CLASS_NAME):
                    count += 1
                    time.sleep(2)
                else:
                    self.click_send_message_button()
                    return True
        except Exception as err:
            print(err)
            return False
