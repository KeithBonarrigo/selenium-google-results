from selenium import webdriver
from selenium.webdriver.common.by import By
from gsearch import *

driver = webdriver.Chrome(executable_path=r'C:\selenium\chromedriver_win32\chromedriver.exe')
driver.get('http://www.google.com') #open our URL
myterms = ['autism counseling in bothell', 'EMDR Bothell'] #our search terms - duh

g = gsearch(myterms, driver)




