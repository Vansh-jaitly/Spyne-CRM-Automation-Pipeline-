import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# This function remains largely the same, but with added logging to see progress.
def get_vehicle_count(driver, url, xpaths):
    """Navigates to a URL and tries to find the vehicle count using a list of XPaths."""
    try:
        print(f"  - Navigating to: {url}")
        driver.get(url)
        # Wait for a known element like the body to ensure the page starts loading
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Loop through all possible XPaths to find the count
        for xpath in xpaths:
            try:
                # Use a shorter wait time here, as we're just checking for an element
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                text = element.text
                # Use regex to find any number in the text
                numbers = re.findall(r'\d+', text.replace(',', ''))
                if numbers:
                    print(f"    -> Found count: {numbers[0]} using xpath: '{xpath}'")
                    return int(numbers[0])
            except TimeoutException:
                # This is expected if an XPath doesn't exist on the page, so we just continue
                continue
        
        print("    -> Could not find vehicle count on the page.")
        return "NA"

    except (WebDriverException, TimeoutException) as e:
        print(f"  - Error accessing or scraping {url}: {e}")
        return "NA"

def run_dealeron_scraper(input_file):
    """
    Initializes a single Chrome WebDriver instance and iterates through a CSV of dealerships
    to scrape new and used car counts.
    """
    # --- FIX 1: More robust Chrome Options to improve stability and reduce log spam ---
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")  # Often recommended for headless
    chrome_options.add_argument("--window-size=1920,1080") # Can help with layout issues
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--enable-unsafe-swiftshader") # Addresses the WebGL fallback warning
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")

    # --- FIX 2: Initialize WebDriver ONCE before the loop for huge performance gains ---
    try:
        # Using Service is the modern way to initialize the driver
        service = Service() 
        driver = webdriver.Chrome(service=service, options=chrome_options)
        # Set a page load timeout to prevent the script from hanging indefinitely
        driver.set_page_load_timeout(60) # Wait up to 60 seconds for a page to load
    except WebDriverException as e:
        print(f"FATAL: Failed to initialize WebDriver: {e}")
        return None

    # Read the input file
    try:
        dealerships_df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        driver.quit()
        return None

    results = []
    # Define XPaths once
    xpaths = [
        "//*[contains(text(), 'Showing all')]", 
        "//*[contains(text(), 'Showing') and contains(text(), 'of')]",
        "//span[contains(@class, 'total-results')]",
        "//span[contains(text(), 'Results')]", 
        "//div[contains(text(), 'Results')]",
        "//span[contains(text(), 'vehicles')]",
        "//div[contains(text(), 'vehicles')]",
        "//span[contains(@class, 'count')]", 
        "//*[contains(@class, 'total')]"
    ]

    # --- FIX 3: Use a try/finally block to ensure the driver always quits ---
    try:
        for index, row in dealerships_df.iterrows():
            company_name = row['Company name']
            domain = row['Company Domain Name']
            
            print(f"\nProcessing ({index + 1}/{len(dealerships_df)}): {company_name}")

            if not isinstance(domain, str) or not domain.strip():
                print("  - Skipping due to empty domain.")
                continue

            domain_norm = domain if domain.startswith('http') else 'https://' + domain
            
            # Default values
            new_cars_count = "NA"
            used_cars_count = "NA"
            website_status = "NA (Timeout or Error)"

            try:
                print(f"  - Checking main site: {domain_norm}")
                driver.get(domain_norm)
                # Wait for the body tag to confirm the site is loading
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                
                website_status = "Relevant"
                
                # Scrape New Cars
                new_car_url = domain_norm.rstrip('/') + "/searchnew.aspx"
                new_cars_count = get_vehicle_count(driver, new_car_url, xpaths)

                # Scrape Used Cars
                used_car_url = domain_norm.rstrip('/') + "/searchused.aspx"
                used_cars_count = get_vehicle_count(driver, used_car_url, xpaths)

                # If we couldn't find any counts, the site might not be relevant
                if new_cars_count == "NA" and used_cars_count == "NA":
                    website_status = "Potentially Irrelevant (No Counts Found)"

            except TimeoutException:
                print(f"  - TimeoutException: The website {domain_norm} is too slow or unresponsive.")
                website_status = "NA (Timeout)"
            except WebDriverException as e:
                print(f"  - WebDriverException on {domain_norm}: {e}")
                website_status = "NA (WebDriver Error)"

            results.append({
                "Company name": company_name,
                "Company Domain Name": row['Company Domain Name'],
                "Number Of Used Cars": used_cars_count,
                "Number Of New Cars": new_cars_count,
                "Website Status": website_status
            })

    finally:
        # This will run no matter what, ensuring the browser closes and doesn't leave zombie processes
        print("\nScraping complete. Closing WebDriver.")
        driver.quit()

    return pd.DataFrame(results)