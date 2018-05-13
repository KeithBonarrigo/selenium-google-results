from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
driver = webdriver.Chrome(executable_path=r'C:\selenium\chromedriver_win32\chromedriver.exe')
driver.get('http://www.google.com') #open our URL

myterms = ['autism counseling in bothell', 'EMDR Bothell'] #our search terms - duh

for term in myterms:
    mycounter = int(0)  # basic counter to track the link position
    mypage = 1  # this is the page counter for the google search results
    elem = driver.find_element_by_name("q") #google search bar
    time.sleep(1)
    elem.send_keys(term)
    elem.send_keys(Keys.RETURN)
    time.sleep(1)

    print("Testing " + term + ":")
    div = driver.find_element_by_class_name('srg') #this is the elements that houses the links we're interested in
    found = 0 #track our link count to see if we need to move to the next page
    for a in div.find_elements_by_xpath('.//a'):
        thislink = str(a.get_attribute('href'))

        if ('google.com' in thislink) | ('webcache.googleusercontent.com' in thislink):
            #do nothing
            mycounter = mycounter
        else:
            mycounter = mycounter + 1
            showcounter = str(mycounter)

        if 'http://counselinginbothell.com' in thislink:
            showcounter = str(mycounter)
            print(thislink + " at position " + showcounter + " at page " + str(mypage))
            found = found + 1

    if found < 1:
        print('no results for ' + term + " on page " + str(mypage))

    driver.back()
    time.sleep(3)