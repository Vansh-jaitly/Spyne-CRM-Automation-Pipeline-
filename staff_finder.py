import pandas as pd
import re
import time
import logging
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_driver():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--user-agent=Mozilla/5.0')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def normalize_url(url):
    if not url:
        return None
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url

def check_staff_pages(driver, base_url):
    staff_pages = [
        '/staff', '/meet-our-staff', '/meet-the-staff', '/team',
        '/meet-our-team', '/meet-the-team', '/our-staff', '/our-team'
    ]
    staff_page_found = False
    staff_page_content = ""
    for page in staff_pages:
        try:
            staff_url = urljoin(base_url, page)
            driver.get(staff_url)
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            if "404" not in driver.title.lower():
                staff_page_found = True
                staff_page_content += driver.page_source
        except:
            continue
    return staff_page_found, staff_page_content

def count_words_on_website(url, words_to_search):
    driver = None
    try:
        url = normalize_url(url)
        if not url:
            return (url, 'Invalid URL', None, False)
        driver = setup_driver()
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(1)
        page_source = driver.page_source.lower()
        staff_page_found, staff_page_content = check_staff_pages(driver, url)
        page_source += staff_page_content.lower()
        word_counts = {word: len(re.findall(r'\b' + re.escape(word.lower()) + r'\b', page_source)) for word in words_to_search}
        total_matches = sum(word_counts.values())
        status = 'Staff Found' if total_matches > 0 else 'No Staff Info'
        return (url, status, word_counts, staff_page_found)
    except TimeoutException:
        return (url, 'Timeout', None, False)
    except WebDriverException:
        return (url, 'WebDriver Error', None, False)
    finally:
        if driver:
            driver.quit()

def run_staff_finder(input_file):
    words_to_search = ["staff", "team", "management", "sales", "service"]
    try:
        df = pd.read_csv(input_file)
        if 'Company Domain Name' not in df.columns:
            logger.error("'Company Domain Name' column not found in input CSV")
            return None
        urls = df['Company Domain Name'].dropna().drop_duplicates().tolist()
        results = []
        for url in urls:
            url, status, word_counts, staff_page_found = count_words_on_website(url, words_to_search)
            row = {
                'Company Domain Name': url,
                'Status': status,
                'Staff_Page_Found': 'Yes' if staff_page_found else 'No',
                'Total_Matches': sum(word_counts.values()) if word_counts else 0
            }
            row.update(word_counts if word_counts else {w: 0 for w in words_to_search})
            results.append(row)
        return pd.DataFrame(results)
    except Exception as e:
        logger.error(f"Error: {e}")
        return None
