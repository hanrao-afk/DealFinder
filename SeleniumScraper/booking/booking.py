import os
import time
from selenium.webdriver.common.by import By
from datetime import datetime
from . import constants as const  # Keep this as is for relative import
from selenium import webdriver
from .booking_filtration import BookingFiltration  # Change this to relative import
from .booking_report import BookingReport
from prettytable import PrettyTable


class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"C:\SeleniumDrivers", teardown=False):
        # Initialize the Booking class as a Chrome WebDriver
        self.driver_path = driver_path
        self.teardown = teardown

        # Set the PATH environment variable to include the driver path
        os.environ['PATH'] += self.driver_path

        # Configure Chrome options
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Suppress logging
        super(Booking, self).__init__(options=options)

        self.implicitly_wait(10)  # Implicitly wait for elements to be ready
        self.maximize_window()  # Maximize the browser window

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Quit the browser if teardown is enabled
        if self.teardown:
            self.quit()

    def land_first_page(self):
        # Navigate to the base URL
        self.get(const.BASE_URL)

    def close_add(self):
        # Attempt to close any pop-up advertisements
        try:
            close_element = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Dismiss sign-in info."]')
            close_element.click()
        except Exception as e:
            print("Ad did not appear or could not be closed:", str(e))

    def select_place_to_go(self, place_to_go):
        # Select a destination by entering the place in the search field
        search_field = self.find_element(By.NAME, "ss")
        search_field.clear()
        search_field.send_keys(place_to_go)

        # Click on the first search result
        first_result = self.find_element(By.XPATH, f'//div[@role="button"]//div[contains(text(), "{place_to_go}")]')
        first_result.click()

    def get_month_clicks(self, today_date, check_in_date, check_out_date):
        # Convert the date strings to datetime objects
        today_date_obj = datetime.strptime(today_date, '%Y-%m-%d')
        check_in_date_obj = datetime.strptime(check_in_date, '%Y-%m-%d')
        check_out_date_obj = datetime.strptime(check_out_date, '%Y-%m-%d')

        # Extract the month from each date
        today_month = today_date_obj.month
        check_in_month = check_in_date_obj.month
        check_out_month = check_out_date_obj.month

        # Calculate clicks required to reach check-in month
        if check_in_month >= today_month:
            check_in_clicks = check_in_month - today_month
        else:
            check_in_clicks = (12 - today_month) + check_in_month

        # Calculate clicks required to reach check-out month
        if check_out_month >= today_month:
            check_out_clicks = check_out_month - today_month
        else:
            check_out_clicks = (12 - today_month) + check_out_month

        return check_in_clicks, check_out_clicks

    def select_dates(self, check_in_date, check_out_date):
        # Get today's date and format it
        today = datetime.today()
        formatted_date = today.strftime("%Y-%m-%d")

        # Calculate how many months to click for check-in and check-out dates
        check_in_click, check_out_click = self.get_month_clicks(formatted_date, check_in_date, check_out_date)

        # Click to navigate to the appropriate check-in month
        click_next_month = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Next month"]')
        for _ in range(check_in_click):
            click_next_month.click()

        # Click on the check-in date
        check_in_element = self.find_element(By.CSS_SELECTOR, f'span[data-date="{check_in_date}"]')
        check_in_element.click()

        # Click to navigate to the appropriate check-out month
        for _ in range(check_out_click - check_in_click):
            click_next_month.click()

        # Click on the check-out date
        check_out_element = self.find_element(By.CSS_SELECTOR, f'span[data-date="{check_out_date}"]')
        check_out_element.click()

    def select_adults(self, count):
        # Open the adults selection menu
        selection_element = self.find_element(By.CSS_SELECTOR, '.d777d2b248')
        selection_element.click()

        # Decrease the number of adults to 1
        while True:
            decrement_adults = self.find_element(By.CSS_SELECTOR,
                                                 'button.a83ed08757.c21c56c305.f38b6daa18.d691166b09.ab98298258.e91c91fa93')
            decrement_adults.click()

            adults_value_count = self.find_element(By.ID, "group_adults")
            adults_value = adults_value_count.get_attribute('value')  # Get current adults count
            if int(adults_value) == 1:
                break

        # Increase the number of adults to the specified count
        increment_adults = self.find_element(By.CSS_SELECTOR,
                                             'button.a83ed08757.c21c56c305.f38b6daa18.d691166b09.ab98298258.bb803d8689.f4d78af12a')
        for _ in range(int(count) - 1):
            increment_adults.click()

    def click_search(self):
        # Click the search button to initiate the search
        search_button = self.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        search_button.click()

    def apply_filtration(self):
        # Create an instance of BookingFiltration to apply filters
        filtration = BookingFiltration(driver=self)

        # Apply star ratings
        filtration.apply_star_rating(3, 4, 5)

        # Optional: Add a small delay for the UI to update
        time.sleep(2)  # Wait a moment for the UI to update

        # Apply sorting to filter results
        filtration.sort_price_by_lowest_first()

    def report_results(self):
        # Retrieve the container for the results
        container = self.find_element(By.CSS_SELECTOR, 'div.d4924c9e74[data-results-container="1"]')
        property_cards = container.find_elements(By.CSS_SELECTOR, '[data-testid="property-card"]')

        # Create a report instance for the container
        report = BookingReport(container)

        # Create a PrettyTable to display results
        table = PrettyTable(field_names=["Hotel Name", "Hotel Price", "Hotel Score"])
        table.add_rows(report.pull_deal_box_attributes())  # Add rows from the report

        print(table)  # Print the table to the console
