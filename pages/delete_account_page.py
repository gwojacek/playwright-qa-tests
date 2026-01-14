import os

from playwright.sync_api import Page, expect

from pages.main_page import NavMenu


class DeleteAccountPage:
    _ACCOUNT_DELETED_HEADER = 'h2[data-qa="account-deleted"]'
    _CONTINUE_BTN = 'a[data-qa="continue-button"]'

    def __init__(self, page: Page):
        self.page = page

    def delete_account_and_continue(self, click=True):
        # Click 'Delete Account' in nav
        NavMenu(self.page).click_delete_account()
        # Wait for URL to be correct
        expect(self.page).to_have_url(f"{os.environ.get('ADDRESS')}/delete_account")
        # Assert the header is present and correct
        account_deleted_header = self.page.locator(self._ACCOUNT_DELETED_HEADER)
        expect(account_deleted_header).to_be_visible()
        expect(account_deleted_header).to_have_text("Account Deleted!")
        if click:
            self.page.locator(self._CONTINUE_BTN).click()
            # Wait for redirect to home
            expect(self.page).to_have_url(f"{os.environ.get('ADDRESS')}/")
