from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
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

        def _options_visible(d):
            return d.find_elements(By.CSS_SELECTOR,
                "li[role='option'], div[role='option'], li.MuiMenuItem-root"
            )

        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: len(_options_visible(d)) > 0
            )
        except TimeoutException:
            opts = _options_visible(self.driver)
            raise AssertionError(
                f"Меню {field!r} не открылось после клика. "
                f"Найдено опций: {len(opts)}. "
                f"HTML обёртки: {wrapper.get_attribute('outerHTML')[:400]}"
            )

        options = _options_visible(self.driver)
        chosen = None
        for opt in options:
            try:
                if opt.is_displayed() and value in (opt.text or ""):
                    chosen = opt
                    break
            except Exception:
                continue

        if chosen is None:
            visible_texts = [
                (o.text or "").strip()
                for o in options if o.is_displayed()
            ]
            raise AssertionError(
                f"Опция {value!r} не найдена в {field!r}. "
                f"Доступные: {visible_texts}"
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