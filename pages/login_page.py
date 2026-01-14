import os

from playwright.sync_api import Page, expect, Locator

from components.consent_popup import ConsentPopup
from pages.main_page import NavMenu


class LoginPage:
    URL = f"{os.environ.get('ADDRESS')}/login"

    # Selectors for login form (left)
    _EMAIL_INPUT = 'input[data-qa="login-email"]'
    _PASSWORD_INPUT = 'input[data-qa="login-password"]'
    _LOGIN_BUTTON = 'button[data-qa="login-button"]'
    _LOGIN_FORM = 'form[action="/login"]'

    # Selectors for signup form (right)
    _SIGNUP_NAME_INPUT = 'input[data-qa="signup-name"]'
    _SIGNUP_EMAIL_INPUT = 'input[data-qa="signup-email"]'
    _SIGNUP_BUTTON = 'button[data-qa="signup-button"]'
    _SIGNUP_FORM = 'form[action="/signup"]'

    def __init__(self, page: Page):
        self.page = page

    # --- Locators for login form ---
    @property
    def email_input(self) -> Locator:
        return self.page.locator(self._EMAIL_INPUT)

    @property
    def password_input(self) -> Locator:
        return self.page.locator(self._PASSWORD_INPUT)

    @property
    def login_button(self) -> Locator:
        return self.page.locator(self._LOGIN_BUTTON)

    @property
    def login_form(self) -> Locator:
        return self.page.locator(self._LOGIN_FORM)

    # --- Locators for signup form ---
    @property
    def signup_name_input(self) -> Locator:
        return self.page.locator(self._SIGNUP_NAME_INPUT)

    @property
    def signup_email_input(self) -> Locator:
        return self.page.locator(self._SIGNUP_EMAIL_INPUT)

    @property
    def signup_button(self) -> Locator:
        return self.page.locator(self._SIGNUP_BUTTON)

    @property
    def signup_form(self) -> Locator:
        return self.page.locator(self._SIGNUP_FORM)

    def load(self) -> None:
        """Navigate to the login page and handle consent popup."""
        self.page.goto(self.URL)
        ConsentPopup(self.page).accept()  # Handles the popup if present
        expect(self.email_input).to_be_visible()

    def login(self, email: str, password: str) -> None:
        """Fill login form and submit."""
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()
        self.is_logged_in()

    def signup(self, name: str, email: str) -> None:
        """Fill signup form and submit."""
        self.signup_name_input.fill(name)
        self.signup_email_input.fill(email)
        self.signup_button.click()

    def is_logged_in(self) -> None:
        """Verify that the user is logged in."""
        nav_menu = NavMenu(self.page)
        expect(nav_menu.logout_btn).to_be_visible(timeout=5000)
        expect(nav_menu.delete_account_btn).to_be_visible(timeout=5000)
        expect(self.page).to_have_url(f"{os.environ.get('ADDRESS')}/")

    def not_logged_in(self) -> bool:
        """Return True if neither Logout nor Delete Account button is displayed."""
        nav_menu = NavMenu(self.page)
        return not (
            nav_menu.logout_btn.is_visible() or nav_menu.delete_account_btn.is_visible()
        )

    def logout(self) -> None:
        """Log out the user and verify the URL."""
        NavMenu(self.page).logout_btn.click()
        expect(self.page).to_have_url(self.URL)
