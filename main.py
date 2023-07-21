from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium_profiles.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium_profiles.profiles import profiles


profile = profiles.Windows()
options = ChromeOptions()
options.add_argument('user-data-dir=C:\\Users\\urib9\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
mydriver = Chrome(profile)
pr = mydriver.profile
driver = mydriver.start()

driver.get('https://main.knesset.gov.il/Activity/Legislation/Laws/Pages/LawSuggestionsSearch.aspx?t=LawSuggestionsSearch&st=AllSuggestions')

try:

    # elements = driver.find_element('xpath','/html/body/form/div[6]/div/div[2]/div/span/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[2]/td/div[2]/div[1]/div/div/div/div/div[1]/div/div/div[2]/div/div/table/tbody')
    elements = driver.find_elements("class name", "rgRow")

    for element in elements:
        element.click()
        element.
except NoSuchElementException:
    print("Element not found")

driver.quit()



