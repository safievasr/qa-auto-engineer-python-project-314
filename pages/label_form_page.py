from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from core.form_page import BaseFormPage
from selenium.webdriver.support.ui import WebDriverWait


class LabelFormPage(BaseFormPage):
    NAME_INPUT = (By.CSS_SELECTOR, 'input[name="name"]')

    NAME_ERROR = (By.ID, ":ra:-helper-text")

    def fill(self, label: dict):
        if label.get("name") is not None:
            self.type(self.NAME_INPUT, label["name"])
        return self

    def values(self) -> dict:
        el = self.wait.until(EC.presence_of_element_located(self.NAME_INPUT))
        return {"name": el.get_attribute("value")}

    def has_name_error(self, timeout: float = 3.0) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.NAME_ERROR)
            )
            return True
        except Exception:
            try:
                el = self.driver.find_element(*self.NAME_INPUT)
                return el.get_attribute("aria-invalid") == "true"
            except Exception:
                return False