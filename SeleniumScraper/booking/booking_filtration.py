from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException


class BookingFiltration:
    def __init__(self, driver: WebDriver):
        # Initialize the BookingFiltration class with the WebDriver instance
        self.driver = driver

    def apply_star_rating(self, *star_values):
        # Apply star ratings based on the provided values
        for attempt in range(3):  # Try up to 3 times
            try:
                # Wait for the star filtration box to be present
                star_filtration_box = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-filters-group="class"]'))
                )

                # Get all child elements within the star filtration box
                star_child_elements = star_filtration_box.find_elements(By.CSS_SELECTOR, "*")

                # Iterate through each star value to select
                for star_value in star_values:
                    for star_element in star_child_elements:
                        # Check if the element text matches the star value and if it's not already selected
                        if star_element.text.strip() == f'{star_value} stars' and not star_element.is_selected():
                            star_element.click()  # Click to select the star rating

                break  # Exit the retry loop on success
            except TimeoutException:
                break  # Exit if a timeout occurs
            except StaleElementReferenceException:
                if attempt == 2:  # Last attempt
                    raise  # Re-raise the exception to be handled elsewhere

    def sort_price_by_lowest_first(self):
        # Sort the results by the lowest price first
        for attempt in range(3):  # Try up to 3 times
            try:
                # Wait for the sorter dropdown to be clickable and click it
                sorter_dropdown = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="sorters-dropdown-trigger"]'))
                )
                sorter_dropdown.click()

                # Wait for the lowest first option to be clickable and click it
                lowest_first = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-id="price"]'))
                )
                lowest_first.click()
                break  # Exit the retry loop on success
            except TimeoutException:
                break  # Exit if a timeout occurs
            except StaleElementReferenceException:
                if attempt == 2:  # Last attempt
                    raise  # Re-raise the exception to be handled elsewhere
