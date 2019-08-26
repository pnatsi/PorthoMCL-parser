# PorthoMCL_parser.py

This is a script to parse .tsv files with groups of ortholog genes as rows.                                                                    
It is most convenient to parse the 8.all.ort.group file that is the output file of orthologs from a PorthoMCL run.                             
Any other files with the same format will work too.                                                                                            
                                                                                                                                               
PorthoMCL (Tabari & Su, 2017) is a parallel re-implementation of the OrthoMCL algorithm.                                                       
More info can be found in https://github.com/etabari/PorthoMCL                                                                                 
A detailed manual of PorthoMCL can be found in https://github.com/etabari/PorthoMCL/wiki/Manual                                                
                                                                                                                                               
The goal of this script is to isolate all 1-1 groups with the preferred number of species.                                                     
These groups can be used in a phylogenetic tree analysis.                                                                                      
 
## EXAMPLE USAGE

The script can be used as following:
```
   python porthomcl_parser.py -i example.tsv -t taxon_list -min 27
```
will return a file with all 1-1 groups with a representation of at least 27 species
 
 
## INPUT FILES FORMAT
The file with the orthogroups must be in the following format:
```
taxon1gene1 taxon1gene2 taxon1gene3 taxon2gene1 taxon3gene2 ...
taxon1gene4 taxon4gene1 taxon5gene1 ... 
...
```   
All gene names are tab-separated, and each row represents an orthogroup

The file with the list of taxa must be in the following format:
```
taxon1
taxon2
taxon3
taxon4
...
```
