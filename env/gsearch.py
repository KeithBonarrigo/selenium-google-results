import time
from selenium.webdriver.common.by import By
import datetime
from selenium.webdriver.common.keys import Keys
from random import randint

class GoogleSearch:
    def __init__(self, myterms, driver):
        self.myterms = myterms
        self.driver = driver
        self.mypage = 1 # this is the page counter for the google search results
        self.pager = 3
        self.report = []

        today = datetime.datetime.today().strftime('%m-%d-%Y')
        today_string = "SEO REPORT FOR " + str(today)
        #self.report.append("------------------------------------------------------------")

        self.report.append(today_string)
        for term in self.myterms:
            self.mypage = 1
            print("------------------------------------------------------------")
            self.sendthesearch(term)
            self.findsearchterm(term)
            print("------------------------------------------------------------")

        report_name = 'reportfile_' + str(today) + '.txt'
        F = open(report_name,'w+')
        for ireport in self.report:
            print(ireport)
            F.write(ireport)
            F.write('\r\n')

    def get_sleep_random(self, start, stop):
        return(randint(start, stop))

    def sendthesearch(self,term):
        elem = self.driver.find_element_by_name("q")  # google search bar
        elem.clear()
        rand = self.get_sleep_random(1, 4)
        time.sleep(rand)
        elem.send_keys(term)
        elem.send_keys(Keys.RETURN)
        rand = self.get_sleep_random(1, 4)
        time.sleep(rand)

    def findsearchterm(self, term):
        mycounter = int(0)  # basic counter to track the link position
        test_message = "Testing '" + term + "' at page " + str(self.mypage) + ":"
        print(test_message)
        self.report.append(test_message)
        div = self.driver.find_element_by_class_name('srg')  # this is the elements that houses the links we're interested in
        found = 0  # track our link count to see if we need to move to the next page
        for a in div.find_elements_by_xpath('.//a'):
            thislink = str(a.get_attribute('href'))
            if ('google.com' in thislink) | ('webcache.googleusercontent.com' in thislink):
                continue
            else:
                mycounter = mycounter + 1
                showcounter = str(mycounter)
            if 'http://counselinginbothell.com' in thislink:
                showcounter = str(mycounter)
                message = term + " found at position " + showcounter + " at page " + str(self.mypage) + " " + "(" + thislink + ")"
                print(thislink + " at position " + showcounter + " at page " + str(self.mypage))
                self.report.append(message)
                found = found + 1
        if found < 1 & self.mypage < self.pager:
            no_results_message = 'no results for ' + term + " on page " + str(self.mypage)
            print(no_results_message)
            self.report.append(no_results_message)
            found = self.checknextpages(term, found)
            if found == 0:
                self.report.append("No listings for '"+ term + "' in " + str(self.pager) + " pages")

        self.driver.back()
        rand = self.get_sleep_random(1, 4)
        time.sleep(rand)
        return found

    def checksubsequentpage(self, term):
        print("checking page "+ str(self.mypage))
        elem = self.driver.find_element_by_link_text(str(self.mypage))
        elem.click()
        rand = self.get_sleep_random(1, 4)
        time.sleep(rand)
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
