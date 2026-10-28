from core.list_page import ListPage


class LabelsPage(ListPage):
    ENTITY_PATH = "/labels"
    ENTITY_LABEL = "Labels"

    def __init__(self, driver, base_url: str):
        super().__init__(driver, base_url)