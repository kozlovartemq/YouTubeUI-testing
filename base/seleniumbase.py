from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from typing import List, Union
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException


class SeleniumBase:
    def __init__(self, driver):
        self._driver = driver
        self.__wait = WebDriverWait(driver, 20)  # Timeout = 10 secs

    @staticmethod
    def __get_selenium_by(find_by: str) -> dict:
        find_by = find_by.lower()
        locating = dict(xpath=By.XPATH,
                        css=By.CSS_SELECTOR,
                        linktext=By.LINK_TEXT,
                        part_of_linktext=By.PARTIAL_LINK_TEXT,
                        tagname=By.TAG_NAME)
        return locating[find_by]

    def _is_visible(self, find_by: str, locator: str) -> WebElement:
        return self.__wait.until(ec.visibility_of_element_located((self.__get_selenium_by(find_by), locator)))

    def _is_present(self, find_by: str, locator: str) -> WebElement:
        return self.__wait.until(ec.presence_of_element_located((self.__get_selenium_by(find_by), locator)))

    def _is_not_present(self, find_by: str, locator: str) -> WebElement:
        return self.__wait.until(ec.invisibility_of_element_located((self.__get_selenium_by(find_by), locator)))

    def _are_visible(self, find_by: str, locator: str) -> List[WebElement]:
        return self.__wait.until(ec.visibility_of_all_elements_located((self.__get_selenium_by(find_by), locator)))

    def _are_present(self, find_by: str, locator: str) -> List[WebElement]:
        return self.__wait.until(ec.presence_of_all_elements_located((self.__get_selenium_by(find_by), locator)))

    def _is_clickable(self, find_by: str, locator: str) -> WebElement:
        return self.__wait.until(ec.element_to_be_clickable((self.__get_selenium_by(find_by), locator)))

    def _text_is_present(self, find_by: str, locator: str, text) -> WebElement:
        return self.__wait.until(ec.text_to_be_present_in_element((self.__get_selenium_by(find_by), locator), text))

    @staticmethod
    def _get_text_from_webelements(elements: Union[List[WebElement], WebElement]) -> List[str]:
        if isinstance(elements, list):
            return [finding_text.text for finding_text in elements]
        else:
            return [elements.text]

    @staticmethod
    def _get_element_from_list_by_text(list_of_elements: List[WebElement], text: str):
        """The method finds a certain WebElement from a given List of WebElements by the given text (case-sensitive).
            If several elements is found the method will return the first one."""
        if list_of_elements is None:
            return None

        web_element = [element for element in list_of_elements if text == element.text]
        if web_element:  # len(element) != 0
            return web_element[0]
        return None

    def _get_select_list(self, find_by: str, locator: str):
        return Select(self._is_present(find_by, locator))

    def find_text_on_page(self, text) -> bool:
        return text in self._driver.page_source

    @staticmethod
    def _find_text_inside_elements(element: List[WebElement], text: str) -> bool:
        a = [elem.text.lower() for elem in element]
        for arg in a:
            if arg.find(text) != -1:
                return True
        return False

    @staticmethod
    def _scroll_to_element(element: WebElement):
        return element.location_once_scrolled_into_view  # return None if element is not visible

    def _move_mouse_a_bit(self):
        ActionChains(self._driver).move_by_offset(2, 2).perform()

    def _move_to_and_move_on_element(self, element: WebElement):
        action = ActionChains(self._driver)
        action.move_to_element(element).move_by_offset(2, 2)
        try:
            action.perform()
        except WebDriverException:
            print(f'WebDriverException was raised, but ignored')
