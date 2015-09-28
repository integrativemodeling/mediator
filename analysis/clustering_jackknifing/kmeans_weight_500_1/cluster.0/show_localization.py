import os
import glob
from chimera import runCommand as rc
from chimera import replyobj

#change to folder with data files
#os.chdir("/Users/pett/data")

#em_map = "../mediator_modeling/em_map_files/asturias_mediator_translated.mrc"

cluster_dir = "./"
#cluster_dir = "../cluster.0/"

pdb_file = cluster_dir + "0.pdb"
view1_matrix = "./view1_matrix"
view2_matrix = "./view2_matrix"
background = "white"


colors = dict(
  #        colo       pdb code    mw
  Med1  = ["#028482",  None,   64252],
  Med2  = ["#AE956D",  None,   47718],
  Med3  = ["#443266",  None,   43080],
  Med4  = ["#660066",  "H",    32205],
  Med5  = ["#7A3E48",  None,   128796],
  Med6  = ["#FFDE00",  "A",    32819],
  Med7  = ["#806641",  "I",    25585],
  Med8  = ["#CC3300",  "B",    25268],
  Med9  = ["#19376A",  "J",    17377],
  Med10 = ["#00B600",  None,   17908],
  Med11 = ["#B76EB8",  "C",    13307],
  Med14 = ["#FF8362",  None,   123359],
  Med15 = ["#097054",  None,   120310],
  Med16 = ["#F6D55D",  "U",    111298],
  Med17 = ["#6599FF",  "D",    78477],
  Med18 = ["#94DAF0",  "E",    34289],
  Med19 = ["#A74400",  None,   24858],
  Med20 = ["#FF9900",  "F",    22894],
  Med21 = ["#FFCC99",  "L",    16072],
  Med22 = ["#7ABA7A",  "G",    13863],
  Med31 = ["#6E7587",  "K",    14741],
  Med314 = ["#FF8362",  None,   80761], # Med314 = Med14Nterm
  Med414 = ["#FF8362",  None,   42616], # Med414 = Med14Cterm
  Med117 = ["#6599FF",  None,    13439], # Med117 = Med17Nterm
  Med217 = ["#6599FF",  "D",     65055] # Med217 = Med17Cterm
)


def open_mrc(dir, thresh=0.1):
   density_names = glob.glob(dir+"*.mrc")

   for d in density_names:
      model_num = d.replace(".mrc","").replace("med","").replace(cluster_dir,"")
      #print(model_num)
      replyobj.status("Processing " + d) # show what file we're working on
      rc("open " + model_num + " " + d )
      rc("col " +colors["Med"+model_num][0] + " #" + model_num)
      if thresh == "byVol":
         volume = str(float(colors["Med"+model_num][2]) * 1.21)
         rc("vol #" + model_num + " encloseVolume " + volume)
      else:
         rc("vol #" + model_num + " level " + str(thresh))

   rc("focus")

def display_pdb(pdb, trans):
   rc("open #0 " + pdb)
   for prot, dat in colors.iteritems():
      model = prot.replace("Med","")
      if dat[1]:
        rc("transparency " + str(trans) + " #" + model)
        rc("col " + dat[0] + " #0:." + dat[1])
   try:
      rc("ribscale med #0")
   except:
      print("Ribbon style not found")

def show_em(em_file):
   rc("open #100 " + em_file)
   rc("vol #100 level 0.35 style mesh")


def view1_rotate(view1_matrix):
   rc("matrixset " + view1_matrix)
   rc("focus")

def view2_rotate(view2_matrix):
    rc("matrixset " + view2_matrix)
    rc("focus")

def save_img(file_name):
    rc("windowsize 1024 768")
    rc("focus")
    rc("copy file " + file_name + ".png" + " width 3072" + " height 2304" + " supersample 3" + " raytrace")

def set_background(background):
   rc("background solid " + background)

set_background(background)

open_mrc(cluster_dir)
#open_mrc(cluster_dir, "byVol")

#display_pdb(pdb_file, 70)

view1_rotate(view1_matrix)
file_name = ("kmeans_500_1_half1_view1_v2")
save_img(file_name)


view2_rotate(view2_matrix)
file_name = ("kmeans_500_1_half1_view2_v2")
save_img(file_name)

#show_em(em_map)

#save_img("out")

