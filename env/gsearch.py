import time
from selenium.webdriver.common.by import By
import datetime
from selenium.webdriver.common.keys import Keys
from random import randint
from operator import itemgetter

class GoogleSearch:
    def __init__(self, myterms, driver, pager, url, regionals, random_range, search_deep):
        self.url_to_look_for = url
        new_terms = []
        for term in myterms:
            for region in regionals:
                term_to_insert = term + " " + region
                new_terms.append(term_to_insert)

        self.myterms = new_terms
        self.driver = driver
        self.search_deep = search_deep
        self.random_range = random_range
        self.mypage = 1 # this is the page counter for the google search results
        self.pager = pager #number of pages to check
        self.report = [] #this is a container for the info we'll be logging
        self.report.append("") #set up our title slot for the report
        today = datetime.datetime.today().strftime('%m-%d-%Y')
        today_string = "SEO report for " + self.url_to_look_for + " on " + str(today)
        self.report[0] = today_string
        self.found_terms = []
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
            found = 0
            found = self.findsearchterm(term, found)
            print("return " + str(found))
            if term not in self.found_terms:
                if term not in self.not_found:
                    print("adding not found " + term)
                    self.not_found.append(term)
            print("------------------------------------------------------------")

        report_name = 'reportfile_' + str(today) + '.txt'
        F = open(report_name,'w+')
        counter = 0
        F.write(today_string) #write the title
        F.write('\r\n')
        F.write('\r\n')

        F.write("Terms tested:")
        F.write('\r\n')
        for term in self.myterms:
            F.write(term)
            F.write('\r\n')

        for ireport in self.report: #now write the results that showed up
            if counter > 0:
                F.write("Terms appearing on page " + str(counter) + ":")
                F.write('\r\n')
                F.write("----------------------------------------------------------------")
                F.write('\r\n')
                ireport.sort(key=itemgetter(1))
                for line in ireport:
                    F.write(line[0])
                    F.write('\r\n')
                F.write('\r\n')
            counter += 1

        if(len(self.not_found) > 0):
            F.write(str(len(self.not_found)) + " terms not found in " + str(self.pager) + " pages:") #now write the results that don't appear
            F.write('\r\n')
            F.write("----------------------------------------------------------------")
            F.write('\r\n')
            for n in self.not_found:
                F.write(n)
                F.write('\r\n')

        F.close()

    def get_sleep_random(self):
        return(randint(self.random_range[0], self.random_range[1]))

    def sendthesearch(self,term):
        elem = self.driver.find_element_by_name("q")  # google search bar
        elem.clear()
        rand = self.get_sleep_random()
        time.sleep(rand)
        elem.send_keys(term)
        elem.send_keys(Keys.RETURN)
        rand = self.get_sleep_random()
        time.sleep(rand)

    def findsearchterm(self, term, found):
        mycounter = int(0)  # basic counter to track the link position
        test_message = "Testing '" + term + "' at page " + str(self.mypage) + ":"
        print(test_message)

        div = self.driver.find_element_by_class_name('srg')  # this is the elements that houses the links we're interested in
        #found = 0  # track our link count to see if we need to move to the next page
        for a in div.find_elements_by_xpath('.//a'):
            thislink = str(a.get_attribute('href'))
            if ('google.com' in thislink) | ('webcache.googleusercontent.com' in thislink):
                continue
            else:
                mycounter = mycounter + 1
            if self.url_to_look_for in thislink:
                showcounter = str(mycounter)
                message = "\"" + term + "\"" + " --------- position " + showcounter + " --------- " + thislink
                print(message)
                info_to_append = [message, showcounter]
                self.report[self.mypage].append(info_to_append)
                self.found_terms.append(term)
                found = found + 1

        #print(" found is " + str(found) + " comparing " + str(self.mypage) + " and " + str(self.pager))
        if found < 1 & (self.mypage <= self.pager):
            no_results_message = 'no results for ' + term + " on page " + str(self.mypage)
            print(no_results_message)
            #self.report.append(no_results_message)
            found = self.checknextpages(term, found)

        self.driver.back()
        rand = self.get_sleep_random()
        time.sleep(rand)
        #print("find func returning " + str(found))
        return found

    def checksubsequentpage(self, term, found):
        #print("inside checksubsequentpage found is " + str(found))
        #print("checking page "+ str(self.mypage))
        if(found < 1):
            elem = self.driver.find_element_by_link_text(str(self.mypage))
            elem.click()
            rand = self.get_sleep_random()
            time.sleep(rand)
            found = self.findsearchterm(term, found)
            return found
        else:
            return 1
        #print("inside checksubsequentpage 2 found is " + str(found))



    def checknextpages(self, term, found):
        #print("inside checknextpages found is " + str(found))

        if self.mypage < self.pager:
            #print('found is ' + str(found))
            self.mypage = self.mypage+1
            found = self.checksubsequentpage(term, found)
            self.checknextpages(term, found)
            return found
        elif self.mypage==self.pager:
            return 1
        else:
            return 1
        #self.driver.back()
