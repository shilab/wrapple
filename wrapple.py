import urllib, urllib2
import re
import time
import os
import argparse
import sys

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-e','--email', nargs=1) 
parser.add_argument('-d','--description',nargs=1)
parser.add_argument('-f','--snpfile',nargs=1)
parser.add_argument('-w','--wait',nargs='?',default=1,help='Check status page every -w minutest. \nLonger wait times suggested for larger datasets. \nDefault is 1 minute.')
parser.add_argument('-p','--permutations',nargs='?',default=1000,help='Number of permutations to run. Default is 1000')
parser.add_argument('-g','--genome',nargs='?',default='19',help='Genome Assembly Options:\n19: Hg19/HapMap\n18: Hg18/HapMap\n1kg: Hg19/1000Genomes SNPs')
parser.add_argument('-c','--ci_cutoff',nargs='?',default=2,help='Common Interactor Binding Degree Cuttoff:\nOptions:2-10\nDefault:2')
args = parser.parse_args()

email = args.email[0]
description=args.description[0]
filename = args.snpfile[0]
wait = args.wait
perm = args.permutations
genome=args.genome
cutoff=int(args.ci_cutoff)

if (genome!='19' and genome!='18' and genome!='1kg'):
        print genome + ' is not a valid genome option.'
        sys.exit()

if (cutoff<2 or cutoff>10):
    print 'CI Cutoff needs to be between 2 and 10'
    sys.exit()

#TODO: When file upload is working, check snpfile if exists
snp_file = open(filename,'r')
snps =snp_file.read()

def check_status():
    try:
        status_page = urllib2.urlopen(link) 
        status_page_list = status_page.read().split("\n")
    except:
        time.sleep(wait*60)
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
                time.sleep(wait*60)
                return check_status()

page = 'http://www.broadinstitute.org/mpg/dapple/dappleTMP.php'
raw_params = {'genome':genome,'numberPermutations':perm,'CIcutoff':cutoff,'regUp':'50','regDown':'50','snpListFile':'filename=""','snpList':snps,'genesToSpecifyFile':'filename=""','genesToSpecify':'','zoomedGenes':'','email':email,'description':description,'submit':'submit'}
params = urllib.urlencode(raw_params)
request = urllib2.Request(page, params)
page = urllib2.urlopen(request)
page_list = page.read().split("\t")

for line in page_list:
    if 'status' in line:
        link = line.split("<a href=")[1].split(">")[0]
            
print "The link to the status page and results is: " + link

#check_status()
