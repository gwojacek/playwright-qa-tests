from playwright.sync_api import Page, expect, Locator


class AddToCartModal:
    # Class-level constants for selectors
    _MODAL = ".modal-content"
    _VIEW_CART_BTN = 'a[href="/view_cart"]'
    _CONTINUE_SHOPPING_BTN = (
        'button.btn.btn-success.close-modal.btn-block[data-dismiss="modal"]'
    )

    def __init__(self, page: Page):
        self.page = page

    @property
    def modal(self) -> Locator:
        """The modal content locator."""
        return self.page.locator(self._MODAL)

    @property
    def view_cart_btn(self) -> Locator:
        """The 'View Cart' button locator."""
        return self.modal.locator(self._VIEW_CART_BTN)

    @property
    def continue_shopping_btn(self) -> Locator:
        """The 'Continue Shopping' button locator."""
        return self.modal.locator(self._CONTINUE_SHOPPING_BTN)

    def wait_until_visible(self, timeout: int = 5000) -> None:
        """Wait for modal to be visible."""
        expect(self.modal).to_be_visible(timeout=timeout)

    def click_continue_shopping(self) -> None:
        """Click 'Continue Shopping' button on modal."""
        self.continue_shopping_btn.click()

    def click_view_cart(self) -> None:
        """Click 'View Cart' link in modal."""
        self.view_cart_btn.click()

    def wait_until_invisible(self, timeout: int = 5000) -> None:
        """Wait for modal to be invisible."""
        expect(self.modal).to_be_hidden(timeout=timeout)
