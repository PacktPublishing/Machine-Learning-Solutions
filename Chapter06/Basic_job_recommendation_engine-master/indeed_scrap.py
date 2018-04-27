from lxml import html
import requests
import re
import pdfquery
import urllib2
import time
import sys

def download_file(download_url,idx):
    response = urllib2.urlopen(download_url)
    file = open("./resume_scrap/"+sys.argv[1]+ "/"+str(idx)+".pdf", 'w')
    file.write(response.read())
    file.close()


indeed = "http://www.indeed.com"
url_prefix = "http://www.indeed.com/resumes?q="+sys.argv[1]+"&co=US&start="

target_idx = 10000

idx = int(sys.argv[2])
file_no = idx
while(idx < target_idx):
	url = url_prefix + str(idx)
	page = requests.get(url).content
	all_links = re.findall(r"/r/[^\?]*", page)
	for link in all_links:
		time.sleep(1)
		url = indeed + link
		page = requests.get(url).content
		print file_no
		print ' files downloaded'
		try:
			download_link = re.search(r"/r/[^\"]*pdf", page).group(0)
			url = indeed + download_link
			download_file(url,file_no)
			file_no = file_no + 1
		except:
			continue

	idx = idx + 50

