from playwright.sync_api import Page, TimeoutError


class ConsentPopup:
    _CONSENT_BTN = 'button[class*="fc-primary-button"][aria-label="Consent"]'

    def __init__(self, page: Page):
        self.page = page

    def accept(self, timeout=5000):
        """Click consent if present; ignore if not found."""
        try:
            self.page.locator(self._CONSENT_BTN).click(timeout=timeout)
        except TimeoutError:
            pass
