from selenium import webdriver
from selenium.webdriver.common.by import By
from gsearch import *

driver = webdriver.Chrome(executable_path=r'C:\selenium\chromedriver_win32\chromedriver.exe')
driver.get('http://www.google.com') #open our URL
myterms = [
    'EMDRIA certified',
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
] #our search terms
regionals = ['bothell', 'seattle', 'wa']
random_range = [0,15]
go_deep = 0
g = GoogleSearch(myterms, driver, 4, 'http://counselinginbothell.com', regionals, random_range, go_deep)



