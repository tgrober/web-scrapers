import requests
import urllib2
import re
from bs4 import BeautifulSoup
import xlwt
from xlwt import Workbook

wb = Workbook()

country_abb = {
                "PHILIPPINES":"PHL",
                "INDIA":"IND",
                "MEXICO":"MEX",
                "CHINA-mainland born":"CHN",
                "All Chargeability Areas Except Those Listed":"YYY"
}

country_list = [
                "PHILIPPINES",
                "INDIA",
                "MEXICO",
                "CHINA",
                "Chargeability",
]

def pull_visa_chart(url):
    #print(url)
    page = urllib2.urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    table_data = soup.find("table")
    #print(len(table_data))
    for i in range(5):
        print(table_data[i])

    return table_data

def check_country_format(string):
    if "CHINA" in string.upper():
        print("Found CHN")
        return "CHN"
    if "PHILIPPINES" in string.upper():
        print("Found PHL")
        return "PHL"
    if "INDIA" in string.upper():
        print("Found IND")
        return "IND"
    if "MEXICO" in string.upper():
        print("Found MEX")
        return "MEX"
    if "CHARGEABILITY" in string.upper():
        print("Found YYY")
        return "YYY"
    else:
        return string

def scrape_chart():
    wb = Workbook()

    # add_sheet is used to create sheet.
    sheet1 = wb.add_sheet('format-sheet')
    #url = "https://travel.state.gov/content/travel/en/legal/visa-law0/visa-bulletin/2021/visa-bulletin-for-december-2020.html"
    with open('visa-bulletin.html', 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')
        visa_table = soup.find("table")
        visa_table_data = visa_table.tbody.find_all("tr")

        col = 0
        r = 0
        for tr in visa_table_data:
            td = tr.find_all('td')
            row = [i.text for i in td]
            #sheet1.write(col,r, row)
            r = 0
            for cell in row:
                sheet1.write(col,r, check_country_format(cell))
                #sheet1.write(col,r, cell+ 'col: ' + str(col) + 'row: ' + str(r))
                r += 1

            col += 1

        wb.save('xlwt example.xls')

def scrape_multiple_chart():
    #wb = Workbook()
    # add_sheet is used to create sheet.
    chart1 = wb.add_sheet('chart1')
    col = 0
    r = 0
    index = 0
    skip_lines = [6,7,8,9,10]

    with open('visa-bulletin.html', 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')

        visa_table_full = soup.findAll("table")
        print(visa_table_full[5])
        for i in range(5):
            visa_table_full.pop(1)

        for table in visa_table_full:
            visa_table_data = table.tbody.find_all("tr")
            for tr in visa_table_data:
                td = tr.find_all('td')
                row = [i.text for i in td]
                r = 0
                for cell in row:
                    chart1.write(col,r, cell)
                    r += 1

                col += 1

            col += 1

        wb.save('xlwt example.xls')

def get_bulletin_title(url):
    #url = "https://travel.state.gov/content/travel/en/legal/visa-law0/visa-bulletin/2021/visa-bulletin-for-november-2020.html"
    page = urllib2.urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    title = soup.title
    print(title.string)
    return title.string

def scrape_web_chart(url):

    # add_sheet is used to create sheet.
    new_chart_title = get_bulletin_title(url)
    new_chart = wb.add_sheet(new_chart_title)
    col = 0
    r = 0
    index = 0
    skip_lines = [6,7,8,9,10]

    page = urllib2.urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    visa_table_full = soup.findAll("table")
    print(visa_table_full[5])
    for i in range(5):
        visa_table_full.pop(1)

    for table in visa_table_full:
        visa_table_data = table.tbody.find_all("tr")
        for tr in visa_table_data:
            td = tr.find_all('td')
            row = [i.text for i in td]
            r = 0
            for cell in row:
                #new_chart.write(col,r, cell)
                new_chart.write(col,r, check_country_format(cell))
                r += 1

            col += 1

        col += 1

    wb.save('xlwt example.xls')

def get_urls():
    url_list = [250]
    # add_sheet is used to create sheet.
    url_sheet = wb.add_sheet('URLs')
    #get soup object
    soup = get_soup_object()

    links = soup.find_all('a', adhocenable='false')
    col = 0
    row = 0
    print("size of links : " + str(len(links)))

    for link in links:
        url = "https://travel.state.gov" + link.get('href')
        url_sheet.write(col,row, url)
        url_list.append(url)
        #(url)
        col += 1

    return url_list
    wb.save('xlwt example.xls')

def get_soup_object():

    url = "https://travel.state.gov/content/travel/en/legal/visa-law0/visa-bulletin.html"
    page = urllib2.urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    return soup

if __name__ == "__main__":
    url = "https://travel.state.gov/content/travel/en/legal/visa-law0/visa-bulletin/2020/visa-bulletin-for-august-2020.html"
    url_list = get_urls()
    url_list_small = url_list[5:10]
    #for url in url_list_small:
#    print(url)
#        scrape_web_chart(url)
    scrape_web_chart(url)
    #scrape_chart()
    #scrape_multiple_chart()
    #get_bulletin_title(url)
