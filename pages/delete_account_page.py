import os

from playwright.sync_api import Page, expect, Locator

from pages.main_page import NavMenu


class DeleteAccountPage:
    # Class-level constants for selectors
    _ACCOUNT_DELETED_HEADER = 'h2[data-qa="account-deleted"]'
    _CONTINUE_BTN = 'a[data-qa="continue-button"]'

    def __init__(self, page: Page):
        self.page = page

    @property
    def account_deleted_header(self) -> Locator:
        """The 'Account Deleted!' header locator."""
        return self.page.locator(self._ACCOUNT_DELETED_HEADER)

    @property
    def continue_btn(self) -> Locator:
        """The 'Continue' button locator."""
        return self.page.locator(self._CONTINUE_BTN)

    def delete_account_and_continue(self, click_continue: bool = True) -> None:
        """
        Deletes the account, verifies the deletion page, and optionally clicks
        the continue button.
        """
        # Click 'Delete Account' in nav
        NavMenu(self.page).delete_account_btn.click()

        # Wait for the URL to be correct
        expect(self.page).to_have_url(f"{os.environ.get('ADDRESS')}/delete_account")

        # Assert the header is present and has the correct text
        expect(self.account_deleted_header).to_be_visible()
        expect(self.account_deleted_header).to_have_text("Account Deleted!")

        if click_continue:
            self.continue_btn.click()
            # Wait for redirect to the home page
            expect(self.page).to_have_url(f"{os.environ.get('ADDRESS')}/")
