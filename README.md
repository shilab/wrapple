wrapple
=======
##A Python wrapper for DAPPLE  
[![Build Status](https://travis-ci.org/shilab/wrapple.svg?branch=master)](https://travis-ci.org/shilab/wrapple) [![Coverage Status](https://coveralls.io/repos/shilab/wrapple/badge.png)](https://coveralls.io/r/shilab/wrapple)  

wrapple is a command line wrapper for [DAPPLE](http://www.broadinstitute.org/mpg/dapple/dappleTMP.php#). You can use it to upload your inputs, and it will download the output files. wrapple is still under development, so some bugs need to be found. If you find a bug, open an issue. 

Install
```
git clone https://github.com/shilab/wrapple
cd wrapple
python setup.py install
```


Required Arguments  

```-e, --email```  
	Email address for DAPPLE to send links  
```-d, --description```  
	Description of analysis  
```-f, --snpfile```  
	Input file  
```-i, --input```  
	Type of input.  
	S: SNP  
	R: Region  
	C: Combination  
	GR: Gene-Region  
	G: Gene  
	Default is Gene  

Optional Arguments  

```-w, --wait```  
	Number of minutes to wait between checking results. Longer wait times are suggested for large jobs.  
	Default is 1.  
```-p, --permutation```  
	Number of permuations to run. Default is 1000.  
```-g, --genome```  
	Genome assembly to use.  
	19: Hg19/HapMap  
	18: Hg18/HapMap  
	1kg: Hg19/1000Genomes SNPs  
	Default is Hg19/HapMap  
```-c, --ci_cutoff```  
	Common Interactor Binding Degree Cutoff  
	Potential values are 2-10, default is 2.  
```-us, --upstream```  
	Define an upstream gene regulatory region. Can only be used with SNP and region input.  
	Measured in kb, default is 50.  
```-ds, --downstream```  
	Define an downstream gene regulatory region. Can only be used with SNP and region input.  
	Measured in kb, default is 50.  
```-n, --nearest```  
	Use nearest gene for SNP input, instead of all genes in the chosen region  
```-gs, --gene_specified```  
	Genes to specify as causal. Should be a filename.  
```-pl, --plot```  
	Plot the network results.  
```-cp, --color_plot```  
	Color the network by p-value  
```-s, --simplify_plot```  
	Simplify the network plot  
```-z, --zoom_to_gene```  
	Specify genes to zoom in on. Should be filename  
