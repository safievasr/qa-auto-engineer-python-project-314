from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from core.page import BasePage
from pages.task_form_page import TaskFormPage


class BoardPage(BasePage):
    BOARD_PATH = "/#/tasks"
    COLUMN_HEADINGS = (By.CSS_SELECTOR, "h6.MuiTypography-subtitle1")
    DROP_ZONES = (By.CSS_SELECTOR, "[data-rfd-droppable-id]")
    CARD_WRAPPERS = (By.CSS_SELECTOR, "[data-rfd-draggable-id]")
    CARD_TITLE = (By.CSS_SELECTOR, ".MuiTypography-h5")
    CARD_EDIT = (By.CSS_SELECTOR, 'a[aria-label="Edit"]')
    CREATE_BUTTON = (By.CSS_SELECTOR, 'a[aria-label="Create"][href*="/tasks/create"]')
    PROFILE_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="Profile"]')
    LOGOUT_ITEM = (By.CSS_SELECTOR, '[role="menuitem"].logout')
    FILTER_FIELDS = ("assignee_id", "status_id", "label_id")
    FILTER_OPTIONS = (
        "li[role='option'], div[role='option'], li.MuiMenuItem-root"
    )

    def __init__(self, driver, base_url: str):
        super().__init__(driver)
        self._base_url = base_url.rstrip("/")

    def open(self) -> "BoardPage":
        self.driver.get(self._base_url + self.BOARD_PATH)
        self.wait.until(EC.presence_of_element_located(self.DROP_ZONES))
        return self

    def is_opened(self) -> bool:
        return self.is_visible(self.DROP_ZONES)

    def logout(self) -> None:
        self.click(self.PROFILE_BUTTON)
        self.click(self.LOGOUT_ITEM)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'input[name="username"]')
            )
        )

    def clear_filters(self) -> "BoardPage":
        for field in self.FILTER_FIELDS:
            input_locator = (
                By.CSS_SELECTOR,
                f'[data-source="{field}"] input[name="{field}"]',
            )
            if not self.driver.find_element(*input_locator).get_attribute("value"):
                continue

            self.driver.find_element(
                By.CSS_SELECTOR,
                f'[data-source="{field}"] [role="combobox"]',
            ).click()
            empty_option = WebDriverWait(self.driver, 5).until(
                lambda d: next(
                    (
                        option
                        for option in d.find_elements(
                            By.CSS_SELECTOR, self.FILTER_OPTIONS
                        )
                        if option.is_displayed() and not option.text.strip()
                    ),
                    None,
                ),
                message=f"Пустая опция фильтра {field!r} не найдена",
            )
            empty_option.click()
            WebDriverWait(self.driver, 10).until(
                lambda d: not d.find_element(*input_locator).get_attribute("value"),
                message=f"Фильтр {field!r} не очистился",
            )

        return self

    def column_titles(self) -> list[str]:
        result = []
        for h in self.driver.find_elements(*self.COLUMN_HEADINGS):
            if h.is_displayed():
                t = h.text.strip()
                if t:
                    result.append(t)
        return result

    def drop_zone_by_title(self, title: str):
        return WebDriverWait(self.driver, 10).until(
            lambda d: d.find_element(
                By.XPATH,
                f"//h6[normalize-space(.)='{title}']"
                f"/following-sibling::*[@data-rfd-droppable-id][1]",
            ),
            message=f"Не нашлась колонка {title!r}",
        )

    def _card_title_of(self, wrapper) -> str:
        try:
            return wrapper.find_element(*self.CARD_TITLE).text.strip()
        except Exception:
            return ""

    def card_titles_in_column(self, column_title: str) -> list[str]:
        zone = self.drop_zone_by_title(column_title)
        result = []
        for w in zone.find_elements(*self.CARD_WRAPPERS):
            t = self._card_title_of(w)
            if t:
                result.append(t)
        return result

    def card_by_title(self, title: str):
        return WebDriverWait(self.driver, 10).until(
            lambda d: next(
                (w for w in d.find_elements(*self.CARD_WRAPPERS)
                 if self._card_title_of(w) == title and w.is_displayed()),
                None,
            ),
            message=f"Карточка {title!r} не найдена на доске",
        )

    def wait_for_card_absence(self, title: str, timeout: float = 10.0) -> None:
        WebDriverWait(self.driver, timeout).until(
            lambda d: not any(
                self._card_title_of(card) == title and card.is_displayed()
                for card in d.find_elements(*self.CARD_WRAPPERS)
            ),
            message=f"Карточка {title!r} не исчезла с доски",
        )

    def is_task_in_column(
        self, title: str, column_title: str, timeout: float = 5.0
    ) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: title in self.card_titles_in_column(column_title)
            )
            return True
        except TimeoutException:
            return False

    def column_of_card(self, title: str) -> str | None:
        for t in self.column_titles():
            if title in self.card_titles_in_column(t):
                return t
        return None

    def open_create_form(self):
        self.click(self.CREATE_BUTTON)

    def open_edit_for(self, title: str):
        card = self.card_by_title(title)
        edit_link = card.find_element(*self.CARD_EDIT)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", edit_link
        )
        edit_link.click()
        WebDriverWait(self.driver, 10).until(
            lambda d: "/tasks/" in d.current_url and "/create" not in d.current_url
        )

    def move_via_edit(self, title: str, new_status_text: str):
        self.open_edit_for(title)
        form = TaskFormPage(self.driver).wait_opened()
        form.set_reference("status_id", new_status_text)
        form.save()
        self.open()

    def move_by_drag(self, title: str, target_column: str):
        """Реальный drag&drop через ActionChains (react-beautiful-dnd)."""
        card = self.card_by_title(title)
        zone = self.drop_zone_by_title(target_column)

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", card
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", zone
        )

        ActionChains(self.driver) \
            .move_to_element(card) \
            .click_and_hold() \
            .pause(0.5) \
            .move_by_offset(0, 5) \
            .pause(0.3) \
            .move_to_element(zone) \
            .pause(0.5) \
            .release() \
            .perform()