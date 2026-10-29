from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from core.page import BasePage


class BaseFormPage(BasePage):
    FORM = (By.CSS_SELECTOR, "form, [role='form']")
    SAVE_BTN = (By.CSS_SELECTOR, 'form button[type="submit"]')
    SNACKBAR = (By.CSS_SELECTOR,".RaNotification-root, .MuiSnackbar-root, [role='alert']")
    FIELD_ERROR = (By.CSS_SELECTOR,".Mui-error, .MuiFormHelperText-root.Mui-error, [aria-invalid='true']")

    def wait_opened(self, timeout: float = 15.0):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.FORM)
            )
        except TimeoutException:
            raise AssertionError(
                f"Форма не открылась за {timeout}s. "
                f"URL: {self.driver.current_url}"
            )
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.SAVE_BTN)
            )
        except TimeoutException:
            raise AssertionError(
                f"Форма открыта, но кнопка Save не появилась. "
                f"URL: {self.driver.current_url}. "
                f"Проверь, что форма не в состоянии загрузки "
                f"и что поле обязательное заполнено."
            )
        return self

    def save(self, expect_redirect: bool = True):
        self.click(self.SAVE_BTN)
        if expect_redirect:
            WebDriverWait(self.driver, 10).until(
                EC.any_of(
                    EC.invisibility_of_element_located(self.FORM),
                    EC.visibility_of_element_located(self.SNACKBAR),
                    EC.visibility_of_element_located(self.FIELD_ERROR),
                )
            )
        return self

    def is_save_enabled(self) -> bool:
        return self.wait.until(
            EC.presence_of_element_located(self.SAVE_BTN)
        ).is_enabled()