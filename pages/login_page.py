import os

from playwright.sync_api import Page, expect

from components.consent_popup import ConsentPopup
from pages.main_page import NavMenu


class LoginPage:
    URL = f"{os.environ.get('ADDRESS')}/login"

    # Selectors for login form (left)
    _EMAIL_INPUT = 'input[data-qa="login-email"]'
    _PASSWORD_INPUT = 'input[data-qa="login-password"]'
    _LOGIN_BUTTON = 'button[data-qa="login-button"]'

    # Selectors for signup form (right)
    _SIGNUP_NAME_INPUT = 'input[data-qa="signup-name"]'
    _SIGNUP_EMAIL_INPUT = 'input[data-qa="signup-email"]'
    _SIGNUP_BUTTON = 'button[data-qa="signup-button"]'

    def __init__(self, page: Page):
        self.page = page

    def load(self):
        self.page.goto(self.URL)
        ConsentPopup(self.page).accept()  # Handles the popup if present
        expect(self.page.locator(self._EMAIL_INPUT)).to_be_visible()

    def login(self, email, password):
        """Fill login form and submit."""
        self.page.locator(self._EMAIL_INPUT).fill(email)
        self.page.locator(self._PASSWORD_INPUT).fill(password)
        self.page.locator(self._LOGIN_BUTTON).click()
        self.is_logged_in()

    def signup(self, name, email):
        """Fill signup form and submit."""
        self.page.locator(self._SIGNUP_NAME_INPUT).fill(name)
        self.page.locator(self._SIGNUP_EMAIL_INPUT).fill(email)
        self.page.locator(self._SIGNUP_BUTTON).click()

    def is_logged_in(self):
        NavMenu(self.page).is_logged_in()
        expect(self.page).to_have_url(f"{os.environ.get('ADDRESS')}/")

    def not_logged_in(self):
        NavMenu(self.page).is_logged_out()

    def logout(self):
        NavMenu(self.page).click_logout()
        expect(self.page).to_have_url(self.URL)
