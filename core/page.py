from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def _loc(self, locator, extra=None):
        if extra is not None:
            locator = (locator, extra)
        if not (isinstance(locator, tuple) and len(locator) == 2):
            raise TypeError(
                f"locator must be (By, value), got: {locator!r}"
            )
        return locator

    def click(self, locator, extra=None):
        locator = self._loc(locator, extra)
        el = self.wait.until(EC.element_to_be_clickable(locator))
        try:
            el.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", el)

    def type(self, locator, text, extra=None):
        if extra is not None:
            locator = (locator, text)
            text = extra
        locator = self._loc(locator)
        el = self.wait.until(EC.visibility_of_element_located(locator))
        el.send_keys(Keys.CONTROL, "a")
        el.send_keys(Keys.BACKSPACE)
        el.send_keys(text)

    def get_text(self, locator):
        return self.wait.until(
            EC.visibility_of_element_located(self._loc(locator))
        ).text

    def is_visible(self, locator, timeout=5) -> bool:
        locator = self._loc(locator)
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def find_all(self, locator):
        return self.driver.find_elements(*self._loc(locator))

    def click_checkbox(self, scope_locator):
        scope = self.wait.until(EC.presence_of_element_located(scope_locator))
        try:
            scope.find_element(By.CSS_SELECTOR, ".MuiCheckbox-root").click()
            return
        except Exception:
            pass
        try:
            inp = scope.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
            self.driver.execute_script("arguments[0].click();", inp)
            return
        except Exception:
            pass
        scope.click()

    def confirm_dialog(self, timeout: float = 3.0):
        dialog_sel = (By.CSS_SELECTOR,"[role='dialog'], .MuiDialog-container, .MuiModal-root")
        try:
            dialog = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(dialog_sel))
        except TimeoutException:
            return

        clicked = False
        for loc in (By.XPATH, ".//button[contains(., 'Delete')"):
            try:
                btn = dialog.find_element(*loc)
                try:
                    btn.click()
                except ElementClickInterceptedException:
                    self.driver.execute_script("arguments[0].click();", btn)
                clicked = True
                break
            except Exception:
                continue

        if not clicked:
            return 

        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(dialog_sel)
            )
        except TimeoutException:
            pass