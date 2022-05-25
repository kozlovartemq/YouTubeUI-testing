import pytest
import allure
from pages.youtubepage import YouTubePage


@allure.feature("Тесты воспроизведения YouTube видео")
@pytest.mark.usefixtures('web_driver_init')
class TestYoutubeUI:

    @allure.story("Проверка поиска и воспроизведения видео")
    @pytest.mark.parametrize('test_data', [['Non-Fungible Planet', 'Non-Fungible Planet | YouTube'],
                                           ['Never Gonna Give You Up', "Rick Astley - Never Gonna Give You Up (Instrumental)"],
                                           pytest.param(['somelongstringsovideowillnofound', 'SomeVideo'], marks=pytest.mark.xfail(reason='There should not be a video here'))],
                             ids=['close_video', 'far_video', 'no_video'])
    def test_search_and_play_video(self, test_data):
        """Verifying the ability to search and play videos"""
        search_n_play = YouTubePage(self.driver)
        search_text, video_name = test_data

        search_n_play.search_by_text(search_text)
        search_n_play.click_search_button()
        video = search_n_play.find_video(video_name)
        search_n_play.click_video(video)

        assert search_n_play.video_started(), 'Видео не началось'
        assert search_n_play.progress_of_video('1/3'), 'Видео не дошло до своей трети'
        assert search_n_play.progress_of_video('4/5'), 'Видео не дошло до 4/5 части'

    @pytest.mark.parametrize('index', [3])
    @allure.story("Проверка воспроизведения видео при hover")
    def test_hover_and_play_video(self, index):
        """Verifying the ability play videos when hover"""
        test_hover = YouTubePage(self.driver)
        video = test_hover.select_video_by_index(index)  # Индекс начинается с 0
        test_hover.hover_video(video)

        assert test_hover.preview_available(video), 'Предпросмотр недоступен для данного видео'
        assert test_hover.video_started(), 'Видео не началось'
        assert test_hover.progress_of_video('1/3'), 'Видео не дошло до своей трети'
        assert test_hover.progress_of_video('4/5'), 'Видео не дошло до 4/5 части'
