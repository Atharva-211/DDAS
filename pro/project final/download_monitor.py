import time
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def init_browser():
    options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": "C:/Users/athar/Downloads",  # Set your download directory
        "download.prompt_for_download": False,  # Disable download prompt
        "profile.default_content_settings.popups": 0,
        "directory_upgrade": True
    }
    options.add_experimental_option("prefs", prefs)
    
    # Provide path to your ChromeDriver executable
    service = Service("path/to/chromedriver")  # Update this path to point to your chromedriver

    # Initialize Chrome WebDriver
    driver = webdriver.Chrome(service=service, options=options)
    return driver


# Monitor downloads and check for duplicate URLs
def monitor_downloads(driver):
    while True:
        try:
            # Assuming the download starts when a button is clicked
            # For example, find the download link/button and get the URL
            download_button = driver.find_element(By.XPATH, '//a[@class="download-link"]')  # Example selector
            download_url = download_button.get_attribute('href')

            # Check if the URL has been downloaded before
            if download_url in downloaded_urls:
                print(f"Duplicate download detected for URL: {download_url}")
                driver.execute_script("alert('This file has already been downloaded.');")
                time.sleep(2)
                driver.switch_to.alert.accept()  # Close the alert
            else:
                print(f"New download initiated: {download_url}")
                downloaded_urls.append(download_url)
                save_downloaded_urls()

            time.sleep(1)

        except Exception as e:
            print(f"Error: {e}")
        time.sleep(5)  # Wait before checking again

if __name__ == "__main__":
    driver = init_browser()
    driver.get("https://example.com/download-page")  # Set your target download page
    monitor_downloads(driver)
