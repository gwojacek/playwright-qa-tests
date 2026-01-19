from playwright.sync_api import Page, expect


class AddToCartModal:
    _MODAL = ".modal-content"
    _VIEW_CART_BTN = 'a[href="/view_cart"]'
    _CONTINUE_SHOPPING_BTN = (
        'button.btn.btn-success.close-modal.btn-block[data-dismiss="modal"]'
    )

    def __init__(self, page: Page):
        self.page = page

    def wait_until_visible(self, timeout=5000):
        """Wait for modal to be visible."""
        expect(self.page.locator(self._MODAL)).to_be_visible(timeout=timeout)

    def click_continue_shopping(self):
        """Click 'Continue Shopping' button on modal."""
        self.page.locator(self._MODAL).locator(self._CONTINUE_SHOPPING_BTN).click()

    def click_view_cart(self):
        """Click 'View Cart' link in modal."""
        self.page.locator(self._MODAL).locator(self._VIEW_CART_BTN).click()

    def wait_until_invisible(self, timeout=5000):
        """Wait for modal to be invisible."""
        expect(self.page.locator(self._MODAL)).to_be_hidden(timeout=timeout)
