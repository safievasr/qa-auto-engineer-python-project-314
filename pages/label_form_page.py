from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from core.form_page import BaseFormPage


class LabelFormPage(BaseFormPage):
    NAME_INPUT = (By.CSS_SELECTOR, 'input[name="name"]')

    NAME_ERROR = (By.CSS_SELECTOR, '[id$="-helper-text"]')

    def fill(self, label: dict):
        if label.get("name") is not None:
            self.type(self.NAME_INPUT, label["name"])
        return self

    def values(self) -> dict:
        el = self.wait.until(EC.presence_of_element_located(self.NAME_INPUT))
        return {"name": el.get_attribute("value")}