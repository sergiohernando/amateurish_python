import requests
import json
import time
from bs4 import BeautifulSoup

# SOME VARIABLES

api_dev_key = 'your_dev_key_goes_here'
api_user_name = your_username_goes_here
api_user_password = 'your_password_goes_here'
login_url = 'https://pastebin.com/api/api_login.php'

# REQUEST TO OBTAIN THE USER KEY

r1 = requests.post(login_url, data = {'api_dev_key':api_dev_key, 'api_user_name':api_user_name, 'api_user_password':api_user_password})
api_user_key = r1.text
print ("Assigned API user key: " + api_user_key + "\n")

# CALL THE SCRAPING URL AND THE TRENDING URL

pastebin_scraping_url ='https://pastebin.com/api_scraping.php'
pastebin_trending_url = 'https://pastebin.com/api/api_post.php'

r_most_recent = requests.get(pastebin_scraping_url)
r_trending = requests.post(pastebin_trending_url, data = {'api_dev_key':api_dev_key, 'api_option':'trends'})
most_recent_pastebins = r_most_recent.text # THIS IS JSON FORMATTED
trending_pastebins = r_trending.text # THIS IS NOT JSON FORMATTED WILL BE DEALT WITH BEAUTIFULSOUP
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

#SOME BEAUTIFUL SOUP TO EXTRACT THE TAGS OF THE TRENDING POST REQUEST

file = open("pastebinoutput.txt", "w", encoding='UTF8')

soup = BeautifulSoup(trending_pastebins, 'html.parser')

find_tag = soup.findAll('paste')

trending_dictionary = {}

for elementos in find_tag:

	trending_paste_key = elementos.paste_key.contents	
	trending_paste_date = elementos.paste_date.contents
	trending_paste_title = elementos.paste_title.contents	
	trending_paste_size = elementos.paste_size.contents
	trending_paste_expire_date = elementos.paste_expire_date.contents
	trending_paste_private = elementos.paste_private.contents
	trending_paste_format_long = elementos.paste_format_long.contents
	trending_paste_format_short = elementos.paste_format_short.contents
	trending_paste_url = elementos.paste_url.contents
	trending_paste_hits = elementos.paste_hits.contents
	print(trending_paste_key)

	trending_dictionary.update({'paste_key': trending_paste_key, 'paste_date': trending_paste_date, 'paste_title': trending_paste_title, 'paste_size': trending_paste_size, 'paste_expire_date': trending_paste_expire_date, 'paste_private': trending_paste_private, 'paste_format_long': trending_paste_format_long, 'paste_format_short': trending_paste_format_short, 'paste_url': trending_paste_url, 'paste_hits': trending_paste_hits})

	print (trending_dictionary)

	file.write("===============================================================" + "\n")
	file.write("Trending element: " + str(trending_dictionary['paste_key']) + "\n")
	file.write("Date: " + str(trending_dictionary['paste_date']) + "\n" + "Hits: " + str(trending_dictionary['paste_hits']) + "\n"+ "URL: " + str(trending_dictionary['paste_url']) + "\n\n")
	file.write("===============================================================" + "\n")
		
# POPULATING THE DICTIONARY WITH JSON OUTPUT, PROCESS AND WRITE TO FILE

working_dictionary = {}

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
	if working_dictionary[syntax] == 'text':
		r2 = requests.get(working_dictionary[scrape_url])
		file.write("Content: " + "\n\n" + r2.text + "\n\n")
	else:
		file.write("Content is not text: " + working_dictionary[syntax] + " detected, so skipping retrieval" + "\n\n")

file.close()
