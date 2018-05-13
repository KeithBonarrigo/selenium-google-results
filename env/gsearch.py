import time
from selenium.webdriver.common.keys import Keys

class gsearch:
    def __init__(self, myterms, driver):
        self.myterms = myterms
        self.driver = driver
        self.mypage = 1

        for term in self.myterms:
            self.sendthesearch(term)
            self.findsearchterm(term)

    def sendthesearch(self,term):
        elem = self.driver.find_element_by_name("q")  # google search bar
        time.sleep(1)
        elem.send_keys(term)
        elem.send_keys(Keys.RETURN)
        time.sleep(1)
        print('go')

    def findsearchterm(self, term):
        mycounter = int(0)  # basic counter to track the link position
        self.mypage = 1  # this is the page counter for the google search results
        print("Testing " + term + ":")
        div = self.driver.find_element_by_class_name('srg')  # this is the elements that houses the links we're interested in
        found = 0  # track our link count to see if we need to move to the next page
        for a in div.find_elements_by_xpath('.//a'):
            thislink = str(a.get_attribute('href'))

            if ('google.com' in thislink) | ('webcache.googleusercontent.com' in thislink):
                # do nothing
                mycounter = mycounter
            else:
                mycounter = mycounter + 1
                showcounter = str(mycounter)
            if 'http://counselinginbothell.com' in thislink:
                showcounter = str(mycounter)
                print(thislink + " at position " + showcounter + " at page " + str(self.mypage))
                found = found + 1

        if found < 1:
            print('no results for ' + term + " on page " + str(self.mypage))
        else:
            self.driver.back()
            time.sleep(3)