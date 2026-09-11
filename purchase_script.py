import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

options = Options()
options.add_experimental_option("prefs", {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False,
    "password_manager.enabled": False,
})
options.add_argument("--incognito")

driver = webdriver.Chrome(options=options)
driver.maximize_window()
wait = WebDriverWait(driver, 10)

try:
    driver.get("https://www.saucedemo.com/")

    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, '[data-test="username"]'))).send_keys("standard_user")
    driver.find_element(By.CSS_SELECTOR, '[data-test="password"]').send_keys("secret_sauce")
    driver.find_element(By.CSS_SELECTOR, '[data-test="login-button"]').click()

    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '[data-test="add-to-cart-sauce-labs-backpack"]'))).click()
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '[data-test="remove-sauce-labs-backpack"]')))

    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '[data-test="shopping-cart-link"]'))).click()
    wait.until(EC.url_contains("cart.html"))

    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '[data-test="checkout"]'))).click()
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, '[data-test="firstName"]'))).send_keys("Ivan")
    driver.find_element(By.CSS_SELECTOR, '[data-test="lastName"]').send_keys("Ivanov")
    driver.find_element(By.CSS_SELECTOR, '[data-test="postalCode"]').send_keys("123456")
    driver.find_element(By.CSS_SELECTOR, '[data-test="continue"]').click()
    wait.until(EC.url_contains("checkout-step-two.html"))

    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '[data-test="finish"]'))).click()
    header = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, '[data-test="complete-header"]')))
    print("Покупка завершена:", header.text)

finally:
    time.sleep(2)
    driver.quit()