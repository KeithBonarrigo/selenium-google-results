import time
from selenium.webdriver.common.by import By
import datetime
from selenium.webdriver.common.keys import Keys
from random import randint

class GoogleSearch:
    def __init__(self, myterms, driver, pager, url):
        self.url_to_look_for = url
        self.myterms = myterms
        self.driver = driver
        self.mypage = 1 # this is the page counter for the google search results
        self.pager = pager #number of pages to check
        self.report = [] #this is a container for the info we'll be logging
        self.report.append("") #set up our title slot for the report
        today = datetime.datetime.today().strftime('%m-%d-%Y')
        today_string = "SEO report for " + self.url_to_look_for + " on " + str(today)
        self.report[0] = today_string
        self.not_found = [] #container for the terms that don't show up

        page_array_added = 0 #loop_counter
        while page_array_added < self.pager:
            list_to_insert = [] #set up and empty container
            self.report.append(list_to_insert ) #add it to the larger report list
            page_array_added += 1

        #print(self.report)

        for term in self.myterms: #now loop through our terms and see where they appear
            self.mypage = 1
            print("------------------------------------------------------------")
            self.sendthesearch(term)
            self.findsearchterm(term)
            print("------------------------------------------------------------")

        report_name = 'reportfile_' + str(today) + '.txt'
        F = open(report_name,'w+')

        counter = 0
        F.write(today_string) #write the title
        F.write('\r\n')
        F.write('\r\n')

        for ireport in self.report: #now write the results that showed up
            if counter > 0:
                F.write("Terms appearing on page " + str(counter) + ":")
                F.write('\r\n')
                F.write("----------------------------------------------------------------")
                F.write('\r\n')
                for line in ireport:
                    F.write(line)
                    F.write('\r\n')
                F.write('\r\n')
            counter += 1

        F.write(str(len(self.not_found)) + " terms not found in " + str(self.pager) + " pages:") #now write the results that don't appear
        F.write("----------------------------------------------------------------")
        F.write('\r\n')
        for n in self.not_found:
            F.write(n)
            F.write('\r\n')

        F.close()

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
        #print('report is ' + str(len(self.report)) + "long")
        #print(self.report)

        if len(self.report)<self.mypage:
            print('creating ' + str(self.mypage))
            push_list = []
            #self.report.append.push_list

        div = self.driver.find_element_by_class_name('srg')  # this is the elements that houses the links we're interested in
        found = 0  # track our link count to see if we need to move to the next page
        for a in div.find_elements_by_xpath('.//a'):
            thislink = str(a.get_attribute('href'))
            if ('google.com' in thislink) | ('webcache.googleusercontent.com' in thislink):
                continue
            else:
                mycounter = mycounter + 1
            if self.url_to_look_for in thislink:
                showcounter = str(mycounter)
                message = "\"" + term + "\"" + " ---------------- found at position " + showcounter + " " + "(" + thislink + ")"
                print(message)
                self.report[self.mypage].append(message)
                found = found + 1
        if found < 1 & self.mypage < self.pager:
            no_results_message = 'no results for ' + term + " on page " + str(self.mypage)
            print(no_results_message)
            #self.report.append(no_results_message)
            found = self.checknextpages(term, found)
            if found == 0:
                self.not_found.append(term)

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
