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
    assert get_snps('tests/resources/snps') == 'rs3890745\nrs2240340\nrs2476601'

def test_get_zoomed_genes_1():
    assert get_zoomed_genes(None) == ''
def test_get_zoomed_genes_2():
    assert get_zoomed_genes('tests/resources/zoom_gene') == 'BRCA1,BRCA2'
@raises(SystemExit)
def test_get_zoomed_genes_3():
    get_zoomed_genes('not_a_zoom_file')

def test_get_specified_genes_1():
    assert get_specified_genes(None) == ''
def test_get_specified_genes_2():
    assert get_specified_genes('tests/resources/specified') == 'BRCA1\nBRCA2'
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
    args = parser.parse_args(['-f', 'tests/resourcessnps'])
    create_request(args)

@raises(SystemExit)
def test_create_request_3():
    parser = create_parser()
    args = parser.parse_args(['-f', 'tests/resources/snps', '-d', 'description'])
    create_request(args)

class TestRequest(unittest.TestCase):
    def test_create_request_4(self):
        parser = create_parser()
        args = parser.parse_args(['-f', 'tests/resources/snps', '-d', 'description', '-e', 'test@test'])
        params, _, _ = create_request(args)
        exp_param = {'plot': False, 'zoomedGenes': '', 'description': 'description', 'numberPermutations': 1000, 'snpListFile': 'filename=""', 'nearestgene': '', 'CIcutoff': 2, 'regDown': 50, 'email': 'test@test', 'submit': 'submit', 'genome': '19', 'regUp': 50, 'snpList': 'rs3890745\nrs2240340\nrs2476601', 'collapseCI': False, 'plotP': False, 'genesToSpecify': ''}
        self.assertEqual(params, exp_param)
    #    assert params == 'plot=False&zoomedGenes=&description=description&numberPermutations=1000&snpListFile=filename%3D%22%22&nearestgene=&CIcutoff=2&regDown=50&email=test%40test&submit=submit&genome=19&regUp=50&snpList=rs3890745%0Ars2240340%0Ars2476601&collapseCI=False&plotP=False&genesToSpecify='

def fail_urlopen(url):
    url_file = open('tests/resources/fail.html', 'rb')
    return url_file

def status_urlopen(url):
    url_file = open('tests/resources/status.html', 'rb')
    return url_file

class sendFail(unittest.TestCase):

    def setUp(self):
        self.patcher = patch('wrapple.urlopen', fail_urlopen)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    @raises(SystemExit)
    def test_send_request_2(self):
        request = ''
        _, _, _ = send_parameters(request, 1, 'description')

class SendSuccess(unittest.TestCase):
    
    def setUp(self):
        self.patcher = patch('wrapple.urlopen', status_urlopen)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_send_request_3(self):
        request = ''
        link, _, _ = send_parameters(request, 1, 'description')
        assert link == 'http://www.broadinstitute.org/mpg/dapple/statusTMP.php?jid=1418998161'

def send_exception_urlopen(url):
    raise urllib2.URLError('no host given')

class SendException(unittest.TestCase):
    def setUp(self):
        self.patcher = patch('wrapple.urlopen', send_exception_urlopen)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
    
    @raises(SystemExit)
    def test_send_request_4(self):
        request = ''
        _, _, _ = send_parameters(request, 1, 'description')

def finished_urlopen(url):
    url_file = open('tests/resources/finished.html', 'rb')
    return url_file

class StatusFinished(unittest.TestCase):

    def setUp(self):
        self.patcher = patch('wrapple.urlopen', finished_urlopen)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        
    def test_check_status(self):
        assert check_status('link', 1, 'description') == True

    def test_get_results_2(self):
        _, commands = get_results('link', 'description')
        assert commands[0] == 'curl http://www.broadinstitute.org/mpg/dapple/results/1418998161/StatusTest_summary -o description/StatusTest_summary'

def run_urlopen(url):
    url_file = open('tests/resources/run.html', 'rb')
    return url_file

class StatusRun(unittest.TestCase):
    def setUp(self):
        self.patcher = patch('wrapple.urlopen', run_urlopen)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_check_status_2(self):
        assert check_status('link', 1, 'description') == False

def pend_urlopen(url):
    url_file = open('tests/resources/pend.html', 'rb')
    return url_file

class StatusPend(unittest.TestCase):
    def setUp(self):
        self.patcher = patch('wrapple.urlopen', run_urlopen)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_check_status_3(self):
        assert check_status('link', 1, 'description') == False

def raise_url_exception(url):
    raise urllib2.URLError('no host given')

class StatusException(unittest.TestCase):
    def setUp(self):
        self.patcher = patch('wrapple.urlopen', raise_url_exception)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_check_status_4(self):
        assert check_status('link', 1, 'description') == False

def raise_missing_exception(url):
    raise urllib2.HTTPError('link',404, "test", {}, None)

class MissingException(unittest.TestCase):
    def setUp(self):
        self.patcher = patch('wrapple.urlopen', raise_missing_exception)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_get_results_3(self):
        ready, _ =  get_results('link', 'description')
        assert ready == False

    def test_get_results_4(self):
        _, commands = get_results('link', 'description')
        assert commands == None

class GetResultsException(unittest.TestCase):
    def setUp(self):
        self.patcher = patch('wrapple.urlopen', raise_url_exception)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_get_results_1(self):
        ready, _ = get_results('link', 'description')
        assert ready == False
