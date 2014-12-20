"""Python wrapper for DAPPLE"""
__version__ = "0.0.1"
import urllib, urllib2
import time
import os
import argparse
import sys

#TODO: Try BeautifulSoup instead of the splits

def create_parser():
    parser = argparse.ArgumentParser(formatter_class=
                                     argparse.RawTextHelpFormatter)
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
    parser.add_argument('-i', '--input', nargs=1, help='Specify the type '
                        +'of input.S: SNP\nR: Region\nC: Combination\n'+
                        'GR: Gene-Region\nG: Gene\nDefault is Gene',
                        default='G')
    parser.add_argument('-us', '--upstream', nargs='?', default=50,
                        help='Define gene regulatory region. Can only be '
                        + 'used with SNP and region input. In kb')
    parser.add_argument('-ds', '--downstream', nargs='?', default=50,
                        help='Define gene regulatory region. Can only be '
                        + 'with SNP and region input. In kb')
    parser.add_argument('-n', '--nearest', action='store_true',
                        help='Use nearest gene for SNP input, instead of all '
                        + 'genes in the chosen region')
    parser.add_argument('-gs', '--gene_specified', nargs='?',
                        help='Genes to specify as causal')
    parser.add_argument('-pl', '--plot', help='Plot the network',
                        action='store_true')
    parser.add_argument('-cp', '--color_plot', help='Color plot by p-value',
                        action='store_true')
    parser.add_argument('-s', '--simplify_plot', help='Simplify plot',
                        action='store_true')
    parser.add_argument('-z', '--zoom_to_gene',
                        help='Create a subplot with only the genes specified')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + __version__)

    return parser

def create_request(args):
    if args.snpfile != None:
        filename = args.snpfile[0]
    else:
        print 'You need to provide a input file'
        sys.exit()

    if args.description == None:
        print 'You need to provide a description'
        sys.exit()

    if args.email == None:
        print 'You need to provide an email'
        sys.exit()

    cutoff = int(args.ci_cutoff)

    check_args(args.genome, cutoff, args.nearest, args.gene_specified,
               args.input)

    args.plot = change_true(args.plot)
    args.simplify_plot = change_true(args.simplify_plot)
    args.color_plot = change_true(args.color_plot)
    args.nearest = change_true(args.nearest)

    zoomed_genes = get_zoomed_genes(args.zoom_to_gene)

    snps = get_snps(filename)

    specified_genes = get_specified_genes(args.gene_specified)

    if not args.nearest:
        args.nearest = ''

#    page = 'http://www.broadinstitute.org/mpg/dapple/dappleTMP.php'
    raw_params = {'genome':args.genome, 'numberPermutations':args.permutations,
                  'CIcutoff':cutoff, 'regUp':args.upstream,
                  'regDown':args.downstream, 'nearestgene':args.nearest,
                  'snpListFile':'filename=""', 'snpList':snps,
                  'genesToSpecify':specified_genes, 'plot':args.plot,
                  'plotP':args.color_plot, 'collapseCI':args.simplify_plot,
                  'zoomedGenes':zoomed_genes, 'email':args.email[0],
                  'description':args.description[0], 'submit':'submit'}
    params = urllib.urlencode(raw_params)
    print params
#    request = urllib2.Request(page, params)
#    return send_parameters(request, args.wait, args.description[0])
    return (params, args.wait, args.description[0])

def get_results(link, description):
    """Saves results when finished"""
    try:
        status_page = urllib2.urlopen(link)
        status_page_list = status_page.read().split("\n")
    except urllib2.URLError:
        #time.sleep(wait*60)
#        get_results(link, description)
        return False

    for status_line in status_page_list:
        if '_summary' in status_line:
            temp = status_line.split(">")
            make_dir = 'mkdir ' + description
            os.system(make_dir)
            time.sleep(60)
            for tag in temp:
                if 'http:' in tag:
                    outfile = tag.split("/")[-1].split("\"")[0]
                    outfile = description+'/'+ outfile
                    command = 'curl ' + tag.split("\"")[1] + ' -o ' + outfile
                    available = False
                    while not available:
                        try:
                            urllib2.urlopen(tag.split("\"")[1])
                            available = True
                        except urllib2.HTTPError, err:
                            print err
                            print 'Oops, 404'
                            time.sleep(30)
                    os.system(command)
                    #print command
    return
