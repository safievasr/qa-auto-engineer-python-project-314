from selenium.webdriver.common.by import By
from core.page import BasePage


class LoginPage(BasePage):
    USERNAME = (By.CSS_SELECTOR, 'input[name="username"]')
    PASSWORD = (By.CSS_SELECTOR, 'input[name="password"]')
    SUBMIT = (By.CSS_SELECTOR, 'button[type="submit"]')
    FORM = (By.TAG_NAME, "form")

    def open(self, base_url: str) -> "LoginPage":
        self.driver.get(base_url + "/")
        self.wait.until(lambda d: self.is_visible(self.FORM))
        return self

    def fill_username(self, username: str) -> "LoginPage":
        self.type(self.USERNAME, username)
        return self

    def fill_password(self, password: str) -> "LoginPage":
        self.type(self.PASSWORD, password)
        return self

    def submit(self) -> "LoginPage":
        self.click(self.SUBMIT)
        return self

    def login(self, username: str, password: str) -> "LoginPage":
        self.fill_username(username)
        self.fill_password(password)
        self.submit()
        return self

    def is_opened(self) -> bool:
        return self.is_visible(self.FORM) and self.is_visible(self.SUBMIT)