import urllib, urllib2
import re
import time

def check_status():
    status_page = urllib2.urlopen(link) 
    status_page_list = status_page.read().split("\n")

    for line in status_page_list:
        if 'status' in line:
            t= line.split("<BR>")
            print t[2] + "\t" + t[3].split("<a href")[0]
            if 'FINISHED' in t[2]:
                for l in status_page_list:
                    if '_summary' in l:
                        print l
            else:
                time.sleep(60)
                return check_status()

page = 'http://www.broadinstitute.org/mpg/dapple/dappleTMP.php'
raw_params = {'genome':'19','numberPermutations':'1000','CIcutoff':'2','regUp':'50','regDown':'50','snpListFile':'filename=""','snpList':"BRCA1\nBRCA2",'genesToSpecifyFile':'filename=""','genesToSpecify':'','zoomedGenes':'','email':'aquitada@uncc.edu','description':'DappleTest','submit':'submit'}
params = urllib.urlencode(raw_params)
request = urllib2.Request(page, params)
page = urllib2.urlopen(request)
info = page.info()
page_list = page.read().split("\t")

for line in page_list:
    if 'status' in line:
            link = line.split("<a href=")[1].split(">")[0]
                    
print "The link to the results is: " + link

check_status()
