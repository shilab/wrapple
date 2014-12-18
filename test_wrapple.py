from wrapple import *
from nose.tools import raises
from mock import patch

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


def fake_urlopen(url):
    url_file = open(url, 'r')
    return url_file

patcher = patch('urllib2.urlopen', fake_urlopen)
patcher.start()

def test_send_request_1():
    status_page = urllib2.urlopen('snps')
    status_page_list = status_page.read().split("\n")
    assert status_page_list == ['rs3890745', 'rs2240340', 'rs2476601', '']
