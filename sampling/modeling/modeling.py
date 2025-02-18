import IMP
import IMP.core
import IMP.algebra
import IMP.atom
import IMP.container

import ihm
try:
    import ihm.reference
except ImportError:
    pass
import IMP.pmi1.mmcif
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
import sys
sys.path.append('../../util/')
import make_archive

# setting up parameters

rbmaxtrans = 2.00
fbmaxtrans = 3.00
rbmaxrot=0.04
outputobjects = []
sampleobjects = []

# setting up topology

m = IMP.Model()
simo = IMP.pmi1.representation.Representation(m,upperharmonic=True,disorderedlength=False)

# Protein Prospector was used to assign the CX-MS data
simo.add_metadata(ihm.Software(
          name='Protein Prospector', classification='mass spectrometry',
          description='Proteomics tools for mining sequence databases '
                      'in conjunction with Mass Spectrometry experiments.',
          version='5.13.1',
          location='http://prospector.ucsf.edu/'))
# We used Situs to dock the Head module into an EM map
s = ihm.Software(
          name='Situs', classification='density map fitting',
          description='Modeling of atomic resolution structures into '
                      'low-resolution density maps',
          version='2.7',
          location='http://situs.biomachina.org/')
if hasattr(s, 'citation'):
    s.citation = ihm.Citation(
        pmid='22505255', title='Conventions and workflows for using Situs.',
        journal='Acta Crystallogr D Biol Crystallogr', volume=68,
        page_range=('344', '351'), year=2012, authors=['Wriggers W'],
        doi='10.1107/S0907444911049791')
simo.add_metadata(s)

simo.add_metadata(ihm.Citation(
          pmid='26402457',
          title="Molecular architecture of the yeast Mediator complex.",
          journal="Elife", volume=4, page_range='e08719',
          year=2015,
          authors=['Robinson PJ', 'Trnka MJ', 'Pellarin R', 'Greenberg CH',
                   'Bushnell DA', 'Davis R', 'Burlingame AL', 'Sali A',
                   'Kornberg RD'],
          doi='10.7554/eLife.08719'))
for subdir, zipname in make_archive.ARCHIVES.items():
    simo.add_metadata(ihm.location.Repository(
          doi="10.5281/zenodo.802915", root="../../%s" % subdir,
          url="https://zenodo.org/record/802915/files/%s.zip" % zipname,
          top_directory=os.path.basename(subdir)))
simo.add_metadata(ihm.location.Repository(
          doi="10.5281/zenodo.802915", root="../..",
          url="https://zenodo.org/record/802915/files/mediator-v1.0.3.zip",
          top_directory="mediator-v1.0.3"))

if '--mmcif' in sys.argv:
    # Record the modeling protocol to an mmCIF file
    po = IMP.pmi1.mmcif.ProtocolOutput(open('mediator.cif', 'w'))
    simo.add_protocol_output(po)
    po.system.title = 'Molecular architecture of the yeast Mediator complex'

simo.dry_run = '--dry-run' in sys.argv

fastadirectory="../fasta_files/"
pdbdirectory="../pdb_files/"
gmmdirectory="../model_gmm_files/"
headpdb="head_module_em_aligned_translated.pdb"

xlmsdirectory="../CXMS_files/"


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

bm=IMP.pmi1.macros.BuildModel1(simo)
bm.build_model(domains)
bm.scale_bead_radii(40,0.8)

resdensities_middle=bm.get_density_hierarchies([t[1] for t in domains_middle])
resdensities_tail  =bm.get_density_hierarchies([t[1] for t in domains_tail])

# randomize the initial configuration

simo.shuffle_configuration(100)

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
# Point to the raw mass spec data and peaklists used to derive the crosslinks.
l = ihm.location.MassIVELocation('MSV000079237',
                         details='All raw mass spectrometry files and '
                                 'peaklists used in the study')
d = ihm.dataset.MassSpecDataset(location=l)
xl.dataset.add_primary(d)

xl.add_to_model()
sampleobjects.append(xl)
outputobjects.append(xl)
xl.set_psi_is_sampled(True)


#simo.optimize_floppy_bodies(200)

