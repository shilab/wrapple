import urllib, urllib2
page = 'http://www.broadinstitute.org/mpg/dapple/dappleTMP.php'
#headers = {'':''}
raw_params = {'genome':'19','numberPermutations':'1000','CIcutoff':'2','regUp':'50','regDown':'50','snpListFile':'filename=""','snpList':"BRCA1\nBRCA2",'genesToSpecifyFile':'filename=""','genesToSpecify':'','zoomedGenes':'','email':'ama234@unh.edu','description':'DappleTest','submit':'submit'}
params = urllib.urlencode(raw_params)
request = urllib2.Request(page, params)
page = urllib2.urlopen(request)
info = page.info()
print page.read() 
