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
        for term in myterms:  # here we append the geographic region name to append to the search
            for region in regionals:
                term_to_insert = term + " " + region
                new_terms.append(term_to_insert)

        self.myterms = new_terms
        self.driver = driver
        self.search_deep = search_deep
        self.random_range = random_range
        self.mypage = 1  # this is the page counter for the google search results
        self.pager = pager  # number of pages to check
        self.report = {}  # this is a container for the info we'll be logging
        today = datetime.datetime.today().strftime('%m-%d-%Y')
        today_string = "SEO report for " + self.url_to_look_for + " on " + str(today)
        self.report['test_date'] = [today_string]
        self.found_terms = []  # bucket for the terms that came up in a search
        self.not_found = []  # container for the terms that don't show up
        term_array_added = 0  # loop_counter

        while term_array_added < len(self.myterms):
            self.report[self.myterms[term_array_added]] = []  # add empty list to the larger report list
            term_array_added += 1

        print('new report:')
        print(self.report)

        for term in self.myterms:  # now loop through our terms and see where they appear
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

        with open(report_name, 'w+') as F:
            for term, term_list in self.report.items():
                if len(term_list) > 0:
                    F.write('\r\n')
                    F.write(term + ":")
                    F.write('\r\n')
                    F.write("-----------------------------------------------------------")
                    F.write('\r\n')
                for term_message in term_list:
                    F.write(term_message)
                    F.write('\r\n')

            print(self.report)

            if len(self.not_found) > 0:
                # now write the results that don't appear anywhere
                F.write(str(len(self.not_found)) + " terms not found in " + str(self.pager) + " pages:")
                F.write('\r\n')
                F.write("----------------------------------------------------------------")
                F.write('\r\n')
                for n in self.not_found:
                    F.write(n)
                    F.write('\r\n')

    def get_sleep_random(self):
        return randint(self.random_range[0], self.random_range[1])

    def sendthesearch(self, term):  # go ahead and type the search term into the google bar
        elem = self.driver.find_element_by_name("q")  # google search bar
        elem.clear()
        rand = self.get_sleep_random()
        time.sleep(rand)
        elem.send_keys(term)
        elem.send_keys(Keys.RETURN)
        rand = self.get_sleep_random()
        time.sleep(rand)

    def findsearchterm(self, term, found):  # we've sent the search term - now test the content for our target URL
        mycounter = int(0)  # basic counter to track the link position
        test_message = "Testing '" + term + "' at page " + str(self.mypage) + ":"
        print(test_message)

        try:
            div = self.driver.find_element_by_class_name(
                'srg')  # this is the elements that houses the links we're interested in
            for a in div.find_elements_by_xpath('.//a'):
                thislink = str(a.get_attribute('href'))
                if ('google.com' in thislink) | ('webcache.googleusercontent.com' in thislink):
                    continue
                else:
                    mycounter = mycounter + 1
                if self.url_to_look_for in thislink:
                    # showcounter = str(mycounter)
                    message = "Position " + str(mycounter) + " Page " + str(self.mypage) + " --------- " + thislink
                    print(message)
                    self.report[term].append(message)
                    self.found_terms.append(term)
                    found = found + 1
        finally:
            pass

        if self.mypage <= self.pager:
            if found < 1:
                no_results_message = 'no results for ' + term + " on page " + str(self.mypage)
                print(no_results_message)
            found = self.checknextpages(term, found)  # go into the following pages to test

        self.driver.back()
        rand = self.get_sleep_random()
        time.sleep(rand)
        return found

    # def test_if_in_array(self, term):
    #     print('checking this term:' + term)
    #     for iterma in self.report:
    #         for z in iterma:
    #             if isinstance(z, list):  # lets see if there's a list to access
    #                 print('inside term:')
    #                 print(z[2][0])
    #                 if term in z[2][0]:
    #                     return z[2][1]
    #     return None

    def checksubsequentpage(self, term, found):  # looks for search term on subsequent pages
        try:
            elem = self.driver.find_element_by_link_text(str(self.mypage))
            elem.click()
            rand = self.get_sleep_random()
            time.sleep(rand)
            found = self.findsearchterm(term, found)
            return found

        finally:
            return found

    def checknextpages(self, term, found):  # recursive function to drill into the pages for the search term
        if self.mypage < self.pager:
            self.mypage = self.mypage+1
            found = self.checksubsequentpage(term, found)
            self.checknextpages(term, found)
            return found
        elif self.mypage == self.pager:
            return 1
        else:
            return 1
