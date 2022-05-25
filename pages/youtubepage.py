import time
from utils.convert_time_helper import convert_secs_to_time_str, convert_str_time_to_secs
from base.seleniumbase import SeleniumBase
from locators.locators import YouTubeLocators
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
from typing import List, Union
import allure


class YouTubePage(SeleniumBase):

    def __init__(self, driver):
        super().__init__(driver)
        self._driver.get('https://www.youtube.com/')
        self._is_visible('xpath', YouTubeLocators.search_field)   # Переопределение стратегии загрузки сайта
        self._is_visible('xpath', YouTubeLocators.search_button)  # чтобы Ютуб долго не прогружался
        self._driver.execute_script("window.stop();")

    @allure.step('Набор заданного текста в поле поиска')
    def search_by_text(self, text):
        self._is_present('xpath', YouTubeLocators.search_field).send_keys(text)

    @allure.step('Клик по кнопке "Найти"')
    def click_search_button(self):
        self._is_clickable('xpath', YouTubeLocators.search_button).click()

    @allure.step('Поиск видео по названию')
    def find_video(self, name) -> WebElement:
        """
        Поиск видео до тех пор, пока не появится сообщение: 'Больше нет результатов'.
        Проверка производится по названиям видимых (загруженных) видео на странице результатов поиска.
        Когда появляется вышеупомянутое сообщение, проверка производится последный раз.
        Функция возвращает найденный элемент (видео) или вызывает соответсвующий AssertionError.
        Так как подгружается не всегда одинаковое количество видео, номер последнего подгруженного запоминается,
        в следующей итерации поиск начинается со следующего подгруженного видео.
        """
        def inner(text, last=False, interval=[]):

            page_elements = self._are_present('xpath', YouTubeLocators.vid_title_wrapper)
            if not interval:
                finding_element = self._get_element_from_list_by_text(page_elements, text)
            else:
                begin_with = page_elements.index(interval[-1]) + 1
                finding_element = self._get_element_from_list_by_text(page_elements[begin_with:], text)
            if finding_element is not None:
                return finding_element
            if not last:
                last_element = page_elements[-1]
                self._scroll_to_element(last_element)
                interval.append(last_element)

        while True:

            try:
                msg = self._driver.find_element_by_xpath(YouTubeLocators.nothing_more_msg)
            except NoSuchElementException:
                result = inner(name)
                if isinstance(result, WebElement):
                    return result
            else:
                result = inner(name, last=True)
                if isinstance(result, WebElement):
                    return result
                assert False, 'Видео не найдено'

    @allure.step('Клик по найденному видео')
    def click_video(self, video: WebElement):
        video.click()

    @allure.step('Проверка: Видео начало проигрывание')
    def video_started(self) -> bool:
        try:
            if self._text_is_present('xpath', YouTubeLocators.time_current, text='0:01'):
                return True
        except TimeoutException:
            return False

    @allure.step('Проверка: {progress} видео прошло')
    def progress_of_video(self, progress: str) -> bool:
        player_element = self._is_present('xpath', YouTubeLocators.player)   # Для взаимодействия с плейером
        duration_element = self._is_present('xpath', YouTubeLocators.time_duration)
        try:
            self._move_to_and_move_on_element(player_element)
        except ElementNotInteractableException:
            player_element = self._is_present('xpath', YouTubeLocators.player_preview)  # Для взаимодействия с превью
            self._move_to_and_move_on_element(player_element)

        current_element = self._is_present('xpath', YouTubeLocators.time_current)
        duration = duration_element.text
        current = current_element.text
        current_int = convert_str_time_to_secs(current)
        print(f'{current=} {duration=}')
        numerator, denominator = map(int, progress.split('/'))
        progress_of_vid = round(convert_str_time_to_secs(duration) * numerator / denominator)

        progress_str = convert_secs_to_time_str(progress_of_vid)
        time.sleep(abs(progress_of_vid - current_int - 3))  # Ждем до нужного времени и начинаем сравнивать с запасом в 3 секунды
        for _ in range(1, 20):
            self._move_mouse_a_bit()
            current_element = self._is_present('xpath', YouTubeLocators.time_current)
            current = current_element.text
            print(f'{current=} {duration=} {progress_str=} in FOR')
            if current == progress_str:
                return True
            time.sleep(0.2)
        return False

    @allure.step('Поиск видео на странице по индексу')
    def select_video_by_index(self, index) -> WebElement:
        while True:
            list_of_videos = self._are_present('xpath', YouTubeLocators.main_page_videos)
            if len(list_of_videos) > index:
                return list_of_videos[index]
            self._scroll_to_element(list_of_videos[-1])

    @allure.step('Наведение на заданное видео')
    def hover_video(self, video: WebElement):
        self._scroll_to_element(video)
        self._move_to_and_move_on_element(video)

    @allure.step('Проверка: Предпросмотр доступен')
    def preview_available(self, elements: Union[List[WebElement], WebElement]):
        for item in self._get_text_from_webelements(elements):
            return False if 'Предпросмотр недоступен' in item else True
