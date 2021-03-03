import sys
import re
import bs4 as bs
from HTMLParser import HTMLParser
import xlsxwriter
import os
from bs4 import BeautifulSoup
import requests
import time

def excelSheet():

    urls = 0
    i = 0
    urlGroup2 = ['']
    rotate = 26815
    rotate2 = 26816
    rotate3 = 26818
    urlGroup = [
        'http://www.crb.ri.gov/licensedetail.php?link=' + str(rotate) + '&type=Residential+Contractor',
        'http://www.crb.ri.gov/licensedetail.php?link=' + str(rotate2) + '&type=Residential+Contractor',
        'http://www.crb.ri.gov/licensedetail.php?link=' + str(rotate3) + '&type=Residential+Contractor'
     ]
    workbook = xlsxwriter.Workbook(os.path.join(os.path.dirname(os.path.abspath(__file__)),"srape.xlsx"))
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0
    i = 0
    length = len(urlGroup2)
    urls = 0
    while i < 400:
      url = ('http://www.crb.ri.gov/licensedetail.php?link=' + str(rotate) + '&type=Residential+Contractor')
      response = requests.get(url)
      data = response.text
      soup = bs.BeautifulSoup(data,'lxml')
      soupString = soup.h9.get_text()
      worksheet.write(row,col,soupString)
      time.sleep(3)
      row += 1
      i += 1
      rotate += 1

    workbook.close()

def main():
    headers = {
        "User-Agent" : "my test program. contact me at admin@domain.com"
    }
    excelSheet()


if __name__ == '__main__':
    main()
