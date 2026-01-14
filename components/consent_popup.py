from playwright.sync_api import Page, TimeoutError


class ConsentPopup:
    # Class-level constant for selector
    _CONSENT_BTN = 'button[class*="fc-primary-button"][aria-label="Consent"]'

    def __init__(self, page: Page):
        self.page = page
        self.consent_btn = self.page.locator(self._CONSENT_BTN)

    def accept(self, timeout: int = 5000) -> None:
        """Click consent if present; ignore if not found."""
        try:
            self.consent_btn.click(timeout=timeout)
        except TimeoutError:
            # The button is not always present, so we can ignore the timeout.
            pass
