import os
import matplotlib
matplotlib.use('Agg')
import sys
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]),
                                'XL_analysis', 'src'))
import xltable
import glob

def get_median_rmf(rmfsfile):
   rf=open(rmfsfile)
   for nl,l in enumerate(rf):
      if nl==2:
         tupletext=l.replace("All"," ").replace("centroid"," ").replace("rmf "," ").replace("name"," ").replace("\n"," ")
         (medianrmf,frame)=eval(tupletext)
   return medianrmf,frame


### data labels
ddir='data/'

cluster_directory="kmeans_weight_500_4/cluster.0/"

field_map={}
field_map["prot1"]='pep1.accession'
field_map["prot2"]='pep2.accession'
field_map["res1"]='pep1.xlinked_aa'
field_map["res2"]='pep2.xlinked_aa'
field_map["score"]='dvals'



prot_list=[       "med6",
                  "med8",
                  "med11",
                  "med17",                  
                  "med18",
                  "med20",
                  "med22", 
                  "med1",                                   
                  "med4",
                  "med7",
                  "med9",
                  "med10",
                  "med14",   
                  "med19",                                  
                  "med21",                                   
                  "med31",
                  "med2",
                  "med3",
                  "med5",
                  "med15",
                  "med16"]

### loading data

#indicate the rmsf.dat file to get the median rmf structure
rmsffile=cluster_directory+"/rmsf.dat"
medianrmf,frame=(cluster_directory+"94.rmf3",0)

                                    

xlt=xltable.XLTable(contact_threshold=30)
xlt.load_crosslinks("../../sampling/CXMS_files/full_med_splitmods.txt",
                    field_map)
for prot in prot_list:
    xlt.load_sequence_from_fasta_file(fasta_file="../../sampling/fasta_files/"+prot+".fasta",
                                  id_in_fasta_file=prot,
                                  protein_name=prot)  

for rmf in glob.glob(cluster_directory+"*.rmf3")[0::10]:
    xlt.load_rmf_coordinates(rmf,0,prot_list)

### creating contact map
xlt.setup_contact_map()

### plotting

xlt.plot_table(prot_listx=prot_list,
           prot_listy=prot_list,
           alphablend=0.2,
           scale_symbol_size=1.5,
           gap_between_components=50,
           filename=cluster_directory+"/XL_table.pdf",
           contactmap=True,
           crosslink_threshold=35.0,
           display_residue_pairs=False)
