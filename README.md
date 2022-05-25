# Introduction
This is a project of UI-testing using Python, Selenium, Pytest, Allure.

Testing website: https://www.youtube.com/

# Files

**/base**
- seleniumbase.py — contains PageObject pattern implementation

**/locators**
- locators.py — contains helper classes to define web elements on web pages

**/pages**
- youtubepage.py — contains methods that interact with YouTube page web elements

**/tests**
- conftest.py — contains the fixture that is used by tests, the plugin that makes screenshot when a test fail,
the function that creates a environment.properties file
- test_homepage.py — contains UI tests for YouTube page

**/allure-results-chrome** — default Allure directory for chrome. Can be changed via --alluredir="dir_name" command
- categories.json — file that fills the "categories" section in Allure report
- environment.properties — file that is created before a first test execution starts. 
It fills the "environment" section in Allure report

**pytest.ini** — configuration file. Contains pytest launch options

**requirements.txt** — requirements file

# Prerequisites

1. Install all requirements:

```bash
pip install -r requirements.txt
```

2. Download and move to the repo directory WebDrivers compatible with your OS and browser's version:

- for Chrome: https://chromedriver.chromium.org/downloads
- for Firefox: https://github.com/mozilla/geckodriver/releases

3. To generate Allure reports install Allure:

https://docs.qameta.io/allure/#_installing_a_commandline

# How to run

Quickrun all the tests in the directory:

    pytest

Specify launch options in **pytest.ini** file and/or using command line.

Pytest documentation can be found at https://docs.pytest.org/

Custom options: 
- --browser_name (chrome or firefox) — to choose a browser (default is **_chrome_**)
- --headless — to launch browsers in 'headless' mode

# Make an Allure report

If tests were run with --alluredir="allure-results-chrome" (by default) option, it is possible to generate an Allure report:

    allure serve allure-results-chrome

Allure documentation can be found at https://docs.qameta.io/allure/