def check_status(link, wait, description):
    """Updates status of run"""
    try:
        status_page = urllib2.urlopen(link)
        status_page_list = status_page.read().split("\n")
    except urllib2.URLError:
        #time.sleep(wait*60)
#        return check_status(link, wait, description)
        return False

    for page_line in status_page_list:
        if 'status' in page_line:
            tag = page_line.split("<BR>")
            print tag[2] + "\t" + tag[3].split("<a href")[0]
            if 'FINISHED' in tag[2]:
                #get_results(status_page_list, description)
                return True
            else:
                #time.sleep(wait*60)
                #return check_status(link, wait, description)
                return False

def check_args(genome, cutoff, nearest, specified, input_type):
    """Check for mistakes in arguments that are fatal"""
    if genome != '19' and genome != '18' and genome != '1kg':
        print genome + ' is not a valid genome option.'
        sys.exit()

    if cutoff < 2 or cutoff > 10:
        print 'CI Cutoff needs to be between 2 and 10'
        sys.exit()

    if (nearest == True and not (input_type[0] == 'S' or
      input_type[0] == 'R')):
        print 'Nearest genes can only be used with SNP or region input'
        sys.exit()

    if specified != None and input_type[0] == 'G':
        print 'Specified genes can\'t be used with gene input'
        sys.exit()

    else:
        return

def change_true(arg):
    """Change True to true for request headers"""
    if arg == True:
        arg = 'true'
    return arg

def get_zoomed_genes(zoomed):
    """Get the list of zoomed genes"""
    if zoomed != None:
        try:
            zoomed_genes = open(zoomed, 'r').read()
            zoomed_genes = zoomed_genes.rstrip()
            zoomed_genes = zoomed_genes.replace('\n', ',')
        except IOError as err:
            print err.strerror + ': ' + zoomed
            sys.exit()
    else:
        zoomed_genes = ''
    return zoomed_genes

def get_specified_genes(specified):
    """Get the list of specified genes"""
    if specified != None:
        try:
            specified_genes = open(specified, 'r').read()
            specified_genes = specified_genes.rstrip()
        except IOError as err:
            print err.strerror + ': ' + specified
            sys.exit()
    else:
        specified_genes = ''
    return specified_genes

def get_snps(filename):
    """Read snps from file"""
    try:
        snp_file = open(filename, 'r')
        snps = snp_file.read()
        snps = snps.rstrip()
    except IOError as err:
        print err.strerror + ': ' + filename
        sys.exit()
    return snps

def send_parameters(request, wait, description):
    """Sends all the parameters to DAPPLE, starts the job"""
    try:
        page = urllib2.urlopen(request)
        page_list = page.read().split("\n")
    except urllib2.URLError:
        print 'Check your network connection'
        sys.exit()

    for line in page_list:
        if 'status' in line:
            link = line.split("<a href=")[1].split(">")[0]

    try:
        print "The link to the status page and results is: " + link
        #return check_status(link, wait, description)
        return (link, wait, description)
    except UnboundLocalError:
        print 'You have exceeded DAPPLE\'s use limit. Wait a bit, and resubmit.'
        sys.exit()

def main():
    """Main function"""
    parser = create_parser()
    args = parser.parse_args()

    page = 'http://www.broadinstitute.org/mpg/dapple/dappleTMP.php'
    params, wait, description = create_request(args)
    request = urllib2.Request(page, params)

    link, wait, description = send_parameters(request, wait, description)

    done = check_status(link, wait, description) 
    while done == False:
        time.sleep(wait*60)    
        done = check_status(link, wait, description)

    results_avail = get_results(link, description)
    while results_avail == False:
        time.sleep(wait*60)
        results_avail = get_results(link, description)
    
if __name__ == "__main__":
    main()
