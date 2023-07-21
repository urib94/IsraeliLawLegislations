from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium_profiles.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium_profiles.profiles import profiles
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import logging
logging.basicConfig(level=logging.INFO) 
logging.basicConfig(format='%(levelname)s: %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger("bills scraper")
profile = profiles.Windows()
options = ChromeOptions()
options.add_argument('user-data-dir=C:\\Users\\urib9\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
mydriver = Chrome(profile)
pr = mydriver.profile
driver = mydriver.start()
driver.refresh()

driver.get('https://main.knesset.gov.il/Activity/Legislation/Laws/Pages/LawSuggestionsSearch.aspx?t=LawSuggestionsSearch&st=AllSuggestions')
wait = WebDriverWait(driver, 3)

def handle_timeout(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TimeoutException:
            return ''
    return wrapper

@handle_timeout
def get_legislators():
    element =  wait.until(EC.visibility_of_element_located((By.XPATH, f'/html/body/form/div[5]/div/div[2]/div/span/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[2]/td/div[2]/div[1]/div/div/div/div/div[1]/div/div[1]/table/tbody/tr[5]/td[2]')))
    legislators = element.text.split(' ,')
    return legislators

@handle_timeout 
def get_bill_date():
    element =  wait.until(EC.visibility_of_element_located((By.XPATH, f'/html/body/form/div[5]/div/div[2]/div/span/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[2]/td/div[2]/div[1]/div/div/div/div/div[1]/div/div[1]/table/tbody/tr[11]/td[2]/div[1]')))
    bill_date = element.text
    return bill_date

@handle_timeout 
def get_bill_status():
    element =  wait.until(EC.visibility_of_element_located((By.XPATH, f'/html/body/form/div[5]/div/div[2]/div/span/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[2]/td/div[2]/div[1]/div/div/div/div/div[1]/div/div[1]/table/tbody/tr[1]/td/table/tbody/tr/td[4]/div[1]/div[2]')))
    bill_status = element.text
    return bill_status

def get_knesset_number(row):    
    element =  wait.until(EC.visibility_of_element_located((By.XPATH, f'/html/body/form/div[6]/div/div[2]/div/span/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[2]/td/div[2]/div[1]/div/div/div/div/div[1]/div/div/div[2]/div/div/table/tbody/tr[{row}]/td[1]')))
    return int(element.accessible_name)

@handle_timeout 
def get_bill_id():
    element =  wait.until(EC.visibility_of_element_located((By.XPATH, f'/html/body/form/div[5]/div/div[2]/div/span/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[2]/td/div[2]/div[1]/div/div/div/div/div[1]/div/div[1]/table/tbody/tr[1]/td/table/tbody/tr/td[3]/div[1]/div[2]')))
    bill_id = element.text
    return bill_id

@handle_timeout 
def get_bill_type():
    element =  wait.until(EC.visibility_of_element_located((By.XPATH, f'/html/body/form/div[5]/div/div[2]/div/span/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[2]/td/div[2]/div[1]/div/div/div/div/div[1]/div/div[1]/table/tbody/tr[1]/td/table/tbody/tr/td[2]/div[1]/div[2]')))
    bill_type = element.text
    return bill_type

def get_num_of_bills():
    element =  wait.until(EC.visibility_of_element_located((By.XPATH, f'/html/body/form/div[6]/div/div[2]/div/span/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[2]/td/div[2]/div[1]/div/div/div/div/div[1]/div/div/table/tbody/tr[2]/td/table/tbody/tr[10]/td[1]/div/label')))
    num_of_bills = int(element.text.split(' ')[1])
    return num_of_bills


def extract_page():    
    page_bills = []
    row = 1
    while True:
        try:
            knesset_number = get_knesset_number(row)
            
            bill_link = wait.until(EC.visibility_of_element_located((By.XPATH, f'/html/body/form/div[6]/div/div[2]/div/span/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[2]/td/div[2]/div[1]/div/div/div/div/div[1]/div/div/div[2]/div/div/table/tbody/tr[{row}]/td[2]/a')))
            
            bill_link.click()
            
            bill_type = get_bill_type()
            bill_legislators = get_legislators() 
            bill_date = get_bill_date()
            bill_status = get_bill_status()
            bill_id = get_bill_id()
            
            page_bills.append(
                {
                    "knesset_number": knesset_number,
                    "bill_type": bill_type,
                    "bill_legislators": bill_legislators,
                    "bill_date": bill_date,
                    "bill_status": bill_status,
                    "bill_id": bill_id
                }
            )
            driver.back()
            
            
        except TimeoutException:
            logger.info(f'completed scraping {row} bills')
            break
        row += 1
        
    return page_bills
        
def go_to_next_page():
        link_to_next_page =  wait.until(EC.visibility_of_element_located((By.XPATH, f'/html/body/form/div[6]/div/div[2]/div/span/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[2]/td/div[2]/div[1]/div/div/div/div/div[1]/div/div/div[2]/div/table/tbody/tr/td/a[5]')))
        link_to_next_page.click()

     
def extract_all_pages():
    
    bills = []  
    page  = 1
    while True:
        bills += extract_page()
        
        try:
            go_to_next_page()
        except TimeoutException:
            logger.info(f'completed scraping {page} pages')
            break  
        page += 1   


extract_all_pages()
driver.quit()