from selenium import webdriver
from gsearch import *

driver = webdriver.Chrome(executable_path=r'C:\selenium\chromedriver_win32\chromedriver.exe')
driver.get('http://www.google.com')  # open our URL
myterms = [
    'EMDRIA certified',
    'PTSD',
    'psychologist',
    'EMDR',
    'EMDR Therapy',
    'EMDR Treatment',
    'EMDRIA',
    'Asperger Syndrome Screening for adults',
    'Autism spectrum screening for adults',
    'A.S.D. screening for adults',
    'counseling for autism ',
    'counseling for couples with a member on the spectrum',
    'anxiety and depression counseling',
    'developing accommodations for the workplace',
]  # our search terms
regionals = ['bothell', 'seattle', 'wa']

# myterms = [
#     'green go solar project',
#     'greengosolar.org'
# ] #our search terms
# regionals = ['mexico', 'brt ytrski']


random_range = [0, 3]
go_deep = 1  # flag to see if the search should drill deeper into subsequent pages after term is found
g = GoogleSearch(myterms, driver, 3, 'http://counselinginbothell.com', regionals, random_range, go_deep)
# g = GoogleSearch(myterms, driver, 2, 'http://greengosolar.org', regionals, random_range, go_deep)
