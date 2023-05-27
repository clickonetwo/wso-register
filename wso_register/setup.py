from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from webdriver_manager.chrome import ChromeDriverManager


def chrome_session(start_url: str, wait: float | None = None) -> ChromeDriver:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    if wait:
        driver.implicitly_wait(wait)
    driver.get(start_url)
    return driver
