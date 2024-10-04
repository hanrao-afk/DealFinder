# This file includes the method that will parse
# the specific data needed from each deal box.

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class BookingReport:
    def __init__(self, boxes_section_element: WebElement):
        # Initialize the BookingReport class with the section containing deal boxes
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()  # Retrieve deal boxes on initialization

    def pull_deal_boxes(self):
        # Find and return all deal boxes within the given section element
        return self.boxes_section_element.find_elements(By.CSS_SELECTOR, '[data-testid="property-card"]')

    def pull_deal_box_attributes(self):
        # Extract attributes from each deal box and store them in a collection
        collection = []
        for deal_box in self.deal_boxes:
            # Extract the listing title
            listing_title = deal_box.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]').text

            # Extract the price element
            price_element = deal_box.find_element(By.CSS_SELECTOR,
                                                  'span[data-testid="price-and-discounted-price"]').text

            try:
                # Attempt to extract the rating element
                rating_element = deal_box.find_element(By.CSS_SELECTOR, '[data-testid="review-score"]').text
                # Split the rating text into lines, filter out empty lines, and join them into a single formatted string
                rating_element_lines = rating_element.split('\n')
                formatted_rating = ', '.join(filter(bool, rating_element_lines))  # Join with ', ' instead of ' '
            except NoSuchElementException:
                # If the rating element is not found, set the rating to 'No rating'
                formatted_rating = 'No rating'

            # Append the extracted attributes to the collection
            collection.append([listing_title, price_element, formatted_rating])

        return collection  # Return the collected attributes
