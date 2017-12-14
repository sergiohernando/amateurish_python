# THIS PIECE OF CODE RETRIEVES VIA THE PASTEBIN API THE LATEST BINS 

import requests
import json
import time

# SOME VARIABLES

api_dev_key = 'your_dev_key_goes_here'
api_user_name = 'your_user_goes_here'
api_user_password = 'your_password_goes_here'
login_url = 'https://pastebin.com/api/api_login.php'

# REQUEST TO OBTAIN THE USER KEY

r = requests.post(login_url, data = {'api_dev_key':api_dev_key, 'api_user_name':api_user_name, 'api_user_password':api_user_password})
api_user_key = r.text
print ("Assigned API user key: " + api_user_key + "\n")

# CALL THE SCRAPING URL 

pastebin_scraping_url ='https://pastebin.com/api_scraping.php'
most_recent_url = requests.get(pastebin_scraping_url)
most_recent_pastebins = most_recent_url.text
json_content = json.loads(most_recent_pastebins)

# JSON STRUCTURE

full_url = 'full_url'
scrape_url = 'scrape_url'
date = 'date'
key = 'key'
size = 'size'
expire = 'expire'
title = 'title'
syntax = 'syntax'
user = 'user'

# POPULATING THE DICTIONARY WITH JSON OUTPUT, PROCESS AND WRITE TO FILE

working_dictionary = {}

file = open("pastebinoutput.txt", "w", encoding='UTF8')

for element in json_content:

	working_dictionary.update({'full_url': element[full_url], 'scrape_url': element[scrape_url], 'date': element[date], 'key': element[key], 'size': element[size], 'expire': element[expire], 'title': element[title], 'syntax': element[syntax], 'user': element[user]})
	print ("Processing: " +working_dictionary[full_url] + "\n")
	file.write("===============================================================" + "\n")
	file.write("Procesing: " + working_dictionary[full_url] + "\n")
	if not working_dictionary[title]:
		file.write("Title: Not specified" + "\n")
	else:
		file.write("Title: " + working_dictionary[title] + "\n")
	friendly_time_date =  time.strftime("%H:%M:%S - %m/%M/%Y %Z", time.localtime(int(working_dictionary[date])))
	file.write("Date: " + friendly_time_date + "\n")
	if not working_dictionary[user]:
		file.write("User: Not specified" + "\n")
	else:
		file.write("User: " + working_dictionary[user] + "\n")
	file.write("Syntax: " + working_dictionary[syntax] + "\n")
	file.write("Size: " + working_dictionary[size] + "\n")
	file.write("===============================================================" + "\n")
	r2 = requests.get(working_dictionary[scrape_url])
	file.write("Content: " + "\n\n" + r2.text + "\n\n")

file.close()

