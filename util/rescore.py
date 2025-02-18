"""Rescore an existing RMF file using the same scoring function that
   was used in the modeling."""

import IMP
import IMP.core
import IMP.algebra
import IMP.atom
import IMP.container

import IMP.pmi1.mmcif
import IMP.pmi1.metadata
import IMP.pmi1.restraints.crosslinking
import IMP.pmi1.restraints.stereochemistry
import IMP.pmi1.restraints.em
import IMP.pmi1.restraints.basic
import IMP.pmi1.representation
import IMP.pmi1.tools
import IMP.pmi1.samplers
import IMP.pmi1.output
import IMP.pmi1.macros

import os
import ast

rmf_file = '../analysis/clustering/kmeans_weight_500_4/cluster.0/0.rmf3'

# The corresponding stat file
stat_file = os.path.join(os.path.dirname(rmf_file), 'stat.out')
# The RMF file is assumed to be the top-scoring model from the cluster,
# i.e. the first line in the stat file
stat = ast.literal_eval(open(stat_file).readline())
# Get optimized nuisance values for crosslink restraints
optimized_sigma_dss = float(stat['ISDCrossLinkMS_Sigma_1_DSS'])
optimized_psi_01_dss = float(stat['ISDCrossLinkMS_Psi_0.1_DSS'])
optimized_psi_001_dss = float(stat['ISDCrossLinkMS_Psi_0.01_DSS'])

# setting up parameters

rbmaxtrans = 2.00
fbmaxtrans = 3.00
rbmaxrot=0.04
outputobjects = []
sampleobjects = []

# setting up topology

m = IMP.Model()
simo = IMP.pmi1.representation.Representation(m,upperharmonic=True,disorderedlength=False)

fastadirectory="../sampling/fasta_files/"
pdbdirectory="../sampling/pdb_files/"
gmmdirectory="../sampling/model_gmm_files/"
headpdb="head_module_em_aligned_translated.pdb"

xlmsdirectory="../sampling/CXMS_files/"


       # compname  hier_name    color         fastafile              fastaid          pdbname      chain    resrange      read    "BEADS"ize rigid_body super_rigid_body emnum_components emtxtfilename  emmrcfilename chain of super rigid bodies

domains_head=   [("med6",  "med6_1",    0.10,  fastadirectory+"med6.fasta",  "med6",   pdbdirectory+headpdb,   "G",   (1,295,0),     None,       20,      None,         None,     15,   gmmdirectory+"med6_1.txt",  gmmdirectory+"med6_1.mrc",   None),
                 ("med8",  "med8_1",    0.20,  fastadirectory+"med8.fasta",  "med8",   pdbdirectory+headpdb,   "C",   (1,223,0),     None,       20,      None,         None,     10,   gmmdirectory+"med8_1.txt",  gmmdirectory+"med8_1.mrc",   None),
                 ("med11", "med11_1",   0.30,  fastadirectory+"med11.fasta", "med11",  pdbdirectory+headpdb,   "A",   (1,115,0),     None,       20,      None,         None,     6,    gmmdirectory+"med11_1.txt", gmmdirectory+"med11_1.mrc",   None),
                 ("med17", "med17_3",   0.40,  fastadirectory+"med17.fasta", "med17",  pdbdirectory+headpdb,   "B",   (123,687,0),   None,       20,      None,         None,     28,   gmmdirectory+"med17_3.txt", gmmdirectory+"med17_3.mrc",   None),
                 ("med18", "med18_1",   0.50,  fastadirectory+"med18.fasta", "med18",  pdbdirectory+headpdb,   "E",   (1,307,0),     None,       20,      None,         None,     15,   gmmdirectory+"med18_1.txt",  gmmdirectory+"med18_1.mrc",   None),
                 ("med20", "med20_1",   0.60,  fastadirectory+"med20.fasta", "med20",  pdbdirectory+headpdb,   "F",   (1,210,0),     None,       20,      None,         None,     20,   gmmdirectory+"med20_1.txt",  gmmdirectory+"med20_1.mrc",   None),
                 ("med22", "med22_1",   0.70,  fastadirectory+"med22.fasta", "med22",  pdbdirectory+headpdb,   "D",   (1,121,0),     None,       20,      None,         None,     6,    gmmdirectory+"med22_1.txt",  gmmdirectory+"med22_1.mrc",   None)]

