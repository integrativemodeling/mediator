import IMP
import IMP.pmi1
import IMP.pmi1.macros
import sys

model=IMP.Model()

# initialize the macro

mc=IMP.pmi1.macros.AnalysisReplicaExchange0(model,
                                        stat_file_name_suffix="stat",     # don't change
                                        merge_directories=[ # change this list splitting the runs or adding new runs
                 "../../sampling/modeling/",
                 # These runs were used in the actual publication, and are
                 # archived as run20.tar.xz, run28.tar.xz and run31.tar.xz
                 # at https://doi.org/10.5281/zenodo.802915
                 "../../run20/modeling.split_density.scale_radii.two_bayesian_classes-1.1",
							   "../../run20/modeling.split_density.scale_radii.two_bayesian_classes-1.2",
							   "../../run20/modeling.split_density.scale_radii.two_bayesian_classes-1.3",
							   "../../run20/modeling.split_density.scale_radii.two_bayesian_classes-1.4",
							   "../../run28/modeling.split_density.scale_radii.two_bayesian_classes-1.5",
                 "../../run28/modeling.split_density.scale_radii.two_bayesian_classes-1.6",
							   "../../run28/modeling.split_density.scale_radii.two_bayesian_classes-1.7",
							   "../../run28/modeling.split_density.scale_radii.two_bayesian_classes-1.8",                                                                              
                 "../../run31/modeling.split_density.scale_radii.two_bayesian_classes-1.9",
							   "../../run31/modeling.split_density.scale_radii.two_bayesian_classes-1.10",
							   "../../run31/modeling.split_density.scale_radii.two_bayesian_classes-1.11",
							   "../../run31/modeling.split_density.scale_radii.two_bayesian_classes-1.12",
							   "../../run31/modeling.split_density.scale_radii.two_bayesian_classes-1.13",
							   "../../run31/modeling.split_density.scale_radii.two_bayesian_classes-1.14",
							   "../../run31/modeling.split_density.scale_radii.two_bayesian_classes-1.15",
							   "../../run31/modeling.split_density.scale_radii.two_bayesian_classes-1.16",
							   "../../run31/modeling.split_density.scale_radii.two_bayesian_classes-1.17",
							   "../../run31/modeling.split_density.scale_radii.two_bayesian_classes-1.18",
							   "../../run31/modeling.split_density.scale_radii.two_bayesian_classes-1.19",
							   "../../run31/modeling.split_density.scale_radii.two_bayesian_classes-1.20"],                                                                                                    
                                        global_output_directory="./output/") # don't change
if '--mmcif' in sys.argv:
    mc.test_mode = simo.dry_run
    for po in simo.protocol_output:
        mc.add_protocol_output(po)

# fields that have to be extracted for the stat file

feature_list=["ISDCrossLinkMS_Distance_intrarb",
              "ISDCrossLinkMS_Distance_interrb",
              "ISDCrossLinkMS_Data_Score",
              "GaussianEMRestraint_None",
              "SimplifiedModel_Linker_Score_None",
              "ISDCrossLinkMS_Psi",
              "ISDCrossLinkMS_Sigma"]

# Dictionary of densities to be calculated
# the key is the name of the file and the value if the selection
# example:
#              {"med17-CTD":[(200,300,"med17")],"med17-CTD.med14":[(200,300,"med17"),"med14"]   }

reduced_density_dict={"med6":["med6"],
                  "med8":["med8"],
                  "med11":["med11"],
                  "med17":["med17"],
                  "med117":[(1,122,"med17")],#med17-Nterm
		  "med217":[(123,687,"med17")],#med17-Cterm
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
		  "med314":[(1,711,"med14")],#med14-Nterm
		  "med414":[(712,1082,"med14")],#med14-Cterm
                  "med19":["med19"],
                  "med2":["med2"],
                  "med3":["med3"],
                  "med5":["med5"],
                  "med15":["med15"],
                  "med16":["med16"]}

# list of component names needed to calculate the RMSD for the clustering

names=["med6",
                  "med8",
                  "med11",
                  "med17",
                  "med18",
                  "med20",
                  "med22",
                  "med4",
                  "med7",
                  "med9",
                  "med31",
                  "med21",
                  "med10",
                  "med1",
                  "med14",
                  "med19",
                  "med2",
                  "med3",
                  "med5",
                  "med15",
                  "med16"]

components_names={}
for i in names:
    components_names[i]=i

prefilter=1818
if '--test' in sys.argv:
    prefilter=10000
nclusters=4                                       # number of clusters needed by kmeans
mc.clustering("SimplifiedModel_Total_Score_None",  # don't change, field where to find the score
              "rmf_file",                          # don't change, field where to find the path for the rmf_file
              "rmf_frame_index",                   # don't change, field for the frame index
              prefiltervalue=prefilter,          # prefilter the models by score
              number_of_best_scoring_models=500,   # number of models to be clustered
              alignment_components=None,           # don't change, (list of proteins you want to use for structural alignment
              rmsd_calculation_components=components_names, # list of proteins used to calculated the rmsd
              distance_matrix_file="distance.rawmatrix.pkl", # save the distance matrix
              outputdir="kmeans_weight_500_"+str(nclusters)+"/",  # directory name for the clustering
              feature_keys=feature_list,                     # extract these fields from the stat file
              load_distance_matrix_file=False,               # skip the matrix calcuklation and read the precalculated matrix
              skip_clustering=False,                         # skip clustering
              display_plot=False,                            # display the heat map plot of the distance matrix
              exit_after_display=False,                      # exit after having displayed the distance matrix plot
              get_every=1,                                   # skip structures for faster computation
              number_of_clusters=nclusters,                  # number of clusters to be used by kmeans algorithm
              voxel_size=3.0,                                # voxel size of the mrc files
              density_custom_ranges=reduced_density_dict)    # setup the list of densities to be calculated

if '--mmcif' in sys.argv:
    # Point to deposited ensembles in DCD format
    dcds = []
    for i in range(nclusters):
        r = ihm.location.Repository(doi="10.5281/zenodo.802915",
             url="https://zenodo.org/record/802915/files/cluster.%d.dcd" % i)
        dcds.append(ihm.location.OutputFileLocation(path='.', repo=r,
                            details="All models in cluster %d" % (i+1)))
    for po in simo.protocol_output:
        if hasattr(po, 'set_ensemble_file'):
            for i, dcd in enumerate(dcds):
                po.set_ensemble_file(i, dcd)
