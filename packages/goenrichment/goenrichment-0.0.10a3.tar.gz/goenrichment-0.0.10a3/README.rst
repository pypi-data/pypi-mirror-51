GO Enrichment package
---------------------

This package execute GO enrichment analysis froma list of gene names using a precomputed database.
The GO terms are analyze using a hypergeometric test.

GO enrichment database
----------------------

The GO graph structure is created from the Gene Ontology OBO 
file http://current.geneontology.org/ontology/go.obo

NCBI gene
---------

The NCBI gene database is used to include genes to the GO terms graph. The required files are:
ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/gene_info.gz and
ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2go.gz

These files can be filter for a specific taxonomy id. This example is for human: 9606

    gunzip -c gene_info.gz | grep -P "^9606\t" > gene_info_${taxid}
    gzip gene_info_${taxid}
    gunzip -c gene2go.gz | grep -P "^9606\t" > gene2go_${taxid}
    gzip gene2go_${taxid}


Uniprot GOA
-----------

The Uniprot GOA files can be also used to add more genes to the GO graph.
The complete file is: 
ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/UNIPROT/goa_uniprot_all.gaf.gz

Uniprot GOA also include some pre-filtered organism: ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/

TSV file: gene\<tab\>GO term
----------------------------

Any TSV file with the relationship between gene names and GO term can also be included into the database.
The file just need to include in the first column the gene name and in the second column the GO term. 
Any other extra column will be ignored. 

Ensembl BioMart
---------------

The Ensembl data can be alos include using their BioMart tool. Go to the Ensembl Biomart website: 
http://useast.ensembl.org/biomart/.
Using this tool a TSV file can be generated with
gene names in the first column and GO term in the second column.

Database creation
-----------------

This example is for human. Please, note all input files should be gzipped.

    python ./bin/goenrichDB.py --gene_info gene_info.gz --gene2go gene2go.gz --goa_uniprot goa_uniprot_all.gaf.gz --gobo go.obo --taxid 9606 --goenrichDB goenrichDB_20190419.pickle


Usage
-----


    usage: goenrichDB.py [-h] [--gene_info GENE_INFO] [--gene2go GENE2GO]
                         [--tsv TSV] [--goenrichDB GOENRICHDB]
                         [--goa_uniprot GOA_UNIPROT] [--gobo GOBO] [--taxid TAXID]
                         -o O

    Creates pickle data structure used by "goenrich.py"

    optional arguments:
        -h, --help            show this help message and exit
        --gene_info GENE_INFO
                            NCBI gene_info file
        --gene2go GENE2GO     NCBI gene2go file
        --tsv TSV             TSV file with at least two columns: Gene_name<tab>GO
                            terms
        --goenrichDB GOENRICHDB
                            Previous created goenrich pickle file. The new genes
                            will be added to this database
        --goa_uniprot GOA_UNIPROT
                            Uniprot GOA file GAF format
        --gobo GOBO           UGO Obo file from Gene Ontology
        --taxid TAXID         Process genes for tax id if it is possible
        -o O                  Pickle output file name


Pre-computed databases
----------------------

We offer some pre-computed database https://ftp.ncbi.nlm.nih.gov/pub/goenrichment/

Go enrichment analysis
----------------------

The analysis is executed using the script `goenrich.py`. The input file is a text file with 
one gene name per line.


    ./bin/goenrich.py --goenrichDB gene2GO_human.pickle -i query.tsv -o goenrich.tsv


The `gene2GO_human.pickle` can be downloaded from https://ftp.ncbi.nlm.nih.gov/pub/goenrichment/goenrichDB_human.pickle

    usage: goenrich.py [-h] -i I -o O [--goenrichDB GOENRICHDB]
                       [--min_category_depth MIN_CATEGORY_DEPTH]
                       [--min_category_size MIN_CATEGORY_SIZE]
                       [--max_category_size MAX_CATEGORY_SIZE] [--alpha ALPHA]
    
    Calculate GO enrichment from a list of genes. Default database organism: human
    
    optional arguments:
        -h, --help            show this help message and exit
        -i I                  Input list of gene names
        -o O                  TSV file with all results
        --goenrichDB GOENRICHDB
                            Gene2GO pickle file created with "goenrichDB.py". If
                            not provided the database is loaded from:
        --min_category_depth MIN_CATEGORY_DEPTH
                            Min GO term graph depth to include in the report.
                            Default: 4
        --min_category_size MIN_CATEGORY_SIZE
                            Min number of gene in a GO term to include in the
                            report. Default: 3
        --max_category_size MAX_CATEGORY_SIZE
                            Max number of gene in a GO term to include in the
                            report. Default: 500
        --alpha ALPHA         Alpha value for p-value correction. Default: 0.05


Requirements
------------
 
 * Python 3.7
     * numpy
     * scipy
     * statsmodels
     * pandas
     * networkx


Public Domain notice
--------------------

National Center for Biotechnology Information.

This software is a "United States Government Work" under the terms of the United States
Copyright Act. It was written as part of the authors' official duties as United States
Government employees and thus cannot be copyrighted. This software is freely available
to the public for use. The National Library of Medicine and the U.S. Government have not
 placed any restriction on its use or reproduction.

Although all reasonable efforts have been taken to ensure the accuracy and reliability
of the software and data, the NLM and the U.S. Government do not and cannot warrant the
performance or results that may be obtained by using this software or data. The NLM and
the U.S. Government disclaim all warranties, express or implied, including warranties
of performance, merchantability or fitness for any particular purpose.

Please cite NCBI in any work or product based on this material.
