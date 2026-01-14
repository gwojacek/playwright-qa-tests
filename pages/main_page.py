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
    _NAV_MENU = '[class*="shop-menu"]'
    _HOME_BTN = 'a[href="/"]'
    _PRODUCTS_BTN = 'a[href="/products"]'
    _CART_BTN = 'a[href="/view_cart"]'
    _LOGIN_BTN = 'a[href="/login"]'
    _LOGOUT_BTN = 'a[href="/logout"]'
    _CONTACT_BTN = 'a[href="/contact_us"]'
    _TEST_CASES_BTN = 'a[href="/test_cases"]'
    _API_TESTING_BTN = 'a[href="/api_list"]'
    _VIDEO_TUTORIALS_BTN = 'a[href="/video_tutorials"]'
    _DOWNLOAD_APP_BTN = 'a[href="/download_app"]'
    _DELETE_ACCOUNT_BTN = 'a[href="/delete_account"]'

    def __init__(self, page: Page):
        self.page = page

    def click_home(self):
        self.page.locator(self._NAV_MENU).locator(self._HOME_BTN).click()

    def click_products(self):
        self.page.locator(self._NAV_MENU).locator(self._PRODUCTS_BTN).click()

    def click_cart(self):
        self.page.locator(self._NAV_MENU).locator(self._CART_BTN).click()

    def click_login(self):
        self.page.locator(self._NAV_MENU).locator(self._LOGIN_BTN).click()

    def click_logout(self):
        self.page.locator(self._NAV_MENU).locator(self._LOGOUT_BTN).click()

    def click_contact(self):
        self.page.locator(self._NAV_MENU).locator(self._CONTACT_BTN).click()

    def click_test_cases(self):
        self.page.locator(self._NAV_MENU).locator(self._TEST_CASES_BTN).click()

    def click_api_testing(self):
        self.page.locator(self._NAV_MENU).locator(self._API_TESTING_BTN).click()

    def click_video_tutorials(self):
        self.page.locator(self._NAV_MENU).locator(self._VIDEO_TUTORIALS_BTN).click()

    def click_download_app(self):
        self.page.locator(self._NAV_MENU).locator(self._DOWNLOAD_APP_BTN).click()

    def click_delete_account(self):
        self.page.locator(self._NAV_MENU).locator(self._DELETE_ACCOUNT_BTN).click()

    def is_logged_in(self):
        expect(self.page.locator(self._LOGOUT_BTN)).to_be_visible(timeout=5000)
        expect(self.page.locator(self._DELETE_ACCOUNT_BTN)).to_be_visible(
            timeout=5000
        )

    def is_logged_out(self):
        expect(self.page.locator(self._LOGOUT_BTN)).not_to_be_visible()
        expect(self.page.locator(self._DELETE_ACCOUNT_BTN)).not_to_be_visible()


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
