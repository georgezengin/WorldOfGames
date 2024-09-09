from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys

# e2e.py

def test_scores_service(url: str) -> bool:
    """
    Test the web service by accessing the URL using Selenium, extracting the score, and 
    checking if it's between 1 and 1000.

    :param url: The URL of the web service
    :return: True if the score is between 1 and 1000, otherwise False
    """
    try:
        # Set up Selenium WebDriver (Ensure chromedriver is in your PATH or specify the executable_path)
        driver = webdriver.Chrome()  # Make sure chromedriver is installed or in PATH

        # Open the web page
        driver.get(url)
        
        # Give the page some time to load
        time.sleep(2)  # Optional: adjust sleep time based on your page load time
        
        # Find the score element by its ID
        score_element = driver.find_element(By.ID, "score")
        
        # Get the score text and convert it to an integer
        score = int(score_element.text.strip())
        
        # Close the browser
        driver.quit()

        # Validate the score is within range 1 to 1000
        if 1 <= score <= 1000:
            print(f"Score is valid: {score}")
            return True
        else:
            print(f"Score is out of range: {score}")
            return False

    except Exception as e:
        print(f"Error during test: {str(e)}")
        return False

def main_function():
    """
    Main function to run the test_scores_service function and handle exit codes.

    :return: 0 if tests pass, -1 if they fail
    """
    # URL of the web service to test
    url = "http://127.0.0.1:5000"  # Change this to your actual URL if necessary

    # Run the test
    if test_scores_service(url):
        print("Test passed.")
        sys.exit(0)  # Exit code 0 for success
    else:
        print("Test failed.")
        sys.exit(-1)  # Exit code -1 for failure

if __name__ == "__main__":
    main_function()
