import urllib, urllib2
page = 'http://www.broadinstitute.org/mpg/dapple/dappleTMP.php'
#headers = {'':''}
raw_params = {'genome':'19','numberPermutations':'1000','CIcutoff':'2','regUp':'50','regDown':'50','snpListFile':'filename=""','snpList':"BRCA1\nBRCA2",'genesToSpecifyFile':'filename=""','genesToSpecify':'','zoomedGenes':'','email':'aquitada@uncc.edu','description':'DappleTest','submit':'submit'}
params = urllib.urlencode(raw_params)
request = urllib2.Request(page, params)
page = urllib2.urlopen(request)
info = page.info()
#print page.read() 
page_list = page.read().split("\t")

for line in page_list:
    if 'status' in line:
            link = line.split("<a href=")[1].split(">")[0]
                    
print "The link to the results is: " + link
