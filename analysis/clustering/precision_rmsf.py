import IMP
import IMP.pmi
import IMP.pmi.analysis
import IMP.pmi.output
import IMP.atom
import glob
import sys
import itertools

test_mode='--test' in sys.argv # runs on the first 10 structures to test if it runs smoothly

# specify the cluster directory to be analysed

#root_cluster_directory='kmeans_500_10'
root_cluster_directory='kmeans_weight_500_1'

# choose whatever selection for the precision calculation

selection_dictionary={"med6":["med6"],
                  "med8":["med8"],
                  "med11":["med11"],
                  "med17":["med17"],
                      #"med17Nterm":[(1,122,"med17")],
                      #"med17Cterm":[(123,687,"med17")],
                  "med18":["med18"],
                  "med20":["med20"],
                  "med22":["med22"],
                  "med4":["med4"],
                  "med7":["med7"],
                  "med9":["med9"],
                  "med31":["med31"],
                  "med21":["med21"],
                  "med10":["med10"],
                  "med1":["med1"],
                  "med14":["med14"],
                      #"med14Nterm":[(1,711,"med14")],
                      #"med14Cterm":[(712,1082,"med14")],
                  "med19":["med19"],
                  "med2":["med2"],
                  "med3":["med3"],
                  "med5":["med5"],
                  "med15":["med15"],
                  "med16":["med16"],
                  "middle":["med1","med4","med7","med9","med10","med14","med19","med21","med31"],
                  "tail":["med2","med3","med5","med15","med16"]}


#####################################################################
# don't change anything below
rmfs=[]
frames=[]
clusterdirectories=glob.glob(root_cluster_directory+'/cluster.*/')

if test_mode:
  # runs on the first 10 structures to test if it runs smoothly
  for clusterdirectory in clusterdirectories:
      rmfs.append(glob.glob(clusterdirectory+'/*.rmf3')[0::10])
      frames.append([0]*len(rmfs[-1]))
else:
  for clusterdirectory in clusterdirectories:
      rmfs.append(glob.glob(clusterdirectory+'/*.rmf3')[0::10])
      frames.append([0]*len(rmfs[-1]))
 
model=IMP.Model()
pr=IMP.pmi.analysis.Precision(model,resolution=1,selection_dictionary=selection_dictionary)
pr.set_precision_style('pairwise_rmsd')

for n in range(len(rmfs)):
    pr.add_structures(zip(rmfs[n],frames[n]),clusterdirectories[n])


#for pair in itertools.product(range(len(rmfs)), repeat=2):
#    clus1=pair[0]
#    clus2=pair[1]
#    pr.get_precision(root_cluster_directory+"/precision."+str(clus1)+"."+str(clus2)+".out",
#                     clusterdirectories[clus1],
#                     clusterdirectories[clus2],
#                     skip=1)

for n in range(len(rmfs)):
    pr.get_rmsf(clusterdirectories[n],clusterdirectories[n]+"/",skip=1,set_plot_yaxis_range=(0,100.0))
