from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from pathlib import Path
import time
import csv
from parsel import Selector


def browse(url):

    #getting chromedriver path
    script_dir = Path(__file__).parent
    path=(script_dir / 'chromedriver').resolve()
    #import chromedriver
    driver = webdriver.Chrome(path)

    # getting the website
    driver.get(url)
    driver.implicitly_wait(5)
    return driver 

def connect(driver,email,psw):
    driver.find_element_by_id('session_key').send_keys(email)
    time.sleep(0.5)
    driver.find_element_by_name('session_password').send_keys(psw)
    time.sleep(0.5)
    login = driver.find_element_by_class_name('sign-in-form__submit-button')
    ActionChains(driver).move_to_element(login).click().perform()
    driver.implicitly_wait(10)
    time.sleep(3)

def write_companies_info_in_file(driver, companies, file_name):
    with open(file_name, "a") as fp:
        wr = csv.writer(fp, dialect='excel')
        ## getting information of each company
        for elem in companies :
            wr.writerow(elem)
    fp.close()
    
def read_csv (file_name):
    l = []
    script_dir = Path(__file__).parent
    with open(str(script_dir)+'/'+ str(file_name)) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            l.append(row)
    return l

def main ():
    linkedin_urls = read_csv('linkedin_urls.csv')
    driver = browse('https://www.linkedin.com')
    connect(driver,'taha.clubiste@gmail.com','123TORNATITOS&')

    driver.execute_script(
    "(function(){try{for(i in document.getElementsByTagName('a')){let el = document.getElementsByTagName('a')[i]; "
    "if(el.innerHTML.includes('Contact info')){el.click();}}}catch(e){}})()")

    # Wait 5 seconds for the page to load
    time.sleep(3)

    for elems in linkedin_urls:
        for elem in elems:
            driver.get(elem)
            driver.implicitly_wait(10)
            time.sleep(3)
            #url
            url = elem

            #name
            name = driver.find_element_by_xpath('//*[@id="ember56"]/div[2]/div[2]/div[1]/ul[1]/li[1]').text
            #position
            position = driver.find_element_by_xpath('//*[@id="ember56"]/div[2]/div[2]/div[1]/h2').text
            #location
            location = driver.find_element_by_xpath('//*[@id="ember56"]/div[2]/div[2]/div[1]/ul[2]/li[1]').text
            #number of connection
            connections = driver.find_element_by_xpath('//*[@id="ember56"]/div[2]/div[2]/div[1]/ul[2]/li[2]/span').text

            #experience
            experience = driver.find_element_by_xpath('//*[@id="experience-section"]/ul/li')
            print('\n')
            print('url : ', url)
            print('name : ', name)
            print('position : ', position)
            print('location : ', location)
            print('connections : ', connections)
            print(experience)

            print('\n')
  
    time.sleep(5)
    driver.quit()
    


main()