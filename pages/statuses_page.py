from core.list_page import ListPage


class StatusesPage(ListPage):
    ENTITY_PATH = "/task_statuses"
    ENTITY_LABEL = "Task statuses"
    EMPTY_STATE_TEXT = "No Task statuses yet."