# middle module em density

middle_mass=sum((IMP.atom.Mass(p).get_mass() for h in resdensities_middle for p in IMP.atom.get_leaves(h)))
gemh = IMP.pmi1.restraints.em.GaussianEMRestraint(resdensities_middle,'../em_map_files/asturias_middle_module_translated_resampled.mrc.gmm.29.txt',
                                               target_mass_scale=middle_mass,
                                                slope=0.000001,
                                                target_radii_scale=3.0,
                                                representation=simo)
gemh.set_label('middle')
gemh.dataset.location.details = 'Segmented map covering the middle module'
# Point to the original map in EMDB before we processed it
l = ihm.location.EMDBLocation('EMD-2634')
emdb = ihm.dataset.EMDensityDataset(location=l)
gemh.dataset.add_primary(emdb)

gemh.add_to_model()
gemh.set_weight(100.0)
#gem.center_model_on_target_density(simo)
outputobjects.append(gemh)


# tail module em density

tail_mass=sum((IMP.atom.Mass(p).get_mass() for h in resdensities_tail for p in IMP.atom.get_leaves(h)))
gemt = IMP.pmi1.restraints.em.GaussianEMRestraint(resdensities_tail,'../em_map_files/asturias_tail_module_translated_resampled.mrc.gmm.49.txt',
                                               target_mass_scale=tail_mass,
                                                slope=0.000001,
                                                target_radii_scale=3.0,
                                                representation=simo)
gemt.set_label('tail')
gemt.dataset.location.details = 'Segmented map covering the tail module'
# This map was generated from the same EMDB entry as above
gemt.dataset.add_primary(emdb)

gemt.add_to_model()
gemt.set_weight(100.0)
#gem.center_model_on_target_density(simo)
outputobjects.append(gemt)

nframes=20000
if '--test' in sys.argv: nframes=1000
mc1=IMP.pmi1.macros.ReplicaExchange0(m,
                                    simo,
                                    monte_carlo_sample_objects=sampleobjects,
                                    output_objects=outputobjects,
                                    crosslink_restraints=[xl],
                                    monte_carlo_temperature=1.0,
                                    replica_exchange_minimum_temperature=1.0,
                                    replica_exchange_maximum_temperature=2.5,
                                    number_of_best_scoring_models=500,
                                    monte_carlo_steps=10,
                                    number_of_frames=nframes,
                                    write_initial_rmf=True,
                                    initial_rmf_name_suffix="initial",
                                    stat_file_name_suffix="stat",
                                    best_pdb_name_suffix="model",
                                    do_clean_first=True,
                                    do_create_directories=True,
                                    global_output_directory="output",
                                    rmf_dir="rmfs/",
                                    best_pdb_dir="pdbs/",
                                    replica_stat_file_suffix="stat_replica",
                                    test_mode=simo.dry_run)
mc1.execute_macro()

if '--mmcif' in sys.argv:
    # Add clustering info to the mmCIF file
    os.chdir('../../analysis/clustering')
    loc = ihm.location.WorkflowFileLocation('clustering.py',
                        details='Main clustering and analysis script')
    simo.add_metadata(loc)
    with open('clustering.py') as fh:
        exec(fh.read())
    # Link entities to UniProt
    if hasattr(ihm, 'reference'):
        for subunit, accession in (
                ('med6', 'P38782'), ('med8', 'P38304'), ('med11', 'Q99278'),
                ('med17', 'P32569'), ('med18', 'P32585'), ('med20', 'P34162'),
                ('med22', 'P32570'), ('med4', 'Q12343'), ('med7', 'Q08278'),
                ('med9', 'P33308'), ('med31', 'P38633'), ('med21', 'P47822'),
                ('med10', 'Q06213'), ('med1', 'Q12321'), ('med14', 'P19263'),
                ('med19', 'P25046'), ('med2', 'Q12124'), ('med3', 'P40356'),
                ('med5', 'P53114'), ('med15', 'P19659'), ('med16', 'P32259')):
            ref = ihm.reference.UniProtSequence.from_accession(accession)
            e = po.asym_units[subunit].entity.references.append(ref)
    po.flush()
