import allure
from allure_commons.types import AttachmentType
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as GoogleOptions
from selenium.webdriver.chrome.service import Service as GoogleService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pathlib
from pathlib import Path

set_environment = True  # The quantity limit of the 'create_allure_environment_properties' func calls
                        # if "True": environment.properties file will be created before the first test
                        # if "False": NEW environment.properties file will not be created


def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="chrome")
    parser.addoption("--headless", action="store_true")  # False if --headless is not provided as CLI option


def create_allure_environment_properties(browser_name, allure_dir, driver):
    """This function creates environment.properties file for Allure reports once per session."""
    if allure_dir is None:
        return "\n\nAllure directory didn't select. To select add option --alluredir='directory_name'\n"
    else:
        browser_version = driver.capabilities['browserVersion']
        driver_version = ""
        if browser_name == "chrome":
            driver_version = driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
        elif browser_name == "firefox":
            driver_version = driver.capabilities['moz:geckodriverVersion']
        with open(f'{allure_dir}{pathlib.os.sep}environment.properties', 'w') as file:
            file.write(f'Browser={browser_name.capitalize()}')
            file.write(f'\nBrowser.Version={browser_version}')
            file.write(f'\nDriver.Version={driver_version}')  # browser_name will exactly be in IF or ELIF
        return "\n\nEnvironment properties for Allure (environment.properties file) was successfully set\n"


def get_chrome_options(request):
    options = GoogleOptions()
    if request.config.option.headless:
        options.add_argument('--headless')
    else:
        options.add_argument("--start-maximized")

    """for performance improvement:"""
    options.add_argument("--no-proxy-server")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    return options


def get_firefox_options(request):
    profile = FirefoxProfile()
    options = FirefoxOptions()
    options.page_load_strategy = 'none'
    if request.config.option.headless:
        options.add_argument('--headless')
    else:
        options.add_argument("--start-maximized")
    return profile, options


def get_chrome_webdriver(request):
    options = get_chrome_options(request)
    service = GoogleService(str(Path(pathlib.Path.cwd() / 'chromedriver')))
    return service, options


def get_firefox_webdriver(request):
    profile, options = get_firefox_options(request)
    service = FirefoxService(str(Path(pathlib.Path.cwd() / 'geckodriver')))
    return service, options, profile


@pytest.fixture
def web_driver_init(request):
    """Init before a test"""
    browser_name = request.config.option.browser_name
    allure_dir = request.config.option.allure_report_dir
    global set_environment
    if browser_name == "chrome":
        capa = DesiredCapabilities.CHROME       # ?????????????????????????????? ?????????????????? ???????????????? ??????????
        capa['pageLoadStrategy'] = "none"       # ?????????? ???????? ?????????? ???? ??????????????????????
        s, o = get_chrome_webdriver(request)
        driver = webdriver.Chrome(service=s, options=o, desired_capabilities=capa)
    elif browser_name == "firefox":
        capa = DesiredCapabilities.FIREFOX
        capa['pageLoadStrategy'] = "none"
        s, o, p = get_firefox_webdriver(request)
        driver = webdriver.Firefox(service=s, firefox_profile=p, options=o, desired_capabilities=capa)

    else:
        raise ValueError("Wrong '--browser_name' option. Available: chrome, firefox.")
    if request.cls is not None:
        request.cls.driver = driver
    if set_environment:
        allure_environment_status = create_allure_environment_properties(browser_name, allure_dir, driver)
        set_environment = False
        print(allure_environment_status)
    yield driver
    """Actions after a test"""
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):  # ?????????????? ???????????????? ?????? ?????????????? ?????????? ???? ?????????? ????????????????????
    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call' and rep.outcome == 'failed':
        driver = item.funcargs["web_driver_init"]
        allure.attach(driver.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)
