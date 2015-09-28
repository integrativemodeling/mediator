# I have to deprecate this function
import IMP
import IMP.atom
import IMP.core
import IMP.display
import IMP.rmf
import IMP.pmi
import IMP.pmi.analysis
import IMP.pmi.output
import RMF

def get_median_rmf(rmfsfile):
   rf=open(rmfsfile)
   for nl,l in enumerate(rf):
      if nl==2:
         tupletext=l.replace("All"," ").replace("centroid"," ").replace("rmf "," ").replace("name"," ").replace("\n"," ")
         (medianrmf,frame)=eval(tupletext)
   return medianrmf,frame

cluster_directory='kmeans_500_10/cluster.7/'

#indicate the rmsf.dat file to get the median rmf structure
rmsffile=cluster_directory+'/rmsf.dat'
medianrmf,frame=get_median_rmf(rmsffile)

model=IMP.Model()
rh = RMF.open_rmf_file_read_only(medianrmf)
prots = IMP.rmf.create_hierarchies(rh, model)
IMP.rmf.load_frame(rh, frame)
model.update()
particle_dict=IMP.pmi.analysis.get_particles_at_resolution_one(prots[0])

reduced_density_dict={"med6":["med6"],
                      "med8":["med8"],
                      "med11":["med11"],
                      "med17":["med17"],
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
                      "med19":["med19"],
                      "med2":["med2"],
                      "med3":["med3"],
                      "med5":["med5"],
                      "med15":["med15"],
                      "med16":["med16"]}



for p in reduced_density_dict:
    print p
    filename=cluster_directory+'/rmsf.'+p+'.dat'
    
    rmsffile=open(filename,"r")
    for l in rmsffile:
      print l
      t=l.split()
      residue=int(t[0])
      rmsf=float(t[2])
      s=IMP.atom.Selection(prots[0],molecule=p,residue_index=residue)
      psel=s.get_selected_particles()
      if rmsf>50: rmsf=50
      color=IMP.display.get_rgb_color(rmsf/50.0)
      IMP.display.Colored(psel[0]).set_color(color)

    

o=IMP.pmi.output.Output()
o.init_rmf(cluster_directory+"median_rmsf.rmf3",[prots[0]])
o.write_rmf(cluster_directory+"median_rmsf.rmf3")
o.close_rmf(cluster_directory+"median_rmsf.rmf3")

