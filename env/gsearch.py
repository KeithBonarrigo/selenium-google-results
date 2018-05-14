import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class gsearch:
    def __init__(self, myterms, driver):
        self.myterms = myterms
        self.driver = driver
        self.mypage = 1 # this is the page counter for the google search results
        self.pager = 3
        self.report = []

        for term in self.myterms:
            self.mypage = 1
            print("------------------------------------------------------------")
            self.sendthesearch(term)
            self.findsearchterm(term)
            print("------------------------------------------------------------")

        for ireport in self.report:
            print(ireport)

    def sendthesearch(self,term):
        elem = self.driver.find_element_by_name("q")  # google search bar
        elem.clear()
        time.sleep(0)
        elem.send_keys(term)
        elem.send_keys(Keys.RETURN)
        time.sleep(0)

    def findsearchterm(self, term):
        mycounter = int(0)  # basic counter to track the link position
        print("Testing '" + term + "' at page " + str(self.mypage) + ":")
        div = self.driver.find_element_by_class_name('srg')  # this is the elements that houses the links we're interested in
        found = 0  # track our link count to see if we need to move to the next page
        for a in div.find_elements_by_xpath('.//a'):
            thislink = str(a.get_attribute('href'))
            if ('google.com' in thislink) | ('webcache.googleusercontent.com' in thislink):
                mycounter = mycounter #do nothing
            else:
                mycounter = mycounter + 1
                showcounter = str(mycounter)
            if 'http://counselinginbothell.com' in thislink:
                showcounter = str(mycounter)
                message = thislink + " at position " + showcounter + " at page " + str(self.mypage)
                print(thislink + " at position " + showcounter + " at page " + str(self.mypage))
                self.report.append(message)
                found = found + 1
        if found < 1 & self.mypage < self.pager:
            print('no results for ' + term + " on page " + str(self.mypage))
            found = self.checknextpages(term, found)
            if found == 0:
                self.report.append("No listings for '"+ term + "' in " + str(self.pager) + " pages")

        self.driver.back()
        time.sleep(1)
        return found

    def checksubsequentpage(self, term):
        print("checking page "+ str(self.mypage))
        elem = self.driver.find_element_by_link_text(str(self.mypage))
        elem.click()
        time.sleep(2)
        found = self.findsearchterm(term)
        if found == 1:
            return 1
        else:
            return 0


    def checknextpages(self, term, found):
        if self.mypage < self.pager:
            self.mypage = self.mypage+1
            self.checksubsequentpage(term)
            self.checknextpages(term, found)
            return 0
        elif self.mypage==self.pager:
            return 1
        else:
            return 1
        #self.driver.back()
