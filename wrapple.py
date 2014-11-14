"""Python wrapper for DAPPLE"""

import urllib, urllib2
import time
import os
import argparse
import sys

#TODO: Try BeautifulSoup instead of the splits

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-e', '--email', nargs=1)
parser.add_argument('-d', '--description', nargs=1)
parser.add_argument('-f', '--snpfile', nargs=1)
parser.add_argument('-w', '--wait', nargs='?', default=1,
                    help='Check status page every -w minutest.\n'
                    + 'Longer wait times suggested for larger datasets.\n'
                    'Default is 1 minute.')
parser.add_argument('-p', '--permutations', nargs='?', default=1000,
                    help='Number of permutations to run. Default is 1000')
parser.add_argument('-g', '--genome', nargs='?', default='19',
                    help='Genome Assembly Options:\n19: Hg19/HapMap\n'
                    + '18: Hg18/HapMap\n1kg: Hg19/1000Genomes SNPs')
parser.add_argument('-c', '--ci_cutoff', nargs='?', default=2,
                    help='Common Interactor Binding Degree Cuttoff:\n'
                    +'Options:2-10\nDefault:2')
args = parser.parse_args()

email = args.email[0]
description = args.description[0]
filename = args.snpfile[0]
wait = args.wait
perm = args.permutations
genome = args.genome
cutoff = int(args.ci_cutoff)

if genome != '19' and genome != '18' and genome != '1kg':
    print genome + ' is not a valid genome option.'
    sys.exit()

if cutoff < 2 or cutoff > 10:
    print 'CI Cutoff needs to be between 2 and 10'
    sys.exit()

#TODO: When file upload is working, check snpfile if exists
snp_file = open(filename, 'r')
snps = snp_file.read()

def get_results(status_page_list):
    """Saves results when finished """
    for status_line in status_page_list:
        if '_summary' in status_line:
            temp = status_line.split(">")
            for tag in temp:
                if 'http:' in tag:
                    outfile = tag.split("/")[-1].split("\"")[0]
                    #command = 'wget ' + t.split("\"")[1]
                    #TODO:Check if directory exists before mkdir
                    make_dir = 'mkdir ' + description
                    os.system(make_dir)
                    outfile = description+'/'+ outfile
                    command = 'curl ' + tag.split("\"")[1] + '>' + outfile
                    os.system(command)


def check_status():
    """Updates status of run"""
    try:
        status_page = urllib2.urlopen(link)
        status_page_list = status_page.read().split("\n")
    except:
        time.sleep(wait*60)
        return check_status()

    for page_line in status_page_list:
        if 'status' in page_line:
            tag = page_line.split("<BR>")
            print tag[2] + "\t" + tag[3].split("<a href")[0]
            if 'FINISHED' in tag[2]:
                get_results(status_page_list)
            else:
                time.sleep(wait*60)
                return check_status()

page = 'http://www.broadinstitute.org/mpg/dapple/dappleTMP.php'
raw_params = {'genome':genome, 'numberPermutations':perm, 'CIcutoff':cutoff,
              'regUp':'50', 'regDown':'50', 'snpListFile':'filename=""',
              'snpList':snps, 'genesToSpecifyFile':'filename=""',
              'genesToSpecify':'', 'zoomedGenes':'',
              'email':email, 'description':description, 'submit':'submit'}
params = urllib.urlencode(raw_params)
request = urllib2.Request(page, params)
page = urllib2.urlopen(request)
page_list = page.read().split("\n")

for line in page_list:
    if 'status' in line:
        link = line.split("<a href=")[1].split(">")[0]

print "The link to the status page and results is: " + link

check_status()
