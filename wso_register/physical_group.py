from datetime import datetime

from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as driverWait

from . import RECORDS_ENDPOINT
from .setup import chrome_session

PHYSICAL_GROUP_CHANGE_PATH = (
    "/changes-existing-al-anon-group/group-records-change-form/"
)


def execute_physical_group_change(group_data: dict):
    driver: ChromeDriver = chrome_session(
        start_url=RECORDS_ENDPOINT + PHYSICAL_GROUP_CHANGE_PATH
    )
    try:
        driverWait(driver, 3).until(
            ec.frame_to_be_available_and_switch_to_it(
                (By.XPATH, "//*[@title='Group Records Change']")
            )
        )
    except TimeoutException:
        raise ReferenceError(
            "Group Records Change page doesn't have the correct structure"
        )
    fill_physical_group_change_header(driver, group_data)
    fill_physical_group_change_status(driver, group_data)
    fill_physical_group_change_summary(driver, group_data)
    pass


def fill_physical_group_change_header(driver: ChromeDriver, group_data: dict):
    locator = (By.ID, "input_156")
    group_name = driverWait(driver, 2).until(ec.presence_of_element_located(locator))
    wso_id_number = driver.find_element(By.ID, "input_13")
    district_number = driver.find_element(By.ID, "input_16")
    area_name = driver.find_element(By.ID, "input_17")
    _norcal_area = driver.find_element(
        By.XPATH, "//select[@id='input_17']/option[text()='California North']"
    )
    next_button = driver.find_element(By.ID, "form-pagebreak-next_97")
    group_name.send_keys(group_data["group_name"])
    wso_id_number.send_keys(group_data["wso_id_number"])
    district_number.send_keys("26")
    area_name.send_keys("California North")
    next_button.click()


def fill_physical_group_change_status(driver: ChromeDriver, _group_data: dict):
    locator = (By.XPATH, "//input[@type='radio' and @value='Change']")
    status_change = driverWait(driver, 2).until(ec.presence_of_element_located(locator))
    change_effective_date = driver.find_element(By.ID, "lite_mode_96")
    next_button = driver.find_element(By.ID, "form-pagebreak-next_98")
    status_change.click()
    change_effective_date.send_keys(datetime.today().strftime("%m-%d-%Y"))
    next_button.click()


def fill_physical_group_change_summary(driver: ChromeDriver, _group_data: dict):
    locator = (By.ID, "input_102_0")
    name_address_change = driverWait(driver, 2).until(
        ec.presence_of_element_located(locator)
    )
    participant_change = driver.find_element(By.ID, "input_102_1")
    contact_change = driver.find_element(By.ID, "input_102_2")
    schedule_details_change = driver.find_element(By.ID, "input_102_3")
    cma_change = driver.find_element(By.ID, "input_102_4")
    gr_change = driver.find_element(By.ID, "input_102_5")
    next_button = driver.find_element(By.ID, "form-pagebreak-next_19")
    name_address_change.click()
    participant_change.click()
    contact_change.click()
    schedule_details_change.click()
    cma_change.click()
    gr_change.click()
    next_button.click()
