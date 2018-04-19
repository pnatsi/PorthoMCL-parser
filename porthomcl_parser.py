'''
orthomcl_parser.py

This is a script to parse .tsv files with groups of ortholog genes as rows.
It is most convenient to parse the 8.all.ort.group file that is the output file of orthologs from a PorthoMCL run.
Any other files with the same format will work too.

PorthoMCL (Tabari & Su, 2017) is a parallel re-implementation of the OrthoMCL algorithm.
More info can be found in https://github.com/etabari/PorthoMCL 
A detailed manual of PorthoMCL can be found in https://github.com/etabari/PorthoMCL/wiki/Manual

The goal of this script is to isolate all 1-1 groups with the preferred number of species.
These groups can be used in a phylogenetic tree analysis.

Created by Paschalis Natsidis (pnatsidis@hotmail.com) as part of his Master thesis in HCMR, Heraklion.
'''


import argparse
import timeit
import sys

start = timeit.default_timer()

#ARGUMENT DEFINING
usage = "A script to easily parse PorthoMCL (Tabari & Su, 2017) output file '8.all.ort.group' or any other file with the same format (.tsv files with one group per row and one gene per tab-separated column).\n\nPorthoMCL (Tabari & Su, 2017) is a parallel re-implementation of the OrthoMCL algorithm.\nMore info can be found in https://github.com/etabari/PorthoMCL\nA detailed manual of PorthoMCL can be found in https://github.com/etabari/PorthoMCL/wiki/Manual\n\n\nThe goal of this script is to isolate all 1-1 groups with the preferred number of species. \nThese groups can be used in a phylogenetic tree analysis."
toolname = "orthomcl_parser"
footer = "AUTHOR: Paschalis Natsidis (pnatsidis@hotmail.com); \n@Hellenic Centre for Marine Research; May 2018"

parser = argparse.ArgumentParser(description = usage, prog = toolname, epilog = footer, formatter_class=argparse.RawDescriptionHelpFormatter,)

parser.add_argument('-i', metavar = 'filename', dest = 'orthogroups', required = True,
                                        help = 'File with one group of orthologs per row. Names of genes must be written in tab-separated columns (one gene name per column)')
parser.add_argument('-t', metavar = 'filename', dest = 'taxon_list', required = True,
                                        help = 'File with all 3-letter taxa codes that were created in the orthomclAdjustFasta step')
parser.add_argument('-min', metavar = 'integer', dest = 'minimum', type = int, required = False,
                                        help = 'Minimum number of taxa to be represented in the output 1-1 groups')

args = parser.parse_args()

######## READ INPUT ARGUMENTS #########
orthologs_file = args.orthogroups
taxon_file = args.taxon_list
minimum_taxa = args.minimum

                    
orthogroups_to_return = []
species = []



#########  READ TAXON LIST ############
try:
    with open(taxon_file, 'r') as tlf:
        for line in tlf.readlines():
            taxon = line.strip()
            species.append(taxon)
except IOError:
    print("\nNo such taxon list file exists. Exiting...\n\n")
    sys.exit()



### CHECK IF -MIN ARGUMENT IS VALID ###
number_of_species = len(species)
if minimum_taxa > number_of_species:
    print("\nNumber of minimum taxa provided is larger than the total number of taxa in taxon list provided.\n\nPlease change -min argument to be smaller than or equal to " + str(number_of_species) + " \n\n\nExiting...\n\n")
    sys.exit()

if not minimum_taxa:
    minimum_taxa = number_of_species


######## READ ORTHOGROUPS FILE ########
try:
    with open(orthologs_file, 'r') as olf:
        for line in olf.readlines():
            orthogroup = line.strip().split("\t")
            orthogroup_size = len(orthogroup)
            if orthogroup_size <= number_of_species and orthogroup_size >= minimum_taxa:
                orthogroups_to_return.append(orthogroup)
except IOError:
    print("\nNo such orthogroups file exists. Exiting...\n\n")
    sys.exit()

taxa_instances = {}
final_groups = []
counter = 0


####### RETRIEVE 1-1 ORTHOGROUPS #######
for group in orthogroups_to_return:
    for taxon in species:
        taxa_instances[taxon] = 0                       #initialize all instances with zero
        for entry in group:     
            if taxon in entry:                          #check orthogroup entries and count
                taxa_instances[taxon] += 1              #instances of each taxon

    counts = set(taxa_instances.values())               #check if the set of instances is [0,1]
    counts_list = list(counts)                          #or [1] so we isolate all 1-1 groups 

    if counts_list == [0,1] or counts_list == [1]:      #if yes, keep group in the final list
        counter += 1
        final_groups.append(group)
print("\nTotal number of 1-1 orthogroups with " + str(minimum_taxa) + " to " + str(number_of_species) + " species: " + str(counter) + "\n\nAll " + str(counter) + " orthogroups are written in final_groups_orthomcl.tsv (one group per row)\n\nExiting...\n\n")


output = open('final_groups_orthomcl.tsv', 'w')         #write a file with all specified groups
                                                        #one group per row
for group in final_groups:
    for entry in group:
        output.write(entry + "\t")
    output.write("\n")
    
