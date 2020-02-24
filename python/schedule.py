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
import json
import pymongo
import sys

from bs4 import BeautifulSoup
from pymongo import IndexModel, ASCENDING, DESCENDING
import requests

from sys import platform

# External Files
from CCLE_professor_parser import CCLEHTMLParser
import Dependencies

# only use computer science as the major to see if scraping is working
testing = False

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

# return soup for HTML from a parent tag
def getHTML(element, attributes):
    global driver

    # Get the current page's HTML
    page_response = requests.get(driver.current_url, timeout=5)

    # Get Lower Div Courses
    soup = BeautifulSoup(page_response.content, "html.parser")
    data = soup.find(element, attributes)

    return data

# Store the driver as a global variable
driver = ""

# ********************************************************************************
# Scrape Schedule of Classes
def sched_scrape():
    global driver, testing

    majorMap = {}   # store pre-reqs for each major
    majors = []

    if testing:
        majors = ['Computer Science']
    else:
        # TODO: go through each dept in client.Metis.Departments
        with open('major_list.json') as json_file:
            data = json.load(json_file)
        majors = data["majors"]

    #with open('complete10.json') as json_file:
    #    majorMap = json.load(json_file)

    for major in majors:
        if major in majorMap:
            if majorMap[major] != "Error":
                continue
        try:
            majorMap[major] = {}
            courseMap = majorMap[major]

            # Go to schedule of classes page
            url = "https://sa.ucla.edu/ro/public/soc"
            driver.get(url)

            # TODO: select term from dropdown, difficult to see the year and pick the right term

            # click on dropdown input
            subject_area_input = check_exists_by_xpath("""//*[@id="select_filter_subject"]""", driver)
            time.sleep(2)
            subject_area_input.click()
            time.sleep(2)

            # TODO: do majors have to be visible? try typing the majors instead of clicking?
            # select the major
            class_dropdown = check_exists_by_xpath("""//*[@id="select_filter_subject"]""", driver)
            class_dropdown.click()
            state = driver.find_elements_by_xpath("//*[contains(text(), '" + major + "')]")

            # Select the major from the dropdown
            for s in state:
                # only one of the returned elements is clickable, not sure which one so try all
                driver.execute_script("arguments[0].click()", s)
            driver.execute_script("arguments[0].click();", state[1])

            # Click the go button
            go = check_exists_by_xpath("""//*[@id="btn_go"]""", driver)
            time.sleep(2)
            go.click()
            time.sleep(2)

            # go through all pages of a major, if they exist
            lim = 0
            try:
                pages = driver.find_elements_by_xpath("""//*[@class="jPag-pages"]""")
                li_list = pages[0].find_elements_by_xpath(".//*")
                li_list = li_list[::2]
                lim = len(li_list)
            except:
                lim = 1

            for i in range(0, lim):

                if lim != 1:
                    # repeat because the links have been refreshed
                    pages = driver.find_elements_by_xpath("""//*[@class="jPag-pages"]""")
                    li_list = pages[0].find_elements_by_xpath(".//*")
                    li_list = li_list[::2]

                    # click twice, bug sometimes doesn't expand all classes otherwise
                    driver.execute_script("arguments[0].click();", li_list[i])
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", li_list[i])
                    time.sleep(1)

                # Click on the "expand all" button to see section information
                expand_classes = check_exists_by_xpath("""//*[@id="expandAll"]""", driver)
                driver.execute_script("arguments[0].click();", expand_classes)

                time.sleep(15)

                # Click on "lec1", "lab1", etc. to open new tab
                sections = driver.find_elements_by_xpath("""//*[@class="hide-small"]""")    # get elements that hold the anchor tags
                # for each element found, get the anchor tag child
                section_links = []
                for s in sections:
                    section_links.append(s.find_elements_by_xpath(".//*"))

                # click on the anchor tags, switch to new tab, close it, switch back to original tab
                for section in section_links:

                    # don't need discussions to get pre-reqs

                    if ("Dis" not in section[0].text and "Tut" not in section[0].text) or ("Sem" in section[0].text and (section[0].text == "Sem 1")) or ("Lab" in section[0].text and (section[0].text == "Lab 1" or section[0].text == "Lab 1A")):
                        if ("Sem" in section[0].text and section[0].text!="Sem 1"):
                            continue
                        if ("Lab" in section[0].text and (section[0].text != "Lab 1" and section[0].text != "Lab 1A")):
                            continue

                        driver.execute_script("arguments[0].click();", section[0])
                        time.sleep(2)
                        driver.switch_to.window(driver.window_handles[1])

                        # Get the current page's HTML
                        page_response = requests.get(driver.current_url, timeout=5)

                        # Get pre-reqs with getReqs()
                        courseTitle=re.search(r'subject_class[\s\S]*?( .*?) - ',page_response.text).group(1).strip()
                        courseTitle = " ".join(courseTitle.split())
                        courseTitle = courseTitle.replace("%26", "&")
                        courseTitle = courseTitle.replace("&amp;", "&")
                        try:
                            courseMap[courseTitle] = Dependencies.getReqs(page_response.text)

                            time.sleep(2)
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                        except:
                            courseMap[courseTitle] = "Error"
                            time.sleep(2)
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                        #time.sleep(1)
                        #driver.close()
                        #driver.switch_to.window(driver.window_handles[0])

                # Get the current page's HTML
                page_response = requests.get(driver.current_url, timeout=5)

                # Create a soup
                soup = BeautifulSoup(page_response.content, "html.parser")
                classes = soup.find(id="divSearchResults")
                # print(classes.findChildren())

                # TODO: extract info from the soup, info may not be accessible because of js

        except:
            majorMap[major] = "Error"

    print(majorMap)


