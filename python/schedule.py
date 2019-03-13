# Selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from openpyxl import Workbook

import selenium.webdriver.chrome.service as service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import TimeoutException

import os
import json
import datetime, re, sys
import pytz
import time
import openpyxl

from bs4 import BeautifulSoup
import requests

from sys import platform

# External Files
from CCLE_professor_parser import CCLEHTMLParser

# ********************************************************************************
# Chrome Driver Helpers

# fill out simple input fields
def fillInput(driver, xpath, value):
    name = check_exists_by_xpath(xpath, driver)
    name.click()
    sendKeys(value, name, driver)

# check for existence of input element in dom
def check_exists_by_xpath(xpath, driver):
    try:
        myElem = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        myElem = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return driver.find_element_by_xpath(xpath)

# fill out the input field with value
def sendKeys(value, field, driver):
    if len(value) < 1:
        return None
    try:
        driver.execute_script("arguments[0].value = '" + value + "';", field)
    except WebDriverException:
        print(field.get_attribute('Name'))

# return HTML from a parent tag
def getHTML(element, attributes):
    global driver

    # Get the current page's HTML
    page_response = requests.get(driver.current_url, timeout=5)

    # Get Lower Div Courses
    # Create a soup
    soup = BeautifulSoup(page_response.content, "html.parser")
    data = soup.find(element, attributes)
    print("********************")
    # TODO: parse this
    print(data.findChildren())
    print("********************")

# Store the driver as a global
driver = ""

# ********************************************************************************
# Scrape Schedule of Classes
def sched_scrape():
    global driver

    majors = ["Aerospace Studies", "African American Studies", "African Studies", "American Indian Studies", "American Sign Language", "Ancient Near East", "Anesthesiology", "Anthropology", "Applied Linguistics", "Arabic", "Archaeology", "Architecture and Urban Design", "Armenian", "Art", "Art History", "Arts and Architecture", "Arts Education", "Asian", "Asian American Studies", "Astronomy", "Atmospheric and Oceanic Sciences", "Bioengineering", "Bioinformatics", "Bioinformatics", "Biological Chemistry", "Biomathematics", "Biomedical Research", "Biostatistics", "Chemical Engineering", "Chemistry and Biochemistry", "Chicana and Chicano Studies", "Chinese", "Civic Engagement", "Civil and Environmental Engineering", "Classics", "Clusters", "Communication", "Community Health Sciences", "Comparative Literature", "Computational and Systems Biology", "Computer Science", "Conservation of Archaeological and Ethnographic Materials", "Dance", "Dentistry", "Design / Media Arts", "Digital Humanities", "Disability Studies", "Dutch", "Earth, Planetary, and Space Sciences", "Ecology and Evolutionary Biology", "Economics", "Education", "Electrical and Computer Engineering", "Engineering", "English", "English as A Second Language", "English Composition", "Environment", "Environmental Health Sciences", "Epidemiology", "Ethnomusicology", "Family Medicine", "Filipino", "Film and Television", "Food Studies", "French", "Gender Studies", "Geography", "German", "Gerontology", "Global Health", "Global Jazz Studies", "Global Studies", "Graduate Student Professional Development", "Greek", "Health Policy and Management", "Hebrew", "Hindi-Urdu", "History", "Honors Collegium", "Human Genetics", "Hungarian", "Indigenous Languages of the Americas", "Indo-European Studies", "Indonesian", "Information Studies", "International and Area Studies", "International Development Studies", "International Migration Studies", "Iranian", "Islamic Studies", "Italian", "Japanese", "Jewish Studies", "Korean", "Labor and Workplace Studies", "Latin", "Latin American Studies", "Law", "Lesbian, Gay, Bisexual, Transgender, and Queer Studies", "Life Sciences", "Linguistics", "Management", "Management-Executive MBA", "Management-Master of Financial Engineering", "Management-Master of Science in Business Analytics", "Management-PhD", "Materials Science and Engineering", "Mathematics", "Mechanical and Aerospace Engineering", "Medical History", "Medicine", "Microbiology, Immunology, and Molecular Genetics", "Middle Eastern Studies", "Military Science", "Molecular and Medical Pharmacology", "Molecular Biology", "Molecular Toxicology", "Molecular, Cell, and Developmental Biology", "Molecular, Cellular, and Integrative Physiology", "Music", "Music Industry", "Musicology", "Naval Science", "Near Eastern Languages", "Neurobiology", "Neurology", "Neuroscience", "Neuroscience", "Neurosurgery", "Nursing", "Obstetrics and Gynecology", "Ophthalmology", "Oral Biology", "Orthopaedic Surgery", "Pathology and Laboratory Medicine", "Pediatrics", "Philosophy", "Physics", "Physics and Biology in Medicine", "Physiological Science", "Physiology", "Polish", "Political Science", "Portuguese", "Program in Computing", "Psychiatry and Biobehavioral Sciences", "Psychology", "Public Affairs", "Public Health", "Public Policy", "Radiation Oncology", "Religion, Study of", "Romanian", "Russian", "Scandinavian", "Science Education", "Semitic", "Serbian/Croatian", "Slavic", "Social Science", "Social Thought", "Social Welfare", "Society and Genetics", "Sociology", "South Asian", "Southeast Asian", "Spanish", "Statistics", "Surgery", "Swahili", "Thai", "Theater", "Turkic Languages", "University Studies", "Urban Planning", "Urology", "Vietnamese", "World Arts and Cultures", "Yiddish"]

    for major in majors:

        # Go to schedule of classes page
        url = "https://sa.ucla.edu/ro/public/soc"
        driver.get(url)

        # click on dropdown input
        subject_area_input = check_exists_by_xpath("""//*[@id="select_filter_subject"]""", driver)
        time.sleep(1)
        subject_area_input.click()
        time.sleep(1)

        print("Clicked input")

        # TODO: do majors have to be visible? try typing the majors instead of clicking?
        # select the major
        class_dropdown = check_exists_by_xpath("""//*[@id="select_filter_subject"]""", driver)
        class_dropdown.click()
        state = driver.find_elements_by_xpath("//*[contains(text(), '" + major + "')]")
        # Select the major from the dropdown
        for s in state:                        # only one of the returned elements is clickable, not sure which one
            driver.execute_script("arguments[0].click()", s)
        driver.execute_script("arguments[0].click();", state[1])

        # Click the go button
        go = check_exists_by_xpath("""//*[@id="btn_go"]""", driver)
        time.sleep(1)
        go.click()
        time.sleep(1)

        try:
            numbers = check_exists_by_xpath("""//*[@class="jPag-pages"]""", driver)

            if len(numbers) != 0:
                print("###")
                print(numbers)
                for number in numbers:
                    driver.execute_script("arguments[0].click();", number)

        except:
            print("hi")

        # Click on the "expand all" button to see section information
        expand_classes = check_exists_by_xpath("""//*[@id="divExpandAll"]""", driver)
        time.sleep(1)

        # Get the current page's HTML
        page_response = requests.get(driver.current_url, timeout=5)

        # Create a soup
        soup = BeautifulSoup(page_response.content, "html.parser")
        classes = soup.find(id="divSearchResults")
        print(classes.findChildren())

        # TODO: extract info from the soup, info may not be accessible because of js

        # TODO: there may be multiple pages of classes, need to go through each one


