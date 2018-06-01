from selenium import webdriver
from selenium.webdriver.common.by import By
from gsearch import *

driver = webdriver.Chrome(executable_path=r'C:\selenium\chromedriver_win32\chromedriver.exe')
driver.get('http://www.google.com') #open our URL
myterms = [
    'Asperger Syndrome Screening for adults bothell wa',
    'Autism spectrum screening for adults wa',
    'Asperger Syndrome Screening for adults seattle',
    'Autism spectrum screening for adults bothell',
    'Autism spectrum screening for adults wa ',
    'Autism spectrum screening for adults seattle',
    'A.S.D. screening for adults wa',
    'A.S.D. screening for adults bothell wa',
    'A.S.D. screening for adults seattle',
    'counseling for autism wa',
    'counseling for autism bothell',
    'counseling for autism seattle',
    'counseling for couples with a member on the spectrum',
    'counseling for couples with a member on the spectrum wa',
    'counseling for couples with a member on the spectrum bothell',
    'anxiety and depression counseling wa',
    'anxiety and depression counseling bothell',
    'anxiety and depression counseling seattle',
    'developing accommodations for the workplace wa',
    'developing accommodations for the workplace bothell',
    'developing accommodations for the workplace seattle'
] #our search terms
g = GoogleSearch(myterms, driver)



