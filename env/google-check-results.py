from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome(executable_path=r'C:\selenium\chromedriver_win32\chromedriver.exe')
driver.get('http://www.google.com')

myterms = ['autism counseling in bothell', 'EMDR']

mycounter = int(0)
for term in myterms:
    elem = driver.find_element_by_name("q")
    time.sleep(1)
    elem.send_keys(term)
    elem.send_keys(Keys.RETURN)
    time.sleep(1)

    div = driver.find_element_by_class_name('srg')
    for a in div.find_elements_by_xpath('.//a'):
    #for a in driver.find_elements_by_xpath('.//a'):
        mycounter = mycounter + 1
        thisguy = str(a.get_attribute('href'))
        if 'http://counselinginbothell.com' in thisguy:
            showcounter = str(mycounter)
            print(thisguy + " at position " + showcounter)

    driver.back()
    time.sleep(3)