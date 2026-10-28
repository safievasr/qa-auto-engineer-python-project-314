from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from core.form_page import BaseFormPage
from selenium.webdriver.support.ui import WebDriverWait


class StatusFormPage(BaseFormPage):
    NAME_INPUT = (By.CSS_SELECTOR, 'input[name="name"]')
    SLUG_INPUT = (By.CSS_SELECTOR, 'input[name="slug"]')

    NAME_ERROR = (By.ID, ":r2r:-helper-text")
    SLUG_ERROR = (By.ID, ":r2t:-helper-text")

    def fill(self, status: dict):
        if status.get("name") is not None:
            self.type(self.NAME_INPUT, status["name"])
        if status.get("slug") is not None:
            self.type(self.SLUG_INPUT, status["slug"])
        return self

    def values(self) -> dict:
        def _val(locator):
            return self.wait.until(EC.presence_of_element_located(locator)).get_attribute("value")

        return {
            "name": _val(self.NAME_INPUT),
            "slug": _val(self.SLUG_INPUT),
        }

    def has_slug_error(self, timeout: float = 3.0) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(self.SLUG_ERROR))
            return True
        except Exception:
            try:
                el = self.driver.find_element(*self.SLUG_INPUT)
                return el.get_attribute("aria-invalid") == "true"
            except Exception:
                return False