domains_middle= [("med4",  "med4_1",    0.10,  fastadirectory+"med4.fasta",  "med4",   pdbdirectory+'med4_med9.pdb',   "D",    (1,131,0),    True,       20,      1,         [19,1,2],     2,   gmmdirectory+"med4_1.txt",  gmmdirectory+"med4_1.mrc",   [0]),
                 ("med4",  "med4_2",    0.10,  fastadirectory+"med4.fasta",  "med4",   "BEADS",               None,   (132,284,0),  True,       20,      2,         [19,1,2],     0,   None,  None,   [0]),
                 ("med7",  "med7_1",    0.20,  fastadirectory+"med7.fasta",  "med7",   pdbdirectory+'med7n_med31.pdb',   "A",    (1,84,0),     True,       20,      3,         [19,1,3],     2,   gmmdirectory+"med7_1.txt",  gmmdirectory+"med7_1.mrc",   [1]),
                 ("med7",  "med7_2",    0.20,  fastadirectory+"med7.fasta",  "med7",   "BEADS",               None,   (85,111,0),   True,       20,      4,         [19,1,3],     1,   None,  None,   [1]),
                 ("med7",  "med7_3",    0.20,  fastadirectory+"med7.fasta",  "med7",   pdbdirectory+'med7c_med21.pdb',   "A",    (112,222,0),  True,       20,      5,         [19,1,3],     2,   gmmdirectory+"med7_3.txt",  gmmdirectory+"med7_3.mrc",   [1]),
                 ("med9",  "med9_1",    0.30,  fastadirectory+"med9.fasta",  "med9",   "BEADS",               None,   (1,64,0),     True,       20,      6,         [19,1,4],     0,   None,  None,   [2]),
                 ("med9",  "med9_6",    0.30,  fastadirectory+"med9.fasta",  "med9",   pdbdirectory+'med4_med9.pdb',   "I",    (65,149,0),   True,       20,      1,         [19,1,4],     2,   gmmdirectory+"med9_6.txt",  gmmdirectory+"med9_6.mrc",   [2]),
                 ("med31", "med31_1",   0.80,  fastadirectory+"med31.fasta", "med31",  pdbdirectory+'med7n_med31.pdb',   "B",    (1,127,0),    True,       20,      3,         [19,1,5],     3,   gmmdirectory+"med31_1.txt",  gmmdirectory+"med31_1.mrc",   None),
                 ("med21", "med21_1",   0.50,  fastadirectory+"med21.fasta", "med21",  pdbdirectory+'med7c_med21.pdb',   "B",    (1,140,0),    True,       20,      5,         [19,1,6],     3,   gmmdirectory+"med21_1.txt",  gmmdirectory+"med21_1.mrc",   None),
                 ("med10", "med10_1",   0.60,  fastadirectory+"med10.fasta", "med10",  "BEADS",               None,   (1,157,0),    True,       20,      8,         [19,1,7],     0,   None,  None,   [5]),
                 ("med1",  "med1_1",    0.70,  fastadirectory+"med1.fasta",  "med1",   "BEADS",               None,   (1,566,0),    True,       20,      9,         [19,1,8],     0,   None,  None,   [6]),
                 ("med14",  "med14_1",  1.00,  fastadirectory+"med14.fasta", "med14",  "BEADS",               None,   (1,711,0),    True,       20,      10,        [19,1,9],     0,   None,  None,   [7]),
                 ("med19",  "med19_1",  0.90,  fastadirectory+"med19.fasta", "med19",  "BEADS",               None,   (1,220,0),    True,       20,      11,        [19,1,10],    0,   None,  None,   [8]),
                 ("med17", "med17_2",   0.40,   fastadirectory+"med17.fasta", "med17",  "BEADS",               None,   (1,122,0),   True,        20,      12,         [19,1,11],    0,   None,  None,   [9])]

domains_tail=   [("med2",  "med2_1",    0.00,  fastadirectory+"med2.fasta",  "med2",   "BEADS",               None,   (1,436,0),     True,       40,      13,         [19,12,13],     0,   None,  None,   [13]),
                 ("med3",  "med3_1",    0.20,  fastadirectory+"med3.fasta",  "med3",   "BEADS",               None,   (1,401,0),     True,       40,      14,         [19,12,14],     0,   None,  None,   [14]),
                 ("med5",  "med5_1",    0.40,  fastadirectory+"med5.fasta",  "med5",   "BEADS",               None,   (1,1146,0),    True,      40,      15,         [19,12,15],     0,   None,  None,   [15]),
                 ("med15", "med15_1",   0.60,  fastadirectory+"med15.fasta", "med15",  "BEADS",               None,   (1,1094,0),    True,      40,      16,         [19,12,16],     0,   None,  None,   [16]),
                 ("med16", "med16_1",   0.80,  fastadirectory+"med16.fasta", "med16",  pdbdirectory+"med16.NTD.phyre.model.pdb",    "A",   (8,538,0),    True,      40,      19,         [19,12,17],     10,   gmmdirectory+"med16_1.txt",  gmmdirectory+"med16_1.mrc",   [20]),
                 ("med16", "med16_2",   0.80,  fastadirectory+"med16.fasta", "med16",  "BEADS",               None,   (539,986,0),     True,       40,      17,         [19,12,17],     0,   None,  None,   [17]),
                 ("med14",  "med14_2",  1.00,  fastadirectory+"med14.fasta", "med14",  "BEADS",               None,   (712,1082,0),  True,        40,      10,         [19,1,9],     0,   None,  None,   [7])]




