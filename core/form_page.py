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
        try:
            btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.SAVE_BTN)
            )
        except TimeoutException:
            # диагностика: почему Save не кликабельна
            form_html = ""
            try:
                form = self.driver.find_element(By.TAG_NAME, "form")
                form_html = form.get_attribute("outerHTML")[:2000]
            except Exception:
                pass
            raise AssertionError(
                f"Кнопка Save не кликабельна за 10s. "
                f"URL: {self.driver.current_url}. "
                f"Проверь, что все обязательные поля заполнены и валидны. "
                f"HTML формы: {form_html}"
            )

        btn.click()
        if expect_redirect:
            try:
                WebDriverWait(self.driver, 10).until(
                    lambda d: (
                        not self.is_visible(self.FORM, timeout=0.3)
                        or self.is_visible(self.SNACKBAR, timeout=0.3)
                        or self.is_visible(self.FIELD_ERROR, timeout=0.3)
                    )
                )
            except TimeoutException:
                pass
        return self

    def is_save_enabled(self) -> bool:
        return self.wait.until(
            EC.presence_of_element_located(self.SAVE_BTN)
        ).is_enabled()