# ********************************************************************************
# Scrape Course Descriptions

def descriptions_scrape():

    global driver, client, testing
    db = client.Scrape.Classes

    majors = []

    if testing:
        majors = ['Computer Science']
    else:
        # TODO: go through each dept in client.Metis.Departments
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
            driver.execute_script("arguments[0].click();", className[0])
            time.sleep(1)

        except:
            print("* " + major)

        # Get the default course set (usually Lower Divs come up first)
        extract_descriptions(major, "lower")
        time.sleep(1)
        extract_descriptions(major, "upper")
        time.sleep(1)
        extract_descriptions(major, "graduate")
        time.sleep(1)

    # index composite key of (department, number)
    index1 = IndexModel([("department", ASCENDING), ("number", ASCENDING)], name="ClassesIndex")
    db.create_indexes([index1])

def extract_descriptions(dept, type):
    """
    given a type: lower, upper, graduate
    put class objects in db with descriptions
    """

    global client
    mapping = client.Metis.MajorToAcronyms
    db = client.Scrape.Classes

    data = mapping.find_one({"major": dept})
    abbrevDept = data["acronym"]

    soup = getHTML("div", {"id": type})
    classes = soup.find_all("li", {"class": "media category-list-item"})

    for c in classes:
        course_data = c.find("h3").get_text()
        course_text = course_data.split('.')

        desc = ''
        for p in c.find_all("p"):
            if 'Units' not in p.get_text():
                p_tags = p.get_text().split('.')
                for text in p_tags:
                    if 'hour' not in text and 'grading' not in text and text != '':
                        desc += (text + '.')

        # TODO: include units and grading from 'p_tags'
        e = {
            "department": abbrevDept,
            "number": course_text[0],
            "name": course_text[1],
            "description": desc
        }

        db.insert_one(e)

# ********************************************************************************
# Scrape CCLE Descriptions

def ccle_scrape():
    """
    cycle through quarters in each year for each major
    """
    global client, testing
    mapping = client.Metis.MajorToAcronyms

    departments = []

    if testing:
        departments = [{'major': 'Computer Science', 'acronym': 'COM SCI'}]
    else:
        with open('major_list.json') as json_file:
            departments = json.load(json_file)["majors"]

        departments = list(mapping.find({}))

    quarterSymbols = ['W', 'S', '1', 'F']

    for dept in departments:

        try:
            major = dept["acronym"]

            # replace spaces with '%20'
            abbrev = major.replace(' ', '%20')

            # go through each quarter in a range of years
            for i in range(16,21):
                for q in quarterSymbols:
                    quarter = str(i) + q
                    ccle_professor_scraper(abbrev, quarter, major)
        except:
            print("No acronym for: " + dept)

def ccle_professor_scraper(abbrev, quarter, major):
    """
    major format: 'COM%20SCI', or 'AF%20AMER' etc.
    quarter format: '19F', '18W', etc.
    returns a list of (class id, professor, full class title) lists
    """
    global driver, client

    url = 'https://ccle.ucla.edu/blocks/ucla_browseby/view.php?term={}&type=course&subjarea={}'.format(quarter, abbrev)
    driver.get(url)

    page_source = driver.page_source
    ccle_professor_parser = CCLEHTMLParser()

    db = client.Scrape.ClassesByQuarter

    try:
        classes = ccle_professor_parser.get_class_professor_list(page_source)

        for c in classes:
            e = {
                "courseNum": c[0],
                "professor": c[1],
                "courseTitle": c[2],
                "major": major,
                "quarter": quarter
            }

            db.insert_one(e)
    except:
        print("CCLE doesn't have data for: " + major + " " + quarter)

# start the driver and return it
def setup_driver(testing):
    chrome_options = webdriver.ChromeOptions()

    if not testing:
        chrome_options.add_argument("--headless")
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
        driver = webdriver.Chrome(executable_path = './chromedrivers/chromedriver.exe', chrome_options=chrome_options)

    return driver

def main():

    global driver, client, testing

    if len(sys.argv) == 2 and sys.argv[1] == 'test':
        testing = True
        print("Testing scrapers for Computer Science, not headless mode")

    driver = setup_driver(testing)
    client = pymongo.MongoClient("mongodb+srv://tester:user@metis-eaoki.mongodb.net/test?retryWrites=true&w=majority")

    # Scrape the schedule of classes
    # sched_scrape()

    # Scrape Class Descriptions
    # descriptions_scrape()
    time.sleep(10)

    # Scrape Professors
    ccle_scrape()
    time.sleep(10)

    client.close()
    driver.close()


if __name__ == '__main__':
    main()
