import sys
import re
import bs4 as bs
from html.parser import HTMLParser
import xlsxwriter
import os
from bs4 import BeautifulSoup
import requests
import time

url ='https://www.google.com/search?hl=en&as_q=&as_epq=created+by+wix&as_oq=landscaping+or+roofing+or+contractor+&as_eq=&as_nlo=&as_nhi=&lr=&cr=&as_qdr=all&as_sitesearch=.wix&as_occt=any&safe=images&as_filetype=&as_rights='
response = requests.get(url)
#print (response)
data = response
#print (data)
soup = bs.BeautifulSoup(data,'html')

for string in soup.stripped_strings:
    print(repr(string))
#print (string)
#print (soup.get_text())
print (type(soup))




#<h3 class="sA5rQ">Roofing and More | High Quality Roofing Experts‎</h3>
