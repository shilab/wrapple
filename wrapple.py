"""Python wrapper for DAPPLE"""
__version__ = "0.0.1"
import urllib, urllib2
import time
import os
import argparse
import sys

#TODO: Try BeautifulSoup instead of the splits

def get_results(status_page_list, description):
    """Saves results when finished """
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
                            print 'Available'
                            available = True
                        except urllib2.HTTPError, e:
                            print e
                            print 'Oops, 404'
                            time.sleep(30)
                    #command = 'wget ' + tag.split("\"")[1]
                    os.system(command)
                    print command


def check_status(link, wait, description):
    """Updates status of run"""
    try:
        status_page = urllib2.urlopen(link)
        status_page_list = status_page.read().split("\n")
    except:
        time.sleep(wait*60)
        return check_status(link, wait, description)

    for page_line in status_page_list:
        if 'status' in page_line:
            tag = page_line.split("<BR>")
            print tag[2] + "\t" + tag[3].split("<a href")[0]
            if 'FINISHED' in tag[2]:
                get_results(status_page_list, description)
            else:
                time.sleep(wait*60)
                return check_status(link, wait, description)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(formatter_class=
                                     argparse.RawTextHelpFormatter)
    parser.add_argument('-e', '--email', nargs=1)
    parser.add_argument('-d', '--description', nargs=1)
    parser.add_argument('-f', '--snpfile', nargs=1)
    parser.add_argument('-w', '--wait', nargs='?', default=1,
                        help='Check status page every -w minutest.\n'
                        + 'Longer wait times suggested for larger datasets.\n'
                        'Default is 1 minute.')
    #TODO: Add options
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
    parser.add_argument('-us', '--upstream', nargs='?',
                        help='Define gene regulatory region. Can only be '
                        + 'used with SNP and region input. In kb')
    parser.add_argument('-ds', '--downstream', nargs='?',
                        help='Define gene regulatory region. Can only be '
                        + 'with SNP and region input. In kb')
    parser.add_argument('-n', '--nearest', action='store_true',
                        help='Use nearest gene for SNP input, instead of all '
                        + 'genes in the chosen region')
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
    args = parser.parse_args()

    filename = args.snpfile[0]
    cutoff = int(args.ci_cutoff)

    if args.genome != '19' and args.genome != '18' and args.genome != '1kg':
        print args.genome + ' is not a valid genome option.'
        sys.exit()

    if cutoff < 2 or cutoff > 10:
        print 'CI Cutoff needs to be between 2 and 10'
        sys.exit()

    if args.plot == True:
        args.plot = 'true'

    if args.simplify_plot == True:
        args.simplify_plot = 'true'

    if args.color_plot == True:
        args.color_plot = 'true'

    if args.nearest == True:
        args.nearest = 'true'

    if args.zoom_to_gene != None:
        zoomed_genes = open(args.zoom_to_gene, 'r').read()
        zoomed_genes = zoomed_genes.rstrip()
        zoomed_genes = zoomed_genes.replace('\n', ',')
    else:
        zoomed_genes = ''

    try:
        snp_file = open(filename, 'r')
        snps = snp_file.read()
    except IOError, e:
        print e.strerror + ': ' + filename
        sys.exit()

    if args.upstream == None:
        args.upstream = 50
    if args.downstream == None:
        args.downstream = 50

    if (args.nearest != None and not (args.input[0] != 'S' or
      args.input[0] != 'R')):
        print 'Nearest genes can only be used with SNP or region input'
        sys.exit()
    
    if not(args.nearest):
        args.nearest = ''

    page = 'http://www.broadinstitute.org/mpg/dapple/dappleTMP.php'
    raw_params = {'genome':args.genome, 'numberPermutations':args.permutations,
                  'CIcutoff':cutoff, 'regUp':args.upstream,
                  'regDown':args.downstream, 'nearestgene':args.nearest,
                  'snpListFile':'filename=""', 'snpList':snps,
                  'genesToSpecifyFile':'filename=""', 'plot':args.plot,
                  'plotP':args.color_plot, 'collapseCI':args.simplify_plot,
                  'genesToSpecify':'', 'zoomedGenes':zoomed_genes,
                  'email':args.email[0], 'description':args.description[0],
                  'submit':'submit'}
    params = urllib.urlencode(raw_params)
    print params
    request = urllib2.Request(page, params)
    page = urllib2.urlopen(request)
    page_list = page.read().split("\n")

    for line in page_list:
        if 'status' in line:
            link = line.split("<a href=")[1].split(">")[0]

    try:
        print "The link to the status page and results is: " + link
        check_status(link, args.wait, args.description[0])
    except:
        print 'You have exceeded DAPPLE\'s use limit. Wait a bit, and resubmit.'
        sys.exit()

if __name__ == "__main__":
    main()
