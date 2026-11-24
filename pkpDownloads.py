################################################################################
# Program to compute downloads for any OJS or OMP platform for a specific year #
#                                                                              #
# This program must be launched with the following mandatory parameters:       #
# python pkpDownloads.py DESTURL YEAR OUTFILE APIKEY                           #
# 																			   #
# where:                                                                       #
#       - DESTURL is in the form https://ojs.example.com                       #
#       - YEAR    is the year in the form aaaa (2026 for example)              #
#       - OUTFILE is the suffix of the output file                             #
#       - APIKEY  is the APIKEY                                                #
# 																			   #
# The program must be launched for each platform. So, if you have OJS and OMP, #
#   you should lauch twice, in the following forms:                            #
#	python pkpDownloads.py https://ojs.example.com 2025 outOjs ojsApiKey	   #
#	python pkpDownloads.py https://omp.example.com 2025 outOmp ompApiKey 	   #
# 																			   #
# 																			   #
# The program produces two output files for each launch, in json format.	   #
# One file contains the series, and the other one contains the series with     #
# related statistics 														   #
# 																			   #
# 																			   #
#                                                            2026 Dario Basset #
################################################################################

import json
import sys
import requests
import datetime

TIMEOUT = 120           # HTTP timeout
PAGE_SIZE = 100         # max elements 
MAX_RETRY = 3           # retries 
T_URL2 = '/api/v1/'     # second part of URL
T_LOG = f'log.txt'      # log

def echoLog(stringObject):
    f = open(T_LOG, "a", encoding="utf-8")
    t = datetime.datetime.now()
    toWrite =  t.strftime("%Y-%m-%d %H:%M:%S") + " " + str(stringObject)
    f.write(toWrite + "\n")
    print (toWrite) 
    f.close() 

def getItemList (apiUrl, headers):
    pageCount = 0
    perPage = 1
    url = apiUrl+'/index.php/index'+T_URL2+'contexts?isEnabled=true&count='+str(perPage)+'&offset='+str(pageCount)
    echoLog(url + " " + APIKEY)
    pageString = requests.get(url, timeout=TIMEOUT, headers=headers)
    page = json.loads(pageString.text)
    total = page['itemsMax'] or 0
    jList = []
    perPage = PAGE_SIZE
    journalCount = 0
    while pageCount < total:
        url = apiUrl+'/index.php/index'+T_URL2+'contexts?isEnabled=true&count='+str(perPage)+'&offset='+str(pageCount)
        pageString = requests.get(url, timeout=TIMEOUT, headers=headers)
        page = json.loads(pageString.text)
        pageCount += perPage
        for item in page['items']:
            urlPath = item['urlPath'] or ""
            if urlPath != "testupov": 	#SKIP here 
                journalCount += 1
                journal = {}
                journal['href'] = item['url'] or "No URL"
                journal['urlPath'] = urlPath
                if 'it_IT' in item['description']: journal['description'] = item['description']['it_IT'] or ""
                if 'it_IT' in item['name']: journal['name'] = item['name']['it_IT'] or ""
                if item['enabled']: 
                    journal['enabled'] = "Yes" 
                else: 
                    journal['enabled'] = "No"
                journal['id'] = item['id'] or 0

                jList.append(journal)
    print("We have "+str(len(jList))+" items.")
    return(jList)

def getDownloads(apiUrl, headers, jList): 
    downloads = {}
    totalDownload = 0; 
    for item in jList:
        galleyView = 0
        pageCount = 0
        perPage = 1
        urlPath = item['urlPath']
        echoLog(urlPath)
        url = apiUrl+'/index.php/'+urlPath+T_URL2+'/stats/publications?dateEnd='+DATEEND+'&dateStart='+DATESTART+'&count='+str(perPage)+'&offset='+str(pageCount)
        pageString = requests.get(url, timeout=TIMEOUT, headers=headers)
        page = json.loads(pageString.text)
        total = page['itemsMax'] or 0
        perPage = 100
        while pageCount < total:
            url = apiUrl+'/index.php/'+urlPath+T_URL2+'/stats/publications?dateEnd='+DATEEND+'&dateStart='+DATESTART+'&count='+str(perPage)+'&offset='+str(pageCount)
            pageString = requests.get(url, timeout=TIMEOUT, headers=headers)
            page = json.loads(pageString.text)
            pageCount += perPage
            for item in page['items']:
                views = item['galleyViews'] or 0
                galleyView += views
        downloads[urlPath] = galleyView
        totalDownload += galleyView
    downloads['TOTAL'] = totalDownload
    return(downloads)
        
######################## MAIN ##########
if len(sys.argv) < 3:
    print("Usage: " + sys.argv[0] + " [OJS/OMP URL] year outputFile [APIKEY]")
    sys.exit()
DESTURL = sys.argv[1]
YEAR = sys.argv[2]
OUTFILE = sys.argv[3]
APIKEY = sys.argv[4] 
print("You launched " + sys.argv[0] + " " + sys.argv[1] + " " + sys.argv[2] + " " + sys.argv[3] + " and the APIKEY")
if len(YEAR) != 4:
    print("Wrong year")
    print("Usage: " + sys.argv[0] + " [OJS/OMP URL] year outputFile [APIKEY]")
    sys.exit()
DATEEND = YEAR + '-12-31'
DATESTART = YEAR + '-01-01'
headers = {'Authorization': f'Bearer {APIKEY}'}

itemList = getItemList(DESTURL, headers)
with open(OUTFILE + '-series.json', 'w') as file:
    json.dump(itemList, file)
downloadList = getDownloads(DESTURL, headers, itemList)
with open(OUTFILE + str(YEAR) + '-downloads.json', 'w') as file:
    json.dump(downloadList, file)
