import urllib, urllib2
import re
import time
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-e','--email', nargs=1) 
parser.add_argument('-d','--description',nargs=1)
parser.add_argument('-f','--snpfile',nargs=1)
args = parser.parse_args()

email = args.email[0]
description=args.description[0]
filename = args.snpfile[0]

snp_file = open(filename,'r')
snps =snp_file.read()

def check_status():
    try:
        status_page = urllib2.urlopen(link) 
        status_page_list = status_page.read().split("\n")
    except:
        time.sleep(60)
        return check_status()

    for line in status_page_list:
        if 'status' in line:
            t= line.split("<BR>")
            print t[2] + "\t" + t[3].split("<a href")[0]
            if 'FINISHED' in t[2]:
                for l in status_page_list:
                    if '_summary' in l:
                        temp =  l.split(">")
                        for t in temp:
                            if 'http:' in t:
                                file =t.split("/")[-1].split("\"")[0] 
                                #command = 'wget ' + t.split("\"")[1]
                                #TODO:Check if directory exists before mkdir
                                make_dir = 'mkdir ' + description
                                os.system(make_dir)
                                file = description+'/'+file
                                command = 'curl ' + t.split("\"")[1] + '>' +file 
                                os.system(command)
                        
            else:
                time.sleep(60)
                return check_status()

page = 'http://www.broadinstitute.org/mpg/dapple/dappleTMP.php'
raw_params = {'genome':'19','numberPermutations':'1000','CIcutoff':'2','regUp':'50','regDown':'50','snpListFile':'filename=""','snpList':snps,'genesToSpecifyFile':'filename=""','genesToSpecify':'','zoomedGenes':'','email':email,'description':description,'submit':'submit'}
params = urllib.urlencode(raw_params)
request = urllib2.Request(page, params)
page = urllib2.urlopen(request)
page_list = page.read().split("\t")

for line in page_list:
    if 'status' in line:
        link = line.split("<a href=")[1].split(">")[0]
            
print "The link to the status page and results is: " + link

check_status()
