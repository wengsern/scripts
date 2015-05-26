#!/usr/bin/env python

#################################################################
#  Auto log in to Google services via iceweasel using selenium  #
#################################################################

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
import sys

# load iceweasel profile
binary = FirefoxBinary('/usr/bin/firefox')
profile = webdriver.FirefoxProfile('/etc/iceweasel/profile')

# load iceweasel
driver = webdriver.Firefox(firefox_binary=binary, firefox_profile=profile)
driver.implicitly_wait(20)

# go to Google accounts login page
driver.get("https://accounts.google.com/ServiceLogin?hl=en&continue=https://www.google.com.au/%3Fgws_rd%3Dssl")

# insert login details
driver.find_element_by_tag_name("body").send_keys(Keys.F11)
driver.find_element_by_id("Email").send_keys("email@domain")
driver.find_element_by_id("Passwd").send_keys("myPassword")

# check "stay logged in" tickbox
if driver.find_element_by_id("PersistentCookie").get_attribute("checked") is None:
  driver.find_element_by_id("PersistentCookie").click()

# click on "signIn" button
driver.find_element_by_id("signIn").click()
driver.implicitly_wait(20)

# load page that requires Google login
driver.get("https://mail.google.com")
