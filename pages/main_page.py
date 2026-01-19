from typing import List
from playwright.sync_api import Page, expect, Locator

from components.add_to_cart_modal import AddToCartModal


class MainPage:
    URL = "https://en.wikipedia.org/wiki/Main_Page"

    def __init__(self, page: Page):
        self.page = page

    def load(self):
        self.page.goto(self.URL)

    def get_title(self):
        return self.page.title()

    def search_input_exists(self):
        return self.page.locator('[name="search"]').is_visible()


class NavMenu:
    HOME_BTN = '[class*="shop-menu"] a[href="/"]'
    PRODUCTS_BTN = '[class*="shop-menu"] a[href="/products"]'
    CART_BTN = '[class*="shop-menu"] a[href="/view_cart"]'
    LOGIN_BTN = '[class*="shop-menu"] a[href="/login"]'
    LOGOUT_BTN = '[class*="shop-menu"] a[href="/logout"]'
    CONTACT_BTN = '[class*="shop-menu"] a[href="/contact_us"]'
    TEST_CASES_BTN = '[class*="shop-menu"] a[href="/test_cases"]'
    API_TESTING_BTN = '[class*="shop-menu"] a[href="/api_list"]'
    VIDEO_TUTORIALS_BTN = '[class*="shop-menu"] a[href="/video_tutorials"]'
    DOWNLOAD_APP_BTN = '[class*="shop-menu"] a[href="/download_app"]'
    DELETE_ACCOUNT_BTN = '[class*="shop-menu"] a[href="/delete_account"]'

    def __init__(self, page: Page):
        self.page = page

    def click_nav_btn(self, btn_selector: str):
        """
        Click any navigation menu button.
        Usage: nav.click_nav_btn(NavMenu.LOGIN_BTN)
        """
        self.page.locator(btn_selector).click()

    def is_logged_in(self):
        expect(self.page.locator(self.LOGOUT_BTN)).to_be_visible(timeout=5000)
        expect(self.page.locator(self.DELETE_ACCOUNT_BTN)).to_be_visible(
            timeout=5000
        )

    def is_logged_out(self):
        expect(self.page.locator(self.LOGOUT_BTN)).not_to_be_visible()
        expect(self.page.locator(self.DELETE_ACCOUNT_BTN)).not_to_be_visible()


class FeaturesItems:
    _COMPONENT = ".features_items"
    _PRODUCT_CARDS = ".product-image-wrapper"
    _VIEW_PRODUCT_BTN = ".choose a[href*='product_details']"
    _ADD_TO_CART_BTN = ".overlay-content .add-to-cart"
    _PRODUCT_NAME = ".productinfo p"
    _PRODUCT_PRICE = ".productinfo h2"
    _PRODUCT_OVERLAY = ".overlay-content"

    def __init__(self, page: Page):
        self.page = page

    def cards(self) -> List[Locator]:
        """Return all product cards as a list of locators."""
        return self.page.locator(self._COMPONENT).locator(self._PRODUCT_CARDS).all()

    def card(self, index=0) -> Locator:
        """Return a specific product card by index."""
        return self.page.locator(self._COMPONENT).locator(self._PRODUCT_CARDS).nth(index)

    def view_product(self, index=0):
        self.card(index).locator(self._VIEW_PRODUCT_BTN).click()

    def add_to_cart_by_hover(self, index, close_modal=True):
        card = self.card(index)
        card.hover()
        expect(card.locator(self._PRODUCT_OVERLAY)).to_be_visible()
        card.locator(self._ADD_TO_CART_BTN).click()

        modal = AddToCartModal(self.page)
        modal.wait_until_visible()
        if close_modal:
            modal.click_continue_shopping()
            modal.wait_until_invisible()

    def add_to_cart_and_view_cart(self, index=0):
        card = self.card(index)
        card.hover()
        expect(card.locator(self._PRODUCT_OVERLAY)).to_be_visible()
        card.locator(self._ADD_TO_CART_BTN).click()

        modal = AddToCartModal(self.page)
        modal.wait_until_visible()
        modal.click_view_cart()

    def get_product_name(self, index=0) -> str:
        return self.card(index).locator(self._PRODUCT_NAME).inner_text().strip()

    def get_product_detail_url(self, index=0) -> str:
        return self.card(index).locator(self._VIEW_PRODUCT_BTN).get_attribute("href")

    def get_product_price(self, index=0) -> int:
        price_text = self.card(index).locator(self._PRODUCT_PRICE).inner_text()
        return self._parse_price(price_text)

    @staticmethod
    def _parse_price(text: str) -> int:
        return int(text.replace("Rs. ", "").replace(",", "").strip())
