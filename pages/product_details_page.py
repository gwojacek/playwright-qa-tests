from playwright.sync_api import Page

from components.add_to_cart_modal import AddToCartModal


class ProductDetailsPage:
    _COMPONENT = ".product-information"
    _NAME = "h2"
    _PRICE = "span span"
    _QUANTITY_INPUT = "input#quantity"
    _ADD_TO_CART_BTN = "button.cart"
    _INFO_FIELD_P_TAG = "p"

    def __init__(self, page: Page):
        self.page = page
        self.component = self.page.locator(self._COMPONENT)
        self.name_locator = self.component.locator(self._NAME)
        self.price_locator = self.component.locator(self._PRICE)
        self.quantity_input = self.component.locator(self._QUANTITY_INPUT)
        self.add_to_cart_btn = self.component.locator(self._ADD_TO_CART_BTN)

    @property
    def name(self) -> str:
        return self.name_locator.inner_text().strip()

    @property
    def price(self) -> int:
        price_text = self.price_locator.inner_text().strip()
        return self._parse_price(price_text)

    @property
    def category(self) -> str:
        return self._get_info_field("Category")

    @property
    def availability(self) -> str:
        return self._get_info_field("Availability")

    @property
    def condition(self) -> str:
        return self._get_info_field("Condition")

    @property
    def brand(self) -> str:
        return self._get_info_field("Brand")

    def _get_info_field(self, label: str) -> str:
        """Return info value from <p> like 'Availability', 'Condition', 'Brand', 'Category'."""
        p_tags = self.component.locator(self._INFO_FIELD_P_TAG).all()
        for p in p_tags:
            if label in p.inner_text():
                return p.inner_text().split(":", 1)[-1].strip()
        return ""

    def set_quantity(self, qty: int) -> int:
        self.quantity_input.fill(str(qty))
        return self.quantity

    def fill_input_with_characters(self, qty: str) -> str:
        self.quantity_input.clear()
        self.quantity_input.press_sequentially(qty)
        return self.quantity_input.input_value()

    @property
    def quantity(self) -> int:
        return int(self.quantity_input.input_value())

    def add_to_cart(self, close_modal: bool = True) -> None:
        self.add_to_cart_btn.click()
        modal = AddToCartModal(self.page)
        modal.wait_until_visible()
        if close_modal:
            modal.click_continue_shopping()

    def add_to_cart_and_view_cart(self) -> None:
        self.add_to_cart_btn.click()
        modal = AddToCartModal(self.page)
        modal.wait_until_visible()
        modal.click_view_cart()

    @staticmethod
    def _parse_price(text: str) -> int:
        """Parse price text like 'Rs. 1,234' into integer 1234."""
        return int(text.replace("Rs.", "").replace(",", "").strip())
