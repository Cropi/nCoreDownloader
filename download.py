#!/usr/bin/python3

import settings
import requests
import sys
import time
import os
import time

payload = { 'nev':  settings.nCoreData['username'], 'pass': settings.nCoreData['password'] }

urlLogin = 'https://ncore.cc/login.php'
urlDownload = 'https://ncore.cc/torrents.php'
nCoreAuthentiactionKey='de18220df95a15a7e403ea080290c26c'

def checkDirectory():
	if not os.path.isdir('./torrents'):
		os.makedirs('./torrents')

def displayInfo(info):
	sys.stdout.write(time.strftime("%H:%M:%S  "))
	print(info)

def searchItems():
	file=open("searchList", "r").readlines()
	array=[]
	for f in file:
		f=f.replace('\n', '')
		array.append(f)
	return array

def makeID(ID):
	return 'https://ncore.cc/torrents.php?action=download&id=' + ID + '&key=' + nCoreAuthentiactionKey



def downloadItems(actualData):
		displayInfo("START")
		with requests.Session() as page:
			loginPage = page.post(urlLogin, data=payload)
			downloadPage=page.get(urlDownload)
			searchedDataUnordered = page.post(urlDownload, data=actualData)
			words = searchedDataUnordered.content.split()
			idList= []
			for word in words:
				if word.find('onclick="torren') == 0:
					idList.append(word)
			count = 0
			if not idList:
				displayInfo("No files are available for name: "+actualData['mire'])
			else :
				displayInfo(str(len(idList)) +" file(s) are being downloaded for name: " + actualData['mire'])
			for i in idList:
				idList[count] = idList[count].replace('onclick="torrent(', '')
				idList[count] = idList[count].replace(');', '')
				nameOfTorrent="torrents/"+idList[count]+".torrent"
				if os.path.isfile(nameOfTorrent):
					displayInfo("Skip torrent: "+nameOfTorrent)
					count += 1
					continue
				idList[count] = makeID(idList[count])
				fileToDownload = requests.get(idList[count], allow_redirects=True)
				open(nameOfTorrent, 'wb').write(fileToDownload.content)
				count += 1

if __name__ == "__main__":
	checkDirectory()
	arrayOfTitles=searchItems()

	while True:
		for i in arrayOfTitles:
			item= { 'mire' : i }
			downloadItems(item)
			displayInfo("Finished\n")
		print("======================================")
		time.sleep(settings.nCoreData['timeDuration'])