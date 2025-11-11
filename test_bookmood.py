import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from webdriver_manager.chrome import ChromeDriverManager
import time

@pytest.fixture
def setup_teardown():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield driver
    driver.quit()

def get_alert_text(driver):
    alert = Alert(driver)
    text = alert.text
    alert.accept()
    return text

def test_empty_username(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "pwd").send_keys("Password123")
    driver.find_element(By.NAME, "sb").click()
    time.sleep(1)
    alert_text = get_alert_text(driver)
    assert alert_text == "Username cannot be empty."

def test_empty_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.NAME, "username").send_keys("John")
    driver.find_element(By.NAME, "pwd").clear()
    driver.find_element(By.NAME, "sb").click()
    time.sleep(1)
    alert_text = get_alert_text(driver)
    assert alert_text == "Password cannot be empty."

def test_short_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.NAME, "username").send_keys("Jane")
    driver.find_element(By.NAME, "pwd").send_keys("abc")
    driver.find_element(By.NAME, "sb").click()
    time.sleep(1)
    alert_text = get_alert_text(driver)
    assert alert_text == "Password must be at least 6 characters long."

def test_valid_login_and_navigation(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.NAME, "username").send_keys("Alice")
    driver.find_element(By.NAME, "pwd").send_keys("abc123")
    driver.find_element(By.NAME, "sb").click()
    time.sleep(2)
    assert "selector" in driver.current_url
    driver.find_element(By.NAME, "vibe").click()
    time.sleep(2)
    assert "suggestions" in driver.current_url
