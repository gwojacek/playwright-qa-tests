from typing import List

from playwright.sync_api import Page, expect, Locator

from components.add_to_cart_modal import AddToCartModal


class MainPage:
    URL = "https://en.wikipedia.org/wiki/Main_Page"
    _SEARCH_INPUT = '[name="search"]'

    def __init__(self, page: Page):
        self.page = page
        self.search_input = self.page.locator(self._SEARCH_INPUT)

    def load(self) -> None:
        self.page.goto(self.URL)

    @property
    def title(self) -> str:
        return self.page.title()

    def search_input_exists(self) -> bool:
        return self.search_input.is_visible()


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
        self.nav_menu = self.page.locator(self._NAV_MENU)
        self.home_btn = self.nav_menu.locator(self._HOME_BTN)
        self.products_btn = self.nav_menu.locator(self._PRODUCTS_BTN)
        self.cart_btn = self.nav_menu.locator(self._CART_BTN)
        self.login_btn = self.nav_menu.locator(self._LOGIN_BTN)
        self.logout_btn = self.nav_menu.locator(self._LOGOUT_BTN)
        self.contact_btn = self.nav_menu.locator(self._CONTACT_BTN)
        self.test_cases_btn = self.nav_menu.locator(self._TEST_CASES_BTN)
        self.api_testing_btn = self.nav_menu.locator(self._API_TESTING_BTN)
        self.video_tutorials_btn = self.nav_menu.locator(
            self._VIDEO_TUTORIALS_BTN
        )
        self.download_app_btn = self.nav_menu.locator(self._DOWNLOAD_APP_BTN)
        self.delete_account_btn = self.nav_menu.locator(
            self._DELETE_ACCOUNT_BTN
        )


class FeaturesItems:
    _COMPONENT = ".features_items"
    _PRODUCT_CARDS = ".product-image-wrapper"
    _VIEW_PRODUCT_BTN = ".choose a[href*='product_details']"
    _ADD_TO_CART_BTN = ".overlay-content .add-to-cart"
    _PRODUCT_NAME = "p"
    _PRODUCT_PRICE = "h2"
    _PRODUCT_OVERLAY = ".overlay-content"

    def __init__(self, page: Page):
        self.page = page
        self.component = self.page.locator(self._COMPONENT)
        self.product_cards = self.component.locator(self._PRODUCT_CARDS)
        self.view_product_btn = self.product_cards.locator(
            self._VIEW_PRODUCT_BTN
        )
        self.add_to_cart_btn = self.product_cards.locator(
            self._ADD_TO_CART_BTN
        )
        self.product_name = self.product_cards.locator(self._PRODUCT_NAME)
        self.product_price = self.product_cards.locator(self._PRODUCT_PRICE)
        self.product_overlay = self.product_cards.locator(self._PRODUCT_OVERLAY)

    def cards(self) -> List[Locator]:
        """Return all product cards as a list of locators."""
        return self.product_cards.all()

    def card(self, index: int = 0) -> Locator:
        """Return a specific product card by index."""
        return self.product_cards.nth(index)

    def view_product(self, index: int = 0) -> None:
        self.view_product_btn.nth(index).click()

    def add_to_cart_by_hover(self, index: int, close_modal: bool = True) -> None:
        self.card(index).hover()
        expect(self.product_overlay.nth(index)).to_be_visible()
        self.add_to_cart_btn.nth(index).click()
        modal = AddToCartModal(self.page)
        modal.wait_until_visible()
        if close_modal:
            modal.click_continue_shopping()
            modal.wait_until_invisible()
            self.page.wait_for_load_state("networkidle")

    def add_to_cart_and_view_cart(self, index: int = 0) -> None:
        self.card(index).hover()
        expect(self.product_overlay.nth(index)).to_be_visible()
        self.add_to_cart_btn.nth(index).click()
        modal = AddToCartModal(self.page)
        modal.wait_until_visible()
        modal.click_view_cart()

    def get_product_name(self, index: int = 0) -> str:
        return self.product_name.nth(index).inner_text().strip()

    def get_product_detail_url(self, index: int = 0) -> str:
        return self.view_product_btn.nth(index).get_attribute("href")

    def get_product_price(self, index: int = 0) -> int:
        """
        Returns product price as int, stripping 'Rs. ' and commas.
        Example: "Rs. 1,000" -> 1000
        """
        price_text = self.product_price.nth(index).inner_text()
        return self._parse_price(price_text)

    @staticmethod
    def _parse_price(text: str) -> int:
        """Parse price text like 'Rs. 1,234' into integer 1234."""
        return int(text.replace("Rs. ", "").replace(",", "").strip())
