import urllib.request
from urllib.request import urlopen, Request
import sys
import os
import requests
import wget
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
i = 0
def download(url,folder):
	global i
	with requests.get(url, stream=True) as r:
		r.raise_for_status()
		if "?" in url:
			url = url.split("?")[-2]
		try:
			with open(folder+'/'+str(i)+url.split('/')[-1], 'wb') as f:
				for chunk in r.iter_content(chunk_size=8192): 
					f.write(chunk)
				i=i+1
		except Exception as e:
			print(e)
try:
	os.mkdir(sys.argv[2])
	req = Request(url=sys.argv[1], headers=headers)
	datos = urllib.request.urlopen(req).read().decode()
	soup = BeautifulSoup(datos,features="html.parser")
	
	# to images
	tags = soup('img')
	for tag in tags:
		url = tag.get('src')
		if not 'data:' in url:
			if 'http' in url:
				download(url,sys.argv[2])
			else:
				if url[0]=="/":
					split_url = sys.argv[1].split('/')
					url = split_url[0]+"//"+split_url[2]+url 
				else:
					url = sys.argv[1]+"/"+url 
				download(url,sys.argv[2])
				
	# to files	
	files = soup('a')
	for file in files:
		url = file.get('href')
		if url:
			if "?" in url:
				url = url.split("?")[-2]
			if 'http' in url:
				if url.endswith(".pdf") or url.endswith(".doc") or url.endswith(".docx") or url.endswith(".xls") or url.endswith(".xlsx"):
					download(url,sys.argv[2])
			else:
				if url.endswith(".pdf") or url.endswith(".doc") or url.endswith(".docx") or url.endswith(".xls") or url.endswith(".xlsx"):
					if url[0]=="/":
						split_url = sys.argv[1].split('/')
						url = split_url[0]+"//"+split_url[2]+url 
					else:
						url = sys.argv[1]+"/"+url 
					download(url,sys.argv[2])
			
	print("Successfully completed")
except Exception as e:
	print("ERROR: can't get files, check its parameters or contact the developer.")
	print(e)