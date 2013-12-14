import urllib
import os
import csv
from bs4 import BeautifulSoup

songlist = "songs.txt"
youtubeURL = "http://www.youtube.com/results?search_query="


def writeToFile(songUrl):

	file = open('list.html','a+')
	file.write(songUrl + '\n')
	file.close()



# loop through each song in the list
with open(songlist, 'rb') as songs:
	songreader = csv.reader(songs, delimiter=' ', quotechar='|')
	for row in songreader:
		searchURL = ""
		songText = " ".join(row)
		if songText.find("SongName") > 0:
			continue
		
		print "STARTING: " + songText

		searchURL = youtubeURL + songText

	# search youtube for this song
		print "Searching Youtube..."
		results = urllib.urlopen(searchURL).read()
		soup = BeautifulSoup(results)
		print "Parsing results..."

		videoElement = soup.find("li", "yt-lockup")
		if videoElement is not None: 
			try: 
				videoLength = videoElement['data-context-item-time']
				videoLegnthInMinutes = videoLength.split(":")[0]
			except KeyError:
            	# result is not what we're looking for, onto the next song...
				print "ERROR: First YouTube result likely was a playlist, moving to next song \n\n"
				continue
		else:
			# # no results on youtube, onto the next song...
			print "ERROR: Nothing found on youtube \n\n"
			continue

		# if first result is more than 2 minutes, download it
		if videoLegnthInMinutes > 2:
			songURL = price = soup.find("a", { "class" : "ux-thumb-wrap" })
			songURL = songURL['href']
			songURL = "http://www.youtube.com" + songURL
			print "Writing to file"
			writeToFile(songURL)
			print "FINISHED: " + songText + "\n\n " 


#exit


