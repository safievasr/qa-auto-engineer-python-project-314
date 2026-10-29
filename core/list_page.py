from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from core.page import BasePage


class ListPage(BasePage):
    ENTITY_PATH = ""
    ENTITY_LABEL = ""
    EMPTY_STATE_TEXT = "No Labels yet."

    TABLE = (By.CSS_SELECTOR, "table")
    ROWS = (By.CSS_SELECTOR, "table tbody tr")
    SELECT_ALL_CELL = (By.CSS_SELECTOR, "table thead tr th:first-child")

    BULK_TOOLBAR = (By.CSS_SELECTOR, "[class*='RaBulkActionsToolbar']")
    BULK_DELETE_BTN = (By.CSS_SELECTOR, "[aria-label='Delete']")

    @property
    def CREATE_LINK(self):
        return (By.CSS_SELECTOR, f'a[href*="{self.ENTITY_PATH}/create"]')

    @property
    def EDIT_LINK_SELECTORS(self):
        p = self.ENTITY_PATH
        return (
            f'a[href*="{p}/"]:not([href$="/create"])',
            f'a[href*="#{p}/"]:not([href$="/create"])',
        )

    @property
    def EMPTY_STATE(self):
        return (By.XPATH, f"//*[contains(text(), '{self.EMPTY_STATE_TEXT}')]")

    def __init__(self, driver, base_url: str | None = None):
        super().__init__(driver)
        self._base_url = base_url.rstrip("/") if base_url else None

    def open(self, base_url: str | None = None):
        if base_url:
            self._base_url = base_url.rstrip("/")
        if self._base_url is None:
            raise ValueError("base_url must be provided before opening the list")
        self.driver.get(self._base_url + "/#" + self.ENTITY_PATH)
        self.wait.until(EC.visibility_of_element_located(self.TABLE))
        return self

    def click_create(self):
        self.click(self.CREATE_LINK)

    def header_text(self) -> str:
        return " ".join(
            header.text.lower()
            for header in self.driver.find_elements(
                By.CSS_SELECTOR, "table thead th"
            )
        )

    def rows(self):
        return self.find_all(self.ROWS)

    def _visible_rows(self):
        """Только те <tr>, которые реально видны пользователю."""
        return [r for r in self.rows() if r.is_displayed()]

    def _visible_cell_texts(self, row):
        """Список видимых текстов всех <td> в строке."""
        result = []
        for cell in row.find_elements(By.TAG_NAME, "td"):
            if cell.is_displayed():
                result.append((cell.text or "").strip())
        return result

    def _find_row(self, text: str, exact: bool):
        for row in self._visible_rows():
            for cell_text in self._visible_cell_texts(row):
                if exact and cell_text == text:
                    return row
                if not exact and text in cell_text:
                    return row
        return None

    def row_by_text(self, text: str, timeout: float = 10.0, exact: bool = True):
        return WebDriverWait(self.driver, timeout).until(
            lambda d: self._find_row(text, exact=exact) or False,
            message=f"Не нашлась строка с текстом {text!r}",
        )

    def is_present(self, text: str, timeout: float = 1.0, exact: bool = True) -> bool:
        try:
            self.row_by_text(text, timeout=timeout, exact=exact)
            return True
        except TimeoutException:
            return False

    def is_empty(self, timeout: float = 5.0) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.EMPTY_STATE)
            )
            return True
        except TimeoutException:
            return len(self._visible_rows()) == 0

    def wait_for_absence(
        self, text: str, timeout: float = 10.0, exact: bool = True
    ) -> None:
        WebDriverWait(self.driver, timeout).until(
            lambda d: self._find_row(text, exact=exact) is None,
            message=f"Строка с текстом {text!r} не исчезла",
        )

    def open_edit_for(self, text: str):
        row = self.row_by_text(text, exact=True)

        clicked = False
        for sel in self.EDIT_LINK_SELECTORS:
            links = row.find_elements(By.CSS_SELECTOR, sel)
            if links:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});", links[0]
                )
                links[0].click()
                clicked = True
                break

        if not clicked:
            cells = row.find_elements(By.TAG_NAME, "td")
            target = next(
                (c for c in cells if (c.text or "").strip() == text),
                cells[1] if len(cells) > 1 else row,
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", target
            )
            try:
                target.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", target)

        WebDriverWait(self.driver, 10).until(
            lambda d: (f"{self.ENTITY_PATH}/" in d.current_url
                       or f"#{self.ENTITY_PATH}/" in d.current_url)
                      and "/create" not in d.current_url,
            message=f"Не открылась форма редактирования для {text}. "
                    f"URL: {self.driver.current_url}",
        )

    def select_row(self, text: str):
        row = self.row_by_text(text, exact=True)
        try:
            row.find_element(By.CSS_SELECTOR, ".MuiCheckbox-root").click()
        except Exception:
            try:
                inp = row.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
                self.driver.execute_script("arguments[0].click();", inp)
            except Exception:
                row.find_element(By.CSS_SELECTOR, "input[type='checkbox']").click()

    def select_all_rows(self):
        self.wait.until(EC.presence_of_element_located(self.SELECT_ALL_CELL))
        self.click_checkbox(self.SELECT_ALL_CELL)

    def bulk_delete_selected(self):
        self.wait.until(EC.visibility_of_element_located(self.BULK_TOOLBAR))
        self.click(self.BULK_DELETE_BTN)
        self.confirm_dialog()

    def delete_row(self, text: str):
        self.select_row(text)
        self.bulk_delete_selected()

    def delete_all(self):
        self.select_all_rows()
        self.bulk_delete_selected()