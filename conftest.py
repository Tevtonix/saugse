import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

BROWSERS = ["chrome", "firefox", "edge"]


def pytest_addoption(parser):
    """Хук: CLI-опция pytest для URL сайта."""
    parser.addoption(
        "--url",
        action="store",
        default="https://www.saucedemo.com/",
        help="URL сайта для тестирования (по умолчанию: https://www.saucedemo.com/)",
    )


@pytest.fixture(params=BROWSERS)
def driver(request):
    """Фикстура управления браузером (мультибраузерность)."""
    name = request.param
    if name == "chrome":
        opts = ChromeOptions()
        opts.add_experimental_option("prefs", {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "password_manager.enabled": False,
        })
        opts.add_argument("--incognito")
        drv = webdriver.Chrome(options=opts)
    elif name == "firefox":
        drv = webdriver.Firefox()
    elif name == "edge":
        opts = EdgeOptions()
        opts.add_experimental_option("prefs", {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        })
        opts.add_argument("--inprivate")
        drv = webdriver.Edge(options=opts)
    else:
        raise ValueError(f"Неизвестный браузер: {name}")
    drv.maximize_window()
    yield drv
    drv.quit()


@pytest.fixture(scope="session")
def url(request):
    """Фикстура URL: значение из опции --url."""
    return request.config.getoption("--url")


@pytest.fixture
def page(driver, url):
    """Открытие сайта перед тестом."""
    driver.get(url)
    return driver