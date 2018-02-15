import os.path
from bs4 import BeautifulSoup
import urllib2

starting_url = "http://www.espn.com/nba/news/archive"
file_name = "archive.html"

#download archive html file if not already downloaded
if not os.path.isfile(file_name):
	response = urllib2.urlopen(starting_url)
	html = response.read()
	file = open(file_name,"w+")
	file.write(html)
	file.close()

#make folder if doesn't exist
if not os.path.exists("articles"):
	os.makedirs("articles")

i = 0
total = 0
with open(file_name) as file:
	html = file.read()
	soup = BeautifulSoup(html)
	li_tags = soup.find_all("li")
	a_tags = soup.find_all("a")
	for a_tag in a_tags:
		if a_tag.parent.name != "li": #must be within li tag
			continue
		href = a_tag.get("href")
		title = a_tag.get("title")
		if href.find("insider") != -1: #ignore insider stories
			continue
		elif href.find("nba") == -1: #must be in nba
			continue
		elif href.find("http") == -1 or href.find("espn") == -1: #must have http link and from espn
			continue
		else:
			print(href)
			total += 1
			i += 1
			#if i < 5: #cap at 5 for debugging
			if title != None and not os.path.isfile("articles/" + title):
				response = urllib2.urlopen(href)
				html = response.read()
				title = title.replace("/", "") #get rid of any slashes
				file = open("articles/" + title,"w+")
				file.write(html)
				file.close()
print("Number of articles: " + str(total))

