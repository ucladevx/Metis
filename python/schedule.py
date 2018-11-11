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

# return HTML 
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

def sched_scrape():
	global driver

	majors = ["African Studies", "African American Studies"]

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
		for s in state:						# only one of the returned elements is clickable, not sure which one
			driver.execute_script("arguments[0].click()", s)
		driver.execute_script("arguments[0].click();", state[1])

		# Click the go button
		go = check_exists_by_xpath("""//*[@id="btn_go"]""", driver)
		time.sleep(1)
		go.click()
		time.sleep(1)

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


# TODO: parse HTML that is output
def descriptions_scrape():
	global driver

	# TODO: get all major names in a file and read from that
	# majors = ["Aerospace Studies", "African American Studies", "African Studies"]
	majors = ["Aerospace Studies", "African American Studies"]


	for major in majors:
		url = "https://www.registrar.ucla.edu/Academics/Course-Descriptions"
		driver.get(url)

		# click on dropdown input
		className = driver.find_elements_by_xpath("//*[contains(text(), '" + major + "')]")
		time.sleep(1)
		print(className)
		driver.execute_script("arguments[0].click();", className[0])
		time.sleep(1)

		# Get the current page's HTML
		page_response = requests.get(driver.current_url, timeout=5)

		
		# Create a soup
		soup = BeautifulSoup(page_response.content, "html.parser")
		classes = soup.find("ul", {"class": "media-list category-list"})
		print("********************")
		# TODO: parse this
		print(classes.findChildren())
		print("********************")

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


# start the driver and return it
def setup_driver():
	chrome_options = webdriver.ChromeOptions()
	# chrome_options.add_argument("--headless")
	chrome_options.add_argument("--start-maximized")
	prefs = {"profile.default_content_setting_values.notifications" : 2}
	chrome_options.add_experimental_option("prefs",prefs)

	print("Starting driver")
	driver = webdriver.Chrome(executable_path = './chromedriver', chrome_options=chrome_options)

	return driver

def main():

	global driver

	driver = setup_driver()

	# Scrape the schedule of classes
	# sched_scrape()

	# Scrape Class Descriptions
	descriptions_scrape()

	# Scrape course descriptions
	# descriptions_scrape()

	time.sleep(10)

	# driver.close()

if __name__ == '__main__':
	main()
