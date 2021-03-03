import requests
import urllib2
import re
from bs4 import BeautifulSoup
import xlwt
from xlwt import Workbook
from collections import defaultdict
from colorama import Fore, Back, Style
from termcolor import colored, cprint
import xlsxwriter
import csv

consensusOddsLink = "https://bookies.com/nba/consensus"

def scrapeConsensusOdds():

    teams = []

    with open('consensusodds.html', 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')
        full_table = soup.find("div", {"class" : "event-item-container"})
        team_table_single = soup.find("div", {"class" : "event-item__field event-item__competitors"})
        team_table_full = soup.find_all("div", {"class" : "event-item__field event-item__competitors"})
        odds_table_single = soup.find("div", {"class" : "event-item__field event-item__market"})
        odds_table_full = soup.find_all("div", {"class" : "event-item__field event-item__market"})
        #for line in odds_table_single:
        #    print(line.text.encode('ascii'))
        #print(odds_table_single.text)
        first = odds_table_full[0].text.strip()
        second = odds_table_full[1].text.strip()
        third = odds_table_full[2].text.strip()
        fourth = odds_table_full[3].text.strip()
        #for line in team_table_single:
        #print(team_table_single.text)
        team_cleaned = []
        team = filter(None, re.split(r"\s(\@?\D\D\D)\s", team_table_single.text.encode('ascii')))
        for t in team:
            #print(len(t))
            if len(t) == 4 or len(t) == 3:
                team_cleaned.append(t)
        print(team_cleaned)
        #print(third)
        #print(fourth)
        #full = full_table.find_all("div", {"style" : "width:40%"})
        #team_names_table = full[0]
        #team_names_formatted = []
        team_table_cleaned = team_table_single.find_all("div", {"class" : "team-item__competitor"})
        
        #print(team_table_cleaned[0].text.encode('ascii')) # this is first team 
        #print(team_table_cleaned[1].text.encode('ascii')) # this is second team 
       

def new_scrape_bets():
    odds = defaultdict(dict)
    odds['Team']['Spread'] = ''
    odds['Team']['Total'] = ''
    odds['Team']['ML'] = ''
    odds['Team']['Opponet'] = ''
    

    team_names = []
    with open('odds.html', 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')
        full_table = soup.find("div", {"class" : "sportsbook-table__body"})
        full = full_table.find_all("div", {"style" : "width:40%"})
        team_names_table = full[0]
        team_names_formatted = []
        for line in team_names_table:
            team = re.split(r"\d+\W\d+[APM]{2}(.+)", line.text.encode('ascii'))
            print(team[1])
            team_names_formatted.append(team[1])

        new = full_table.find_all("div", {"style" : "width:20%"})
        spreads = new[0]
        totals = new[1]
        ml = new[2]
        spread_formatted = []
        total_formatted = []
        ml_formatted = []



        print("SPREADS")
        for line in spreads:
            if line == '':
                spread_formatted.append("BLANK")
                print("BLANK")
            else:
                spread = filter(None, re.split(r"([\+|\-]\d\.?\d+)", line.text.encode('ascii')))
                spread_formatted.append(spread)

        print("TOTALS")
        for line in totals:
            temp = []
            if line == '':
                total_formatted.append("BLANK")
                print("BLANK")
            else:
                #print(line.text)
                total = filter(None, re.split(r"(O\W\d+\.?\d?|U\W\d+\.?\d?)(\+|-\d+)", line.text))
                temp.append(total[0].encode('ascii', 'ignore'))
                temp.append(total[1].encode('ascii', 'ignore'))
                total_formatted.append(temp)

        print(total_formatted)
        print("ML")
        for line in ml:
            if line.text == '':
                ml_formatted.append("BLANK")
                print("BLANK")
            else:
                print(line.text)
                ml_formatted.append(line.text.encode('ascii'))

        print("team size : " + str(len(team_names_formatted)))
        print("Spread size : " + str(len(spread_formatted)))
        print("total size : " + str(len(total_formatted)))
        print("ml size : " + str(len(ml_formatted)))

        for index, team in enumerate(team_names_formatted):
            print(index , team )
            odds[team]['Spread'] = spread_formatted[index]
            odds[team]['Total'] = total_formatted[index]
            odds[team]['ML'] = ml_formatted[index]
        i = 0 
        for _ in range(len(team_names_formatted) / 2):
            print("index : " + str(index))
            try:
                odds[team_names_formatted[i]]['Opponent'] = team_names_formatted[i+1]
                
            except: 
                print("All good")
            i += 2
        i = 1 
        for _ in range(len(team_names_formatted) / 2):
            print("index : " + str(index))
            try:
                odds[team_names_formatted[i]]['Opponent'] = team_names_formatted[i-1]
                
            except: 
                print("All good")
            i += 2

        del(odds['Team'])
        write_bets_to_excel(odds)
        #print2DArr(odds)

def write_bets_to_excel(odds):
    print(odds)


    workbook = xlsxwriter.Workbook('hello.xlsx')
    worksheet = workbook.add_worksheet()
    w = csv.writer(open('output.csv', 'w'))
    row = 0
    col = 0
    '''
    for team_id, team_info in odds.items():
        row = 0
        worksheet.write(row,col, team_id)
        for key in team_info:
            worksheet.write(row,col,team_info[key][0])
            row += 1
        col += 1
    '''
    for key, val in odds.items():
        #w.writerow([key, val])
        for line in val:
            w.writerow([key,val[line]])
    #worksheet.write('A1', 'Hello world')

    workbook.close()

def scrape_bets():
    wb = Workbook()

    # add_sheet is used to create sheet.
    sheet1 = wb.add_sheet('bet-sheet')
    #url = "https://travel.state.gov/content/travel/en/legal/visa-law0/visa-bulletin/2021/visa-bulletin-for-december-2020.html"
    d = defaultdict(dict)
    d['team']['OpeningLine'] = ''
    d['team']['LiveLine'] = ''
    d['team']['Movement'] = ''
    d['team']['HighestLine'] = ''
    d['team']['LowestLine'] = ''
    d['team']['Opponent']= ''
    d['team']['NumberOfLines']=''
    d['team']['test']=''
    team_names = []
    with open('odds.html', 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')
        topteam_spread_and_price_array = soup.find_all("div", {"class" : "op-first-row"})
        bottomteam_spread_and_price_array = soup.find_all("div", {"class" : "op-second-row"})
        additional_lines = soup.find_all("div", {"class" : "op-item-wrapper no-vegas"})
        full_row = soup.find_all("div", {"class" : "op-item-row-wrapper not-futures"})
        for element in soup.find_all("div" , {"class" : "op-matchup-team-wrapper"}):
            for name in element.find_all("div"):
                text = name["data-op-name"].encode('ascii')
                match = re.split(r"\"(\w+\W?\w+)\"{,4}", text)
                if match[3] == "Texas":
                    print(text)
                    print(match)
                team_names.append(match[3])
    # Holds number of teams - 66 today
    numberOfTeams = len(team_names)
    print("NUMBER OF TEAMS " + str(numberOfTeams))
    print(len(full_row))
    print(len(team_names))
    numberOfLinesForTeam = 0
    size = 0
    i = 0
    for index in range(len(full_row)-1):
        size = 0
        for line in full_row[i]:
            #print("LINE : " + str(size) + " " + str(line.text))
            if(line.text != ''):
                size +=1
        d[team_names[i*2]]['NumberOfLines'] = size
        d[team_names[i*2+1]]['NumberOfLines'] = size
        print("team name " + team_names[i*2])
        print("team name " + team_names[i*2+1])
        #print("size " + str(size))
        #print("i " + str(i))
        #print("index " + str(index))
        i += 1
        #size = 0

    #print2DArrPretty(d);
    print(len(topteam_spread_and_price_array))
    size = 0
    i = 0
    topTeamArray = []
    bottomTeamArray = []
    #print(type(d[team_names[0]]['NumberOfLines']))
    for line in topteam_spread_and_price_array:
        if line.text != '':
            temp = matchup = filter(None, re.split(r"([\+|\-]\d{,3}\.?\d)", str(line.text)))
            topTeamArray.append(temp)

    for line in bottomteam_spread_and_price_array:
        if line.text != '':
            temp = matchup = filter(None, re.split(r"([\+|\-]\d{,3}\.?\d)", str(line.text)))
            bottomTeamArray.append(temp)
            #print(temp)
    i = 0

    for line in topTeamArray:
        print("line new : " + str(line))
        for index in range(d[team_names[i]]['NumberOfLines']):
            d[team_names[i]]['test'] = line
            print("index new : " + str(index))
            print("line second : " + str(line))

    # filling up team lines array -> full row len is 44
    i = 0
    j = 0
    k = 0
    #print2DArr(d)
    '''
    for index in range(len(team_names)):
        print(k + d[team_names[i]]['NumberOfLines'])
        k = k + d[team_names[i]]['NumberOfLines']
        print("Team Name: " + team_names[i] + "  " + str(d[team_names[i]]['NumberOfLines']))
        print("i : " +  str(i))
        d[team_names[i]]['test'] = topTeamArray[j:k]
        print(d[team_names[i]]['test'])
        print("k : " +  str(k))
        j = k
        i = i + 2
    '''
    # filling up team lines array -> full row len is 44
    i = 1
    j = 0
    k = 0
    '''
    #print(d[team_names[1]]['NumberOfLines'])
    for index in range(len(team_names)):
        k = k + d[team_names[i]]['NumberOfLines']
        print("Team Name: " + team_names[i] + "  " + str(d[team_names[i]]['NumberOfLines']))
        print("i : " +  str(i))
        #d[team_names[i]]['test'] = topteamArray[0:7]
        d[team_names[i]]['test'] = topteamArray[j:k]
        print(d[team_names[i]]['test'])
        j = k
        i = i + 2
    '''

    team_names = filter(None,team_names)
    lines = {}
    matchupSpreads = []
    emptyMatchups  = []
    fullMatchups = []
    i = 0
    j = 0
    for line in full_row:
            line = str(line.text)
            matchup = filter(None, re.split(r"([\+|\-]\d{,3}\.?\d)", string = line))
            if not matchup:
                emptyMatchups.append(i)
            else:
                fullMatchups.append(i)
            i += 1
            it = iter(matchup)
            for cost in it:
                if cost == 'Ev':
                    matchupSpreads.append([0 , next(it)])
                else:
                    matchupSpreads.append([cost , next(it)])
                j += 1

    opening_lines = []
    #print(fullMatchups)
    i = 0
    for index in matchupSpreads:
        #print("index : " + str(i) + str(index))
        i += 1

    # matchup spread go from 0 - 15 for first one
    # team_names[0] = matchupSpread[0:15:2]
    # team_names[1] = matchupSpread[1:15:2]
    #d[team_names[2]]['openingSpread'] = matchupSpreads[0]
    #d[team_names[3]]['openingSpread'] = matchupSpreads[1]
    #d[team_names[8]]['openingSpread'] = matchupSpreads[16]
    #d[team_names[9]]['openingSpread'] = matchupSpreads[17]

    # 1 4 5 6 7 .... are full matchups so each matchup has 2 teams that are empty
    # matchup[1] -> team_name[2, 3]
    # matchup[4] -> team_name[8, 9]
    # matchup[5] -> team_name[10, 11]

    i = 0 # index for opening spread
    j = 2 # index for spread now
    for index in fullMatchups:
        #print(fullMatchups)
        #print(index)
        #print(i)
        #print(team_names[index*2])
        #print(team_names[index*2 + 1])
        #print(matchupSpreads[i*16])
        #print(matchupSpreads[i*16 + 1])
        d[team_names[index*2]]['OpeningLine'] = matchupSpreads[i*16]
        d[team_names[index*2+1]]['OpeningLine'] = matchupSpreads[i*16+1]
        d[team_names[index*2]]['LiveLine'] = matchupSpreads[i*16+2]
        d[team_names[index*2+1]]['LiveLine'] = matchupSpreads[i*16+3]
        openLine1 = float(d[team_names[index*2]]['OpeningLine'][0])
        live1 = float(d[team_names[index*2]]['LiveLine'][0])
        change1 = (openLine1 - live1)
        openLine2 = float(d[team_names[index*2+1]]['OpeningLine'][0])
        live2 = float(d[team_names[index*2+1]]['LiveLine'][0])
        change2 = (openLine2 - live2)
        d[team_names[index*2]]['Movement'] = change1
        d[team_names[index*2+1]]['Movement'] = change2
        i += 1

    i = 0 # index for opening spread
    j = 2 # index for spread now
    highArray = []
    lowArray = []
    currentArrary = []
    for index in fullMatchups:
        #print(fullMatchups)
        #print(index)
        #print(i)
        j = 2
        low = 100
        high = 0
        print("FLOAT" + str(float(matchupSpreads[i*16+j][0])))
        for spread in range(14):
            #print(spread)
            #print(matchupSpreads[i*16+j])
            lowComp = abs(float(matchupSpreads[i*16+j][0]))
            highComp = abs(float(matchupSpreads[i*16+j][0]))
            if lowComp < low:
                low = lowComp
            if highComp > high:
                high = highComp

            j += 1
        i += 1
        d[team_names[index*2]]['HighestLine'] = high
        d[team_names[index*2+1]]['HighestLine'] = high
        d[team_names[index*2]]['LowestLine'] = low
        d[team_names[index*2+1]]['LowestLine'] = low
        d[team_names[index*2]]['Opponent'] = team_names[index*2+1]
        d[team_names[index*2+1]]['Opponent'] = team_names[index*2]
        highArray.append(high)
        lowArray.append(low)
    print(highArray)
    print(lowArray)


    '''
    for index in emptyMatchups:
        #print(index)
        #print(team_names[index*2])
        #print(team_names[index*2 + 1])
        d[team_names[index*2]]['openingSpread'] = 'NO game'
        d[team_names[index*2]]['additionalLines'] = 'NO game'
        d[team_names[index*2]]['spread'] = 'NO game'
        d[team_names[index*2]]['totalodds'] = 'NO game'
        d[team_names[index*2+1]]['openingSpread'] = 'NO game'
        d[team_names[index*2+1]]['additionalLines'] = 'NO game'
        d[team_names[index*2+1]]['spread'] = 'NO game'
        d[team_names[index*2+1]]['totalodds'] = 'NO game'
    '''
    # 0 2 3 11 15 are empty matchups so each matchup has 2 teams that are empty
    # matchup[0] -> team_name[0, 1]
    # matchup[2] -> team_name[4, 5]
    # matchup[3] -> team_name[6, 7]

    toparr = []
    botarr = []
    addLinesArr = []
    addLinesArr2 = []

    del(d['team'])
    #print2DArrPretty(d)
    '''
    # find highest and lowest number of each line from matchupSpreads[0:15] is first time
    highArray = []
    lowArray = []
    currentArrary = []
    print("total # of mathcups" + str(len(fullMatchups)))
    i = 0
    j = 3
    #print("total # of spreads " + str(len(fullMatchups)))
    for index in fullMatchups:
        print("index : " + str(index) + "  i : " + str(i))
        highArray[i] = matchupSpreads[i*16+2]
        for spread in range(11):
            print("spread : " + str(spread) + "  j : " + str(j))
            if matchupSpreads[i*16+j] > highArray[i]:
                highArray[i] = matchupSpreads[i*16+j]
            j += 1
        i += 1

    print(highArray)
    openLine1 = float(d[team_names[index*2]]['openingLine'][0])
    live1 = float(d[team_names[index*2]]['liveLine'][0])
    change1 = (openLine1 - live1)
    '''

def printArrWithIndex(array, indexLimit):
    i = 0
    for _ in range(indexLimit):
        print(array[i].text)
        i += 1

def print2DArrPretty(array):
    for team_id, team_info in array.items():
        text = colored("Team Name: " + team_id, 'green', attrs=['bold', 'blink','underline'])
        print(text)

        for key in team_info:
            if key == "NumberOfLines" and team_info[key]:
                text = colored("Number of Lines: "  + str(team_info[key]), 'red', 'on_blue')
                print(text)
                if key == "Movement":
                    text = colored("Movement: "  + str(team_info[key]), 'blue', 'on_yellow')
                    print(text)
                if key == "Opponent":
                    text = colored("Opponent: "  + str(team_info[key]), 'red')
                    print(text)
                if key != 'Movement' and key != 'Opponent':
                    print("{}: {}".format(key, team_info[key]))

        print "\n"

def print2DArr(array):
    for team_id, team_info in array.items():
        print("\n")
        print("Team name:", team_id)

        for key in team_info:
            print(key + ':', team_info[key])

if __name__ == "__main__":
    scrapeConsensusOdds()
