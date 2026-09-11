from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_login_add_to_cart_and_purchase(page):
    driver = page
    wait = WebDriverWait(driver, 10)

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
    wait.until(EC.url_contains("checkout-step-one.html"))

    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, '[data-test="firstName"]'))).send_keys("Ivan")
    driver.find_element(By.CSS_SELECTOR, '[data-test="lastName"]').send_keys("Ivanov")
    driver.find_element(By.CSS_SELECTOR, '[data-test="postalCode"]').send_keys("123456")
    driver.find_element(By.CSS_SELECTOR, '[data-test="continue"]').click()
    wait.until(EC.url_contains("checkout-step-two.html"))

    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '[data-test="finish"]'))).click()
    wait.until(EC.url_contains("checkout-complete.html"))

    header = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, '[data-test="complete-header"]')))
    assert header.text == "Thank you for your order!", \
        f"Ожидали надпись о успешной покупке, получили: {header.text!r}"