from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_login_add_to_cart_and_purchase(page):
    driver = page
    wait = WebDriverWait(driver, 15)

    # ==========================================================
    # Критерий 2. Явные ожидания для СТРАНИЦЫ АВТОРИЗАЦИИ
    # ==========================================================
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, '[data-test="username"]'))).send_keys("standard_user")
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, '[data-test="password"]'))).send_keys("secret_sauce")
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '[data-test="login-button"]'))).click()

    # Переход на страницу товаров
    wait.until(EC.url_contains("inventory.html"))

    # ==========================================================
    # Критерий 3. Явные ожидания для СТРАНИЦЫ С ТОВАРАМИ
    # ==========================================================
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '[data-test="add-to-cart-sauce-labs-backpack"]'))).click()
    # Признак, что товар действительно добавлен в корзину
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '[data-test="remove-sauce-labs-backpack"]')))
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '[data-test="shopping-cart-link"]'))).click()

    # Переход в корзину
    wait.until(EC.url_contains("cart.html"))
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '[data-test="checkout"]'))).click()

    # ==========================================================
    # Критерий 4. Явные ожидания для СТРАНИЦЫ ОФОРМЛЕНИЯ (Checkout: Your Information)
    # ==========================================================
    wait.until(EC.url_contains("checkout-step-one.html"))
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, '[data-test="firstName"]'))).send_keys("Ivan")
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, '[data-test="lastName"]'))).send_keys("Ivanov")
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, '[data-test="postalCode"]'))).send_keys("123456")
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '[data-test="continue"]'))).click()

    # ==========================================================
    # Критерий 5. Явное ожидание для СТРАНИЦЫ ОПЛАТЫ (Checkout: Overview)
    # ==========================================================
    wait.until(EC.url_contains("checkout-step-two.html"))
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, '[data-test="finish"]'))).click()

    # ==========================================================
    # Критерий 6. Явное ожидание для ТЕКСТА ОБ УСПЕШНОЙ ПОКУПКЕ
    # ==========================================================
    wait.until(EC.url_contains("checkout-complete.html"))
    header = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, '[data-test="complete-header"]')))
    assert header.text == "Thank you for your order!", \
        f"Ожидали надпись о успешной покупке, получили: {header.text!r}"
