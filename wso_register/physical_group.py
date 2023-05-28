from datetime import datetime

from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as driverWait

from . import RECORDS_ENDPOINT
from .setup import chrome_session
from .wso_data import GroupData, SubmitterData

PHYSICAL_GROUP_CHANGE_PATH = (
    "/changes-existing-al-anon-group/group-records-change-form/"
)
FRAME_FILL_TIMEOUT_SECS = 5.0


def execute_physical_group_change(submitter_data: SubmitterData, group_data: GroupData):
    if not group_data.wso_id:
        raise ValueError("Cannot submit change from for non-registered group")
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
    fill_physical_group_change_name(driver, group_data)
    fill_physical_group_change_participants(driver, group_data)
    fill_physical_group_change_public_phone(driver, group_data)
    fill_physical_group_change_details(driver, group_data)
    if group_data.has_cma():
        fill_physical_group_change_cma(driver, group_data)
    if group_data.has_gr():
        fill_physical_group_change_gr(driver, group_data)
    submit_physical_group_change(driver, submitter_data)
    driver.close()


def fill_physical_group_change_header(driver: ChromeDriver, group_data: GroupData):
    next_button = driverWait(driver, FRAME_FILL_TIMEOUT_SECS).until(
        ec.presence_of_element_located((By.ID, "form-pagebreak-next_97"))
    )
    group_name = driver.find_element(By.ID, "input_156")
    wso_id_number = driver.find_element(By.ID, "input_13")
    district_number = driver.find_element(By.ID, "input_16")
    area_name = driver.find_element(By.ID, "input_17")
    _norcal_area = driver.find_element(
        By.XPATH, "//select[@id='input_17']/option[text()='California North']"
    )
    group_name.send_keys(group_data.name)
    wso_id_number.send_keys(group_data.wso_id)
    district_number.send_keys("26")
    area_name.send_keys("California North")
    next_button.click()


def fill_physical_group_change_status(driver: ChromeDriver, _group_data: GroupData):
    next_button = driverWait(driver, FRAME_FILL_TIMEOUT_SECS).until(
        ec.presence_of_element_located((By.ID, "form-pagebreak-next_98"))
    )
    status_change = driver.find_element(
        By.XPATH, "//input[@type='radio' and @value='Change']"
    )
    change_effective_date = driver.find_element(By.ID, "lite_mode_96")
    status_change.click()
    change_effective_date.send_keys(datetime.today().strftime("%m-%d-%Y"))
    next_button.click()


def fill_physical_group_change_summary(driver: ChromeDriver, group_data: GroupData):
    next_button = driverWait(driver, FRAME_FILL_TIMEOUT_SECS).until(
        ec.presence_of_element_located((By.ID, "form-pagebreak-next_19"))
    )
    name_address_change = driver.find_element(By.ID, "input_102_0")
    participant_change = driver.find_element(By.ID, "input_102_1")
    contact_change = driver.find_element(By.ID, "input_102_2")
    details_change = driver.find_element(By.ID, "input_102_3")
    cma_change = driver.find_element(By.ID, "input_102_4")
    gr_change = driver.find_element(By.ID, "input_102_5")
    name_address_change.click()
    participant_change.click()
    contact_change.click()
    details_change.click()
    if group_data.has_cma():
        cma_change.click()
    if group_data.has_gr():
        gr_change.click()
    next_button.click()


def fill_physical_group_change_name(driver: ChromeDriver, group_data: GroupData):
    next_button = driverWait(driver, FRAME_FILL_TIMEOUT_SECS).until(
        ec.presence_of_element_located((By.ID, "form-pagebreak-next_116"))
    )
    group_name = driver.find_element(By.ID, "input_21")
    language_radio = driver.find_element(
        By.XPATH, f"//input[@type='radio' and @value='{group_data.wso_language()}']"
    )
    meeting_place = driver.find_element(By.ID, "input_23")
    address_line_1 = driver.find_element(By.ID, "input_24_addr_line1")
    address_line_2 = driver.find_element(By.ID, "input_24_addr_line2")
    address_city = driver.find_element(By.ID, "input_80")
    address_state = driver.find_element(By.ID, "input_81")
    address_zip = driver.find_element(By.ID, "input_82")
    address_country = driver.find_element(By.ID, "input_83")
    address_email = driver.find_element(By.ID, "input_25")
    group_name.send_keys(group_data.name)
    language_radio.click()
    meeting_place.send_keys(group_data.wso_meeting_place())
    address_line_1.send_keys(group_data.address_street_1)
    address_line_2.send_keys(group_data.address_street_2)
    address_city.send_keys(group_data.wso_city())
    address_state.send_keys(group_data.wso_state())
    address_zip.send_keys(group_data.wso_zip())
    address_country.send_keys(group_data.wso_country())
    address_email.send_keys(group_data.public_email)
    next_button.click()


def fill_physical_group_change_participants(
    driver: ChromeDriver, group_data: GroupData
):
    next_button = driverWait(driver, FRAME_FILL_TIMEOUT_SECS).until(
        ec.presence_of_element_located((By.ID, "form-pagebreak-next_134"))
    )
    if wso_pt := group_data.wso_participant_type():
        checkbox = driver.find_element(
            By.XPATH, f"//input[@type='checkbox' and @value='{wso_pt}']"
        )
        checkbox.click()
    next_button.click()


def fill_physical_group_change_public_phone(
    driver: ChromeDriver, group_data: GroupData
):
    next_button = driverWait(driver, FRAME_FILL_TIMEOUT_SECS).until(
        ec.presence_of_element_located((By.ID, "form-pagebreak-next_135"))
    )
    if wso_pt := group_data.wso_participant_type():
        checkbox = driver.find_element(
            By.XPATH, f"//input[@type='checkbox' and @value='{wso_pt}']"
        )
        checkbox.click()
    next_button.click()


