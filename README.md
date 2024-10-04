# Deal Finder

## Description
Deal Finder is a web scraping tool built using Selenium, designed to help users find and filter hotel deals based on their travel preferences. The bot interacts with a booking website, allowing users to input their destination, check-in and check-out dates, and the number of adults, then retrieves and displays the available options.

### Main Components
- **main.py**: The entry point of the application that initializes the booking process and handles user inputs.
- **booking/**: A package containing classes and methods that manage the booking process:
  - **booking.py**: Contains the `Booking` class, which encapsulates the web scraping logic using Selenium.
  - **booking_filtration.py**: Contains the `BookingFiltration` class, responsible for applying filters to the search results.
  - **booking_report.py**: Contains the `BookingReport` class, which formats and presents the search results.
  - **constants.py**: Contains constants such as the base URL for the booking site.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Deal-Finder.git
   cd Deal-Finder/SeleniumScraper

2. Install the required dependencies:
    pip install -r requirements.txt
    Ensure you have Selenium and PrettyTable installed.

3. Set up the Selenium WebDriver:
    Download the appropriate WebDriver for your browser and add it to your system PATH.

## Usage

1. Run the application:
   ```bash
   python main.py

2. Follow the prompts to enter your travel details:

   Enter your destination.
   Provide the check-in and check-out dates (format: YYYY-MM-DD).
   Specify the number of adults.






