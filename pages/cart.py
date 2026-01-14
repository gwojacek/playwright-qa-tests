from dataclasses import dataclass

from playwright.sync_api import Page, Locator


@dataclass
class ProductRow:
    row_locator: Locator

    # Class-level constants for selectors
    _NAME = ".cart_description h4 a"
    _CATEGORY = ".cart_description p"
    _PRICE = ".cart_price p"
    _QUANTITY = ".cart_quantity button"
    _TOTAL = ".cart_total_price"
    _DELETE_BTN = ".cart_quantity_delete"
    _INPUT = "input[type='number'], input"

    @property
    def name(self) -> str:
        """Get product name."""
        return self.row_locator.locator(self._NAME).inner_text().strip()

    @property
    def category(self) -> str:
        """Get product category."""
        return self.row_locator.locator(self._CATEGORY).inner_text().strip()

    @property
    def price(self) -> int:
        """Get product price in Rs."""
        txt = self.row_locator.locator(self._PRICE).inner_text()
        return self._parse_price(txt)

    @property
    def quantity(self) -> int:
        """Get product quantity."""
        txt = self.row_locator.locator(self._QUANTITY).inner_text().strip()
        return int(txt)

    @property
    def total(self) -> int:
        """Get total price (price × quantity) in Rs."""
        txt = self.row_locator.locator(self._TOTAL).inner_text()
        return self._parse_price(txt)

    @property
    def id(self) -> int:
        """Get product ID from the row element."""
        product_id = self.row_locator.get_attribute("id")
        return int(product_id.replace("product-", ""))

    def delete(self) -> None:
        """Click the delete button to remove this product from cart."""
        self.row_locator.locator(self._DELETE_BTN).click()

    def set_quantity(self, value: int) -> None:
        """
        Set the quantity in the cart's input field for this product row.

        Args:
            value: The new quantity to set
        """
        input_elem = self.row_locator.locator(self._INPUT)
        input_elem.fill(str(value))

    @staticmethod
    def _parse_price(text: str) -> int:
        """Parse price text like 'Rs. 1,234' into integer 1234."""
        return int(text.replace("Rs. ", "").replace(",", "").strip())


@dataclass
class CartPage:
    page: Page

    _TABLE = "table.table.table-condensed"
    _ROWS = "tr[id^='product-']"

    def get_product_row(self, product_id: int) -> ProductRow:
        row_locator = self.page.locator(self._TABLE).locator(
            f"tr#product-{product_id}"
        )
        return ProductRow(row_locator)

    def get_all_rows(self) -> list[ProductRow]:
        return [
            ProductRow(row)
            for row in self.page.locator(self._TABLE).locator(self._ROWS).all()
        ]

    def get_product_ids(self) -> list[int]:
        return [row.id for row in self.get_all_rows()]

    def assert_all_line_totals(self):
        for row in self.get_all_rows():
            assert (
                row.total == row.price * row.quantity
            ), f"Line total mismatch for id={row.id}: {row.total} != {row.price} * {row.quantity}"

    def get_total_cart_value(self) -> int:
        return sum(row.total for row in self.get_all_rows())
