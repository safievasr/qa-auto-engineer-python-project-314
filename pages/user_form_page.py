from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.form_page import BaseFormPage


class UserFormPage(BaseFormPage):
    FORM = (By.TAG_NAME, "form")
    EMAIL_INPUT = (By.CSS_SELECTOR, 'input[name="email"]')
    FIRST_NAME_INPUT = (By.CSS_SELECTOR, 'input[name="firstName"]')
    LAST_NAME_INPUT = (By.CSS_SELECTOR, 'input[name="lastName"]')
    SAVE_BTN = (By.CSS_SELECTOR, 'form button[type="submit"]')

    EMAIL_ERROR = (By.XPATH,"//input[@name='email']/ancestor::*[contains(@class,'MuiFormControl')]"
            "//*[contains(@class,'Mui-error')]",
    )
    FIELD_ERROR = EMAIL_ERROR

    def fill(self, user: dict) -> "UserFormPage":
        if user.get("email") is not None:
            self.type(self.EMAIL_INPUT, user["email"])
        if user.get("first_name") is not None:
            self.type(self.FIRST_NAME_INPUT, user["first_name"])
        if user.get("last_name") is not None:
            self.type(self.LAST_NAME_INPUT, user["last_name"])
        return self

    def values(self) -> dict:
        def _val(locator):
            return self.wait.until(
                EC.presence_of_element_located(locator)
            ).get_attribute("value")

        return {
            "email": _val(self.EMAIL_INPUT),
            "first_name": _val(self.FIRST_NAME_INPUT),
            "last_name": _val(self.LAST_NAME_INPUT),
        }

    def has_email_error(self, timeout: float = 3.0) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.EMAIL_ERROR)
            )
            return True
        except Exception:
            try:
                el = self.driver.find_element(*self.EMAIL_INPUT)
                return el.get_attribute("aria-invalid") == "true"
            except Exception:
                return False