domains=domains_head+domains_middle+domains_tail

# build model using RMF file from previous modeling run
bm=IMP.pmi1.macros.BuildModel1(simo)
bm.build_model(domains, rmf_file=rmf_file)
#bm.scale_bead_radii(40,0.8)

resdensities_middle=bm.get_density_hierarchies([t[1] for t in domains_middle])
resdensities_tail  =bm.get_density_hierarchies([t[1] for t in domains_tail])

# defines the movers

simo.set_rigid_bodies_max_rot(rbmaxrot)
simo.set_floppy_bodies_max_trans(fbmaxtrans)
simo.set_rigid_bodies_max_trans(rbmaxtrans)

outputobjects.append(simo)
sampleobjects.append(simo)

# scoring function

ev = IMP.pmi1.restraints.stereochemistry.ExcludedVolumeSphere(simo,resolution=10)
ev.add_to_model()
outputobjects.append(ev)


# here we have a protocol for clean datesets, 
# when the model is flexible and there are not large rigid parts
columnmap={}
columnmap["Protein1"]='pep1.accession'
columnmap["Protein2"]='pep2.accession'
columnmap["Residue1"]='pep1.xlinked_aa'
columnmap["Residue2"]='pep2.xlinked_aa'
columnmap["IDScore"]='mod_type'
columnmap["XLUniqueID"]='spec_id'

ids_map=IMP.pmi1.tools.map()
ids_map.set_map_element("intra_mod",0.01)
ids_map.set_map_element("inter_mod",0.1)

xl = IMP.pmi1.restraints.crosslinking.ISDCrossLinkMS(simo,
                                   xlmsdirectory+"/full_med_splitmods.txt",
                                   length=21.0,
                                   slope=0.01,
                                   columnmapping=columnmap,
                                   ids_map=ids_map,
                                   resolution=1.0,
                                   label="DSS",
                                   csvfile=True)
xl.add_to_model()
sampleobjects.append(xl)
outputobjects.append(xl)
xl.set_psi_is_sampled(True)

#simo.optimize_floppy_bodies(200)

# middle module em density

middle_mass=sum((IMP.atom.Mass(p).get_mass() for h in resdensities_middle for p in IMP.atom.get_leaves(h)))
gemh = IMP.pmi1.restraints.em.GaussianEMRestraint(resdensities_middle,'../sampling/em_map_files/asturias_middle_module_translated_resampled.mrc.gmm.29.txt',
                                               target_mass_scale=middle_mass,
                                                slope=0.000001,
                                                target_radii_scale=3.0,
                                                representation=simo)

gemh.set_label('middle')
gemh.add_to_model()
gemh.set_weight(100.0)
#gem.center_model_on_target_density(simo)
outputobjects.append(gemh)


# tail module em density

tail_mass=sum((IMP.atom.Mass(p).get_mass() for h in resdensities_tail for p in IMP.atom.get_leaves(h)))
gemt = IMP.pmi1.restraints.em.GaussianEMRestraint(resdensities_tail,'../sampling/em_map_files/asturias_tail_module_translated_resampled.mrc.gmm.49.txt',
                                               target_mass_scale=tail_mass,
                                                slope=0.000001,
                                                target_radii_scale=3.0,
                                                representation=simo)

gemt.set_label('tail')
gemt.add_to_model()
gemt.set_weight(100.0)
#gem.center_model_on_target_density(simo)
outputobjects.append(gemt)

# Set nuisance values (from stat file)
for key in xl.sigma_dictionary:
    sigma=xl.sigma_dictionary[key][0]
    sigma.set_scale(optimized_sigma_dss)
psi=xl.psi_dictionary[0.1][0]
psi.set_scale(optimized_psi_01_dss)
psi=xl.psi_dictionary[0.01][0]
psi.set_scale(optimized_psi_001_dss)

# Evaluate the score
print(IMP.pmi1.tools.get_restraint_set(m).evaluate(False))

# Print out EM score and CCC
print(gemh.get_output())
print(gemt.get_output())
