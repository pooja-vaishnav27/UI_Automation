from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pytest

@pytest.fixture(scope="module")
def setup():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("https://www.tendable.com")
    driver.maximize_window()
    yield driver
    driver.quit()

def test_top_level_menus(setup):
    driver = setup
    menu_items = ["Home", "Our Story", "Our Solution", "Why Tendable"]
    
    for item in menu_items:
        menu = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, item)))
        assert menu.is_displayed() and menu.is_enabled()
        menu.click()
        assert driver.current_url != "https://www.tendable.com"

def test_request_demo_button(setup):
    driver = setup
    menu_items = ["Home", "Our Story", "Our Solution", "Why Tendable"]
    
    for item in menu_items:
        driver.find_element(By.LINK_TEXT, item).click()
        demo_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Request a Demo')]")))
        assert demo_button.is_displayed() and demo_button.is_enabled()

def test_contact_us_form(setup):
    driver = setup
    driver.find_element(By.LINK_TEXT, "Contact Us").click()
    
    marketing_option = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//option[contains(text(), 'Marketing')]")))
    marketing_option.click()
    
    driver.find_element(By.NAME, "your-name").send_keys("Test Name")
    driver.find_element(By.NAME, "your-email").send_keys("test@example.com")
    driver.find_element(By.NAME, "your-phone").send_keys("1234567890")
    driver.find_element(By.XPATH, "//input[@type='submit']").click()
    
    error_message = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'This field is required.')]")))
    assert error_message.is_displayed()