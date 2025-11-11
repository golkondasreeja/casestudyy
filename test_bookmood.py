import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def setup_teardown():
    # ✅ Set Chrome options (with Jenkins-compatible settings)
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("detach", True)

    # ✅ Add headless and no-sandbox flags for Jenkins
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # ✅ Specify Chrome binary path (your system path)
    chrome_options.binary_location = r"C:\Users\golko\AppData\Local\Google\Chrome\Application\chrome.exe"

    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.implicitly_wait(5)  # wait up to 5s for elements to appear
    yield driver
    driver.quit()


def get_alert_text(driver):
    # Wait for the alert to appear
    WebDriverWait(driver, 3).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    text = alert.text
    alert.accept()
    return text


def test_empty_username(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "pwd").send_keys("Password123")
    driver.find_element(By.NAME, "sb").click()
    alert_text = get_alert_text(driver)
    assert alert_text == "Username cannot be empty."


def test_empty_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.NAME, "username").send_keys("John")
    driver.find_element(By.NAME, "pwd").clear()
    driver.find_element(By.NAME, "sb").click()
    alert_text = get_alert_text(driver)
    assert alert_text == "Password cannot be empty."


def test_short_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.NAME, "username").send_keys("Jane")
    driver.find_element(By.NAME, "pwd").send_keys("abc")
    driver.find_element(By.NAME, "sb").click()
    alert_text = get_alert_text(driver)
    assert alert_text == "Password must be at least 6 characters long."


def test_valid_login_and_navigation(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.NAME, "username").send_keys("Alice")
    driver.find_element(By.NAME, "pwd").send_keys("abc123")
    driver.find_element(By.NAME, "sb").click()

    # Wait for navigation to /selector page
    WebDriverWait(driver, 5).until(EC.url_contains("selector"))
    assert "selector" in driver.current_url

    # Wait for the mood dropdown to appear
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "mood"))
    )

    # Select a mood (e.g., adventure)
    dropdown = Select(driver.find_element(By.ID, "mood"))
    dropdown.select_by_value("adventure")

    # Click the "See Books" button to submit the form
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Wait for redirection to /suggestions
    WebDriverWait(driver, 5).until(EC.url_contains("suggestions"))
    assert "suggestions" in driver.current_url