def fill_physical_group_change_details(driver: ChromeDriver, group_data: GroupData):
    next_button = driverWait(driver, FRAME_FILL_TIMEOUT_SECS).until(
        ec.presence_of_element_located((By.ID, "form-pagebreak-next_133"))
    )
    wso_day, wso_hour, wso_minute, wso_am_pm = group_data.wso_schedule()
    day_menu = driver.find_element(By.ID, "input_30")
    day_menu.send_keys(wso_day)
    start_hour_menu = driver.find_element(By.ID, "input_31")
    start_hour_menu.send_keys(wso_hour)
    start_minute_menu = driver.find_element(By.ID, "input_32")
    start_minute_menu.send_keys(wso_minute)
    am_pm_menu = driver.find_element(By.ID, "input_33")
    am_pm_menu.send_keys(wso_am_pm)
    attendees_radio = driver.find_element(
        By.XPATH, f"//input[@type='radio' and @value='{group_data.wso_attendees()}']"
    )
    attendees_radio.click()
    language_text = driver.find_element(By.ID, "input_78")
    language_text.send_keys(group_data.wso_language(False))
    member_count = driver.find_element(By.ID, "input_47")
    member_count.send_keys("")
    for wso_option in group_data.wso_options():
        checkbox = driver.find_element(
            By.XPATH, f"//input[@type='checkbox' and @value='{wso_option}']"
        )
        checkbox.click()
    location_instructions = driver.find_element(By.ID, "input_39")
    location_instructions.send_keys(group_data.wso_location())
    next_button.click()


def fill_physical_group_change_cma(driver: ChromeDriver, group_data: GroupData):
    next_button = driverWait(driver, FRAME_FILL_TIMEOUT_SECS).until(
        ec.presence_of_element_located((By.ID, "form-pagebreak-next_64"))
    )
    first_name = driver.find_element(By.ID, "first_66")
    first_name.send_keys(group_data.cma_first_name)
    last_name = driver.find_element(By.ID, "last_66")
    last_name.send_keys(group_data.cma_last_name)
    street_address_1 = driver.find_element(By.ID, "input_67_addr_line1")
    street_address_1.send_keys(group_data.cma_street_address_1)
    street_address_2 = driver.find_element(By.ID, "input_67_addr_line2")
    street_address_2.send_keys(group_data.cma_street_address_2)
    city = driver.find_element(By.ID, "input_84")
    city.send_keys(group_data.cma_city)
    state = driver.find_element(By.ID, "input_85")
    state.send_keys(group_data.cma_state)
    zip_field = driver.find_element(By.ID, "input_86")
    zip_field.send_keys(group_data.cma_zip)
    country = driver.find_element(By.ID, "input_87")
    country.send_keys(group_data.wso_cma_country())
    area, number = group_data.wso_cma_phone()
    phone_area = driver.find_element(By.ID, "input_68_area")
    phone_area.send_keys(area)
    phone_number = driver.find_element(By.ID, "input_68_phone")
    phone_number.send_keys(number)
    email = driver.find_element(By.ID, "input_69")
    email.send_keys(group_data.cma_email)
    next_button.click()


def fill_physical_group_change_gr(driver: ChromeDriver, group_data: GroupData):
    next_button = driverWait(driver, FRAME_FILL_TIMEOUT_SECS).until(
        ec.presence_of_element_located((By.ID, "form-pagebreak-next_148"))
    )
    first_name = driver.find_element(By.ID, "first_74")
    first_name.send_keys(group_data.gr_first_name)
    last_name = driver.find_element(By.ID, "last_74")
    last_name.send_keys(group_data.gr_last_name)
    street_address_1 = driver.find_element(By.ID, "input_73_addr_line1")
    street_address_1.send_keys(group_data.gr_street_address_1)
    street_address_2 = driver.find_element(By.ID, "input_73_addr_line2")
    street_address_2.send_keys(group_data.gr_street_address_2)
    city = driver.find_element(By.ID, "input_88")
    city.send_keys(group_data.gr_city)
    state = driver.find_element(By.ID, "input_89")
    state.send_keys(group_data.gr_state)
    zip_field = driver.find_element(By.ID, "input_90")
    zip_field.send_keys(group_data.gr_zip)
    country = driver.find_element(By.ID, "input_91")
    country.send_keys(group_data.wso_gr_country())
    area, number = group_data.wso_gr_phone()
    phone_area = driver.find_element(By.ID, "input_72_area")
    phone_area.send_keys(area)
    phone_number = driver.find_element(By.ID, "input_72_phone")
    phone_number.send_keys(number)
    email = driver.find_element(By.ID, "input_71")
    email.send_keys(group_data.gr_email)
    comments = driver.find_element(By.ID, "input_95")
    comments.send_keys(group_data.gr_comment)
    next_button.click()


def submit_physical_group_change(driver: ChromeDriver, submitter_data: SubmitterData):
    submit_button = driverWait(driver, FRAME_FILL_TIMEOUT_SECS).until(
        ec.presence_of_element_located((By.ID, "input_2"))
    )
    submitted_by = driver.find_element(By.ID, "input_43")
    submitted_by.send_keys(submitter_data.name)
    submit_date = driver.find_element(By.ID, "lite_mode_44")
    submit_date.send_keys(datetime.today().strftime("%m-%d-%Y"))
    area, number = submitter_data.wso_phone()
    phone_area = driver.find_element(By.ID, "input_45_area")
    phone_area.send_keys(area)
    phone_number = driver.find_element(By.ID, "input_45_phone")
    phone_number.send_keys(number)
    email = driver.find_element(By.ID, "input_46")
    email.send_keys(submitter_data.email)
    submit_button.click()
