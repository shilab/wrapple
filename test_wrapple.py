from wrapple import *
from nose.tools import raises
from mock import patch
import unittest

def test_change_true_1():
    assert change_true(True) == 'true'
def test_change_true_2():
    assert change_true(False) == False

def test_check_args_1():
    assert check_args('19', 2, False, None, 'G') == None
@raises(SystemExit)
def test_check_args_2():
    check_args('32', 2, False, None, 'G')
@raises(SystemExit)
def test_check_args_3():
    check_args('19', 11, False, None, 'G')
@raises(SystemExit)
def test_check_args_4():
    check_args('19', 2, True, None, 'G')
def test_check_args_5():
    assert check_args('19', 2, True, None, 'S') == None
def test_check_args_6():
    assert check_args('19', 2, True, None, 'R') == None
@raises(SystemExit)
def test_check_args_7():
    check_args('19', 2, False, 'specified', 'G')

@raises(SystemExit)
def test_get_snps_1():
    get_snps('not_a_snp_file')
def test_get_snps_2():
    assert get_snps('snps') == 'rs3890745\nrs2240340\nrs2476601'

def test_get_zoomed_genes_1():
    assert get_zoomed_genes(None) == ''
def test_get_zoomed_genes_2():
    assert get_zoomed_genes('zoom_gene') == 'BRCA1,BRCA2'
@raises(SystemExit)
def test_get_zoomed_genes_3():
    get_zoomed_genes('not_a_zoom_file')

def test_get_specified_genes_1():
    assert get_specified_genes(None) == ''
def test_get_specified_genes_2():
    assert get_specified_genes('specified') == 'BRCA1\nBRCA2'
@raises(SystemExit)
def test_get_specified_genes_3():
    get_specified_genes('not_a_specified_file')

@raises(SystemExit)
def test_create_request_1():
    parser = create_parser()
    args = parser.parse_args([])
    create_request(args)

@raises(SystemExit)
def test_create_request_2():
    parser = create_parser()
    args = parser.parse_args(['-f', 'snps'])
    create_request(args)

@raises(SystemExit)
def test_create_request_3():
    parser = create_parser()
    args = parser.parse_args(['-f', 'snps', '-d', 'description'])
    create_request(args)

def test_create_request_4():
    parser = create_parser()
    args = parser.parse_args(['-f', 'snps', '-d', 'description', '-e', 'test@test'])
    params, _, _ = create_request(args)
    assert params == 'plot=False&zoomedGenes=&description=description&numberPermutations=1000&snpListFile=filename%3D%22%22&nearestgene=&CIcutoff=2&regDown=50&email=test%40test&submit=submit&genome=19&regUp=50&snpList=rs3890745%0Ars2240340%0Ars2476601&collapseCI=False&plotP=False&genesToSpecify='

def fail_urlopen(url):
    url_file = open('fail.html', 'r')
    return url_file

def status_urlopen(url):
    url_file = open('status.html', 'r')
    return url_file

class send_fail(unittest.TestCase):

    def setUp(self):
        self.patcher = patch('urllib2.urlopen', fail_urlopen)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    @raises(SystemExit)
    def test_send_request_2(self):
        request = ''
        _, _, _ = send_parameters(request, 1, 'description')

class send_success(unittest.TestCase):
    
    def setUp(self):
        self.patcher = patch('urllib2.urlopen', status_urlopen)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_send_request_3(self):
        request = ''
        link, _, _ = send_parameters(request, 1, 'description')
        assert link == 'http://www.broadinstitute.org/mpg/dapple/statusTMP.php?jid=1418998161'

def finished_urlopen(url):
    url_file = open('finished.html', 'r')
    return url_file

class status_finished(unittest.TestCase):

    def setUp(self):
        self.patcher = patch('urllib2.urlopen', finished_urlopen)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        
    def test_check_status(self):
        assert check_status('link', 1, 'description') == True

def run_urlopen(url):
    url_file = open('run.html', 'r')
    return url_file

class status_run(unittest.TestCase):
    def setUp(self):
        self.patcher = patch('urllib2.urlopen', run_urlopen)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_check_status_2(self):
        assert check_status('link', 1, 'description') == False

def pend_urlopen(url):
    url_file = open('pend.html', 'r')
    return url_file

class status_pend(unittest.TestCase):
    def setUp(self):
        self.patcher = patch('urllib2.urlopen', run_urlopen)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_check_status_3(self):
        assert check_status('link', 1, 'description') == False
