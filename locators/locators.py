class YouTubeLocators:
    """A class for YouTube locators"""

    search_field = "//input[@id='search']"
    search_button = "//button[@id='search-icon-legacy']"
    vid_title_wrapper = "//div[@id='title-wrapper']"
    nothing_more_msg = "//yt-formatted-string[text()='Больше нет результатов']"
    player = "//div[@id='player']"
    player_preview = "//div[@class='ytp-inline-preview-scrim ytp-inline-preview-scrim-clear']"
    time_current = "//span[@class='ytp-time-current']"
    time_duration = "//span[@class='ytp-time-duration']"
    main_page_videos = "//ytd-rich-item-renderer[@class='style-scope ytd-rich-grid-row']"
