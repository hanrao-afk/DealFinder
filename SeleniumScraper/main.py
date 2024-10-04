from selenium.common import TimeoutException, StaleElementReferenceException

from booking.booking import Booking

try:
    # Create an instance of the Booking class and use it as a context manager
    with Booking() as bot:
        # Navigate to the first page of the booking site
        bot.land_first_page()

        # Close any advertisement pop-ups
        bot.close_add()

        # Get user input for the destination
        bot.select_place_to_go(input("Where do you want to go? "))

        # Get user input for check-in and check-out dates
        bot.select_dates(
            check_in_date=input("What is the check-in date? (YYYY-MM-DD) "),
            check_out_date=input("What is the check-out date? (YYYY-MM-DD) ")
        )

        # Get user input for the number of adults
        bot.select_adults(input("How many adults? "))

        # Click the search button to find available options
        bot.click_search()

        # Apply filters to the search results
        bot.apply_filtration()

        # Generate and display the results report
        bot.report_results()

# Handle specific exceptions that may occur during the process
except TimeoutException as e:
    print(f"Timeout occurred: {e}. Please check your network connection or the website's availability.")
except StaleElementReferenceException as e:
    print(f"Stale element reference: {e}. The webpage may have changed, please try again.")
except Exception as e:
    # Handle the case where the Selenium driver is not in the system PATH
    if 'in PATH' in str(e):
        print(
            'You are trying to run the bot from the command line.\n'
            'Please add your Selenium Drivers to the PATH.\n'
            'Windows:\n'
            '    set PATH=%PATH%;C:path-to-your-folder\n\n'
            'Linux:\n'
            '    PATH=$PATH:/path/to/your/folder/\n'
        )
    else:
        # Re-raise any other exceptions not specifically handled
        raise
