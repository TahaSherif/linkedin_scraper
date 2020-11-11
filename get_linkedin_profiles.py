from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from pathlib import Path
import time
import csv

def browse(url):

    #getting chromedriver path
    script_dir = Path(__file__).parent
    path=(script_dir / 'chromedriver').resolve()
    #disabling images
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    #import chromedriver
    driver = webdriver.Chrome(path,chrome_options=chrome_options)

    # getting the website
    driver.get(url)
    driver.implicitly_wait(5)
    return driver 

def search(driver):
    # locate search form by_name
    search_query = driver.find_element_by_name('q')

    # send_keys() to simulate the search text key strokes
    search_query.send_keys('site:linkedin.com/in/ AND "data scientist" AND "United State"')
    time.sleep(0.5)

    # .send_keys() to simulate the return key 
    search_query.send_keys(Keys.RETURN)

def write_linkedin_urls_in_file(driver, companies, file_name):
    with open(file_name, "a") as fp:
        wr = csv.writer(fp, dialect='excel')
        ## getting information of each company
        for elem in companies :
            wr.writerow(elem)
    fp.close()


def main():
    driver = browse('https://www.google.com/?hl=en')
    search(driver)
    time.sleep(5)

    page = 0
    linkedin_urls = []
    while page < 29 :
        urls = driver.find_elements_by_css_selector("div.yuRUbf [href]")
        links = [elem.get_attribute('href') for elem in urls]
        i = 0
        while i < len(links) :
            if links[i][12] =='g':
                links.pop(i)
            else:
                i += 1
        linkedin_urls.append(links)
        print(links)
        next = driver.find_element_by_xpath('//*[@id="pnnext"]/span[2]')
        ActionChains(driver).move_to_element(next).click().perform()
        driver.implicitly_wait(5)
        time.sleep(3)
        page += 1

    write_linkedin_urls_in_file(driver,linkedin_urls,'linkedin_urls.csv')
    driver.quit()

main()