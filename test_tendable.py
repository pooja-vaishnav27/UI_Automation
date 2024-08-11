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
    """
    Initializes a Chrome WebDriver instance and navigates to the Tendable website.
    
    This fixture is scoped to the module level, meaning the WebDriver instance
    is shared across all tests in the module. The browser window is maximized
    to ensure all elements are visible. After all tests have run, the WebDriver
    instance is closed.

    Yields:
        WebDriver: An instance of Chrome WebDriver pointed at the Tendable homepage.
    """
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("https://www.tendable.com")
    driver.maximize_window()
    yield driver
    driver.quit()

def test_top_level_menus(setup):
    """
    Verifies that the top-level menu items are accessible, clickable, and
    navigate to a different URL on the Tendable website.

    This test checks the presence, visibility, and functionality of the
    following menu items: Home, Our Story, Our Solution, and Why Tendable.
    For each menu item, it is ensured that clicking on it does not keep
    the browser on the homepage.

    Args:
        setup (WebDriver): The WebDriver instance provided by the `setup` fixture.
    """
    driver = setup
    menu_items = ["Home", "Our Story", "Our Solution", "Why Tendable"]
    
    for item in menu_items:
        menu = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, item)))
        assert menu.is_displayed() and menu.is_enabled()
        menu.click()
        assert driver.current_url != "https://www.tendable.com"

def test_request_demo_button(setup):
    """
    Verifies that the "Request a Demo" button is present and active on each of the
    top-level menu pages of the Tendable website.

    This test iterates through the top-level menu items: Home, Our Story, Our Solution,
    and Why Tendable. For each page, it checks if the "Request a Demo" button is visible
    and clickable.

    Args:
        setup (WebDriver): The WebDriver instance provided by the `setup` fixture.
    """
    driver = setup
    menu_items = ["Home", "Our Story", "Our Solution", "Why Tendable"]
    
    for item in menu_items:
        driver.find_element(By.LINK_TEXT, item).click()
        demo_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Request a Demo')]")))
        assert demo_button.is_displayed() and demo_button.is_enabled()

def test_contact_us_form(setup):
    """
    Tests the "Contact Us" form by selecting the "Marketing" option and attempting to
    submit the form without filling out the "Message" field, verifying that an error
    message appears.

    This test navigates to the "Contact Us" page, fills in the required fields except
    for the "Message" field, and submits the form. It confirms that an error message
    is displayed indicating that the "Message" field is required.

    Args:
        setup (WebDriver): The WebDriver instance provided by the `setup` fixture.
    """
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