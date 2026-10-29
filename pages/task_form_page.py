from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from core.form_page import BaseFormPage


class TaskFormPage(BaseFormPage):
    TITLE_INPUT = (By.CSS_SELECTOR, 'input[name="title"]')
    CONTENT_INPUT = (By.CSS_SELECTOR, 'textarea[name="content"]')
    SAVE_BTN = (By.CSS_SELECTOR, 'button[type="submit"][aria-label="Save"]')

    def fill(self, task: dict):
        if task.get("assignee"):
            self.set_reference("assignee_id", task["assignee"])
        if task.get("status"):
            self.set_reference("status_id", task["status"])
        if task.get("title"):
            self.type(self.TITLE_INPUT, task["title"])
        if task.get("content") and self.is_visible(self.CONTENT_INPUT, timeout=1):
            self.type(self.CONTENT_INPUT, task["content"])
        if task.get("labels"):
            for lbl in task["labels"]:
                self.set_reference("label_id", lbl)
        return self

    def set_reference(self, field: str, value: str):
        wrapper = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                f"//div[contains(concat(' ', normalize-space(@class), ' '), "
                f"' ra-input-{field} ')]",
            ))
        )

        clickable = wrapper.find_element(
            By.CSS_SELECTOR, ".MuiInputBase-root"
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", clickable
        )
        try:
            clickable.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", clickable)

        def _visible_option(d):
            options = d.find_elements(
                By.CSS_SELECTOR,
                "li[role='option'], div[role='option'], li.MuiMenuItem-root",
            )
            for option in options:
                try:
                    if option.is_displayed() and value in (option.text or ""):
                        return option
                except StaleElementReferenceException:
                    continue
            return False

        try:
            chosen = WebDriverWait(self.driver, 5).until(
                _visible_option,
                message=f"Опция {value!r} не найдена в видимом меню {field!r}",
            )
        except TimeoutException:
            opts = self.driver.find_elements(
                By.CSS_SELECTOR,
                "li[role='option'], div[role='option'], li.MuiMenuItem-root",
            )
            raise AssertionError(
                f"Видимая опция {value!r} не найдена в меню {field!r}. "
                f"Доступные: "
                f"{[(o.text or '').strip() for o in opts if o.is_displayed()]}. "
                f"HTML обёртки: {wrapper.get_attribute('outerHTML')[:400]}"
            )

        try:
            chosen.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", chosen)

        try:
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        except Exception:
            pass

    def delete_current(self):
        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(., 'Delete') or contains(., 'Удалить')]",
            ))
        )
        btn.click()
        self.confirm_dialog()