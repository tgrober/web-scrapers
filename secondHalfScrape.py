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

def scrapeGamecastURLs():
    teams = []
    url = "https://www.espn.com/mens-college-basketball/scoreboard/_/group/50"
    html_page = urllib2.urlopen(url)
    with open('scoreboard.html', 'r') as f:
    	contents = f.read()
    	soup = BeautifulSoup(contents, 'html.parser')
    	games = 0
    	gameURLs = []
    	gamecastURLs = soup.find_all("section", {"class" : "sb-actions"})
    	#print gamecastURLs
    	for line in gamecastURLs:
    		for link in line.find_all("a"):
    			gameURLs.append(link.get('href'))
    	#print gameURLs
    	for url in gameURLs:
    		if "game" in url and "boxscore" not in url and "playbyplay" not in url:
    			try:
    				scrapeGameInfoFromLink(url)
    				games += 1
    			except IndexError as error:
    				break
    	numberOfGames = len(gameURLs)
    	print str(games) + " : number of games active"
       	
def scrapeGameInfoFromLink(url):
	# print("Scraping info for " + url)
	html_page = urllib2.urlopen(url)
	test = "https://www.espn.com/mens-college-basketball/game?gameId=401280173"
	newTest = url.replace("game", "matchup", 1)
	
	#html_page2 = urllib2.urlopen("https://www.espn.com/mens-college-basketball/matchup?gameId=401280173")
	html_page2 = urllib2.urlopen(newTest)
	soup = BeautifulSoup(html_page, 'html.parser')
	soup2 = BeautifulSoup(html_page2, "html.parser")
	teamNames = soup.find_all("span", {"class" : "long-name"})
	team1Name = teamNames[0].text
	team2Name = teamNames[1].text
	print team1Name
	print team2Name
	print 
	teamStatsTable = soup2.find_all("tr", {"class" : "highlight"})
	gameTimeStatus = soup2.find_all("span", {"class" : "status-detail"})
	for line in gameTimeStatus:
		if "Final" in line.text.encode('ascii'):
			text = colored(line.text.encode('ascii'), 'red', 'on_blue')
			print text
		else:
			text = colored(line.text.encode('ascii'), 'red', 'on_yellow')
			print text
	# try:
		# Gets Shots taken field
	shotsTaken = teamStatsTable[2]
	shotsCleaned = filter(None, re.split(r"\-(\d+)", shotsTaken.text.encode('ascii')))
	print team1Name + " shots taken " + shotsCleaned[1]
	print team2Name + " shots taken " + shotsCleaned[3]
	print 
	team1ShotsTaken = shotsCleaned[1]
	team2ShotsTaken = shotsCleaned[3]

	# 3 point % is [3]
	threePoint = teamStatsTable[3]
	cleaned = filter(None, re.split(r"(\d+\.\d)", threePoint.text.encode('ascii')))
	team1ThreePointPercentage = cleaned[1]
	team2ThreePointPercentage = cleaned[3]
	print team1Name + " 3 point % " + team1ThreePointPercentage
	print team2Name + " 3 point % " + team2ThreePointPercentage
	print 

	if (float(team1ThreePointPercentage) >= 60.0 and int(team1ShotsTaken) >= 10 or float(team2ThreePointPercentage) >= 60.0 and int(team2ShotsTaken) <= 10):
		#print("THIS GAME COUNTS")
		text = colored("THIS GAME COUNTS ", 'green', 'on_blue')
		print text
	else:
		#print("THIS GAME DOESNT COUNT")
		text = colored("THIS GAME DOESNT COUNT ", 'red', 'on_green')
		print text
	# except IndexError as error:
	# 	return



if __name__ == "__main__":
    scrapeGamecastURLs()
	#checkGameStatus()