# ********************************************************************************
# Scrape Course Descriptions

def descriptions_scrape():

    # TODO: parse HTML that is output

    global driver

    # TODO: get all major names in a file and read from that

    with open('major_list.json') as json_file:
        data = json.load(json_file)
    majors = data["majors"]


    for major in majors:
        url = "https://www.registrar.ucla.edu/Academics/Course-Descriptions"
        driver.get(url)

        # click on dropdown input
        try:
            className = driver.find_elements_by_xpath("//*[contains(text(), '" + major + "')]")
            time.sleep(1)
            print(className)
            driver.execute_script("arguments[0].click();", className[0])
            time.sleep(1)

        except:
            print("* " + major)


        # Get the default course set (usually Lower Divs come up first)
        getHTML("ul", {"class": "media-list category-list"})

        # Get Upper Div Courses
        upperDivButton = driver.find_elements_by_xpath("//*[contains(text(), '" + "Upper Division Courses" + "')]")
        if len(upperDivButton) != 0:
            driver.execute_script("arguments[0].click();", upperDivButton[0])
            getHTML("div", {"class": "tab-content"})

        # Get Graduate Courses
        upperDivButton = driver.find_elements_by_xpath("//*[contains(text(), '" + "Graduate Courses" + "')]")
        if len(upperDivButton) != 0:
            driver.execute_script("arguments[0].click();", upperDivButton[0])
            getHTML("div", {"class": "tab-content"})

# ********************************************************************************
# Scrape CCLE Descriptions

def ccle_professor_scraper(major, quarter):
    """
    major format: 'COM%20SCI', or 'AF%20AMER' etc.
    quarter format: '19F', '18W', etc.

    returns a list of (class id, professor, full class title) lists
    """
    global driver

    url = 'https://ccle.ucla.edu/blocks/ucla_browseby/view.php?term={}&type=course&subjarea={}'.format(quarter, major)
    driver.get(url)

    page_source = driver.page_source
    ccle_professor_parser = CCLEHTMLParser()

    return ccle_professor_parser.get_class_professor_list(page_source)

# start the driver and return it
def setup_driver():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)

    print("Starting driver")

    if platform == "linux" or platform == "linux2":
        print("Don't have linux chrome driver")
        return

    if platform == "darwin":  # OS X
        driver = webdriver.Chrome(executable_path = './chromedrivers/chromedriver', chrome_options=chrome_options)
    elif platform == "win32":   # Windows...
        driver = webdriver.Chrome(executable_path = '.chromedrivers/chromedriver.exe', chrome_options=chrome_options)

    return driver

def main():

    global driver

    driver = setup_driver()

    # Scrape the schedule of classes
    sched_scrape()

    # Scrape Class Descriptions
    # descriptions_scrape()

    # Scrape Professors
    # ccle_professor_scraper(quarter='19W', major='COM%20SCI')
    time.sleep(10)

    # driver.close()

if __name__ == '__main__':
    main()
