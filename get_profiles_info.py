from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from pathlib import Path
import time
import csv
from linkedin_scraper import Person, actions

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

def write_profiles_info_in_file(profiles, file_name):
    with open(file_name, "a") as fp:
        wr = csv.writer(fp, dialect='excel')
        ## getting information of each company
        for elem in profiles :
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
    list_of_profiles = []

    for elems in linkedin_urls:
        for elem in elems:
            profile = []
            driver.get(elem)
            driver.implicitly_wait(10)
            time.sleep(3)

            person = Person(str(elem), driver = driver, scrape=False)
            person.scrape(close_on_complete=False)
            #name
            name = driver.find_element_by_xpath('//*[@id="ember56"]/div[2]/div[2]/div[1]/ul[1]/li[1]').text
            #position
            position = driver.find_element_by_xpath('//*[@id="ember56"]/div[2]/div[2]/div[1]/h2').text
            #location
            location = driver.find_element_by_xpath('//*[@id="ember56"]/div[2]/div[2]/div[1]/ul[2]/li[1]').text
            #number of connection
            connections = driver.find_element_by_xpath('//*[@id="ember56"]/div[2]/div[2]/div[1]/ul[2]/li[2]/span').text

            #experience
            print('\n')
            ## url
            print('url : ', person.linkedin_url)
            profile.append(person.linkedin_url)
            # name
            print('name : ', name)
            profile.append(name)
            ## position
            print('position : ', position)
            profile.append(position)
            ## location
            print('location : ', location)
            profile.append(location)
            ## connections
            print('connections : ', connections)
            profile.append(connections)
            ## experiences
            print('experiences : ', person.experiences)
            profile.append(person.experiences)
            ## educations
            print('education : ', person.educations)
            profile.append(person.educations)
            ## interests
            print('interests : ', person.interests)
            profile.append(person.interests)
            print('\n')

            list_of_profiles.append(profile)

    write_profiles_info_in_file(list_of_profiles,'profiles.csv')
    time.sleep(5)
    driver.quit()
    


main()