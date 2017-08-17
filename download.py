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
	if os.path.isfile("data"):
		os.remove("data")

def displayInfo(info):
	sys.stdout.write(time.strftime("%H:%M:%S  "))
	file=open("data","a")
	file.write(time.strftime("%H:%M:%S  ") + info + "\n")
	print(info)

def searchItems():
	file=open("searchList", "r").readlines()
	for i in file:
		if i == '\n':
			file.remove(i)
	index = 0
	for i in file:
		file[index]=file[index].replace('\n', '')
		index +=1
	return file

def removeUnnecessaryItems(array):
	lines=searchItems()
	for i in lines:
		if i in array:
			lines.remove(i)
	return lines

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
				if os.path.isfile(nameOfTorrent+".imported"):
					displayInfo("Skip torrent: "+nameOfTorrent)
					count += 1
					continue
				idList[count] = makeID(idList[count])
				fileToDownload = requests.get(idList[count], allow_redirects=True)
				open(nameOfTorrent, 'wb').write(fileToDownload.content)
				count += 1
			return len(idList)

if __name__ == "__main__":
	checkDirectory()
	arrayOfTitles=searchItems()

	itemsToRemove=[]
	while arrayOfTitles:
		for i in arrayOfTitles:
			item= { 'mire' : i }
			foundItems=downloadItems(item)
			if foundItems > 0:
				itemsToRemove.append(i)
			displayInfo("Finished\n")
		print("================================================================")
		time.sleep(settings.nCoreData['timeDuration'])
		arrayOfTitles=removeUnnecessaryItems(itemsToRemove)

displayInfo("Got everything :)")
