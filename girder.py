'''
Issues faced- 
too many inputs
no way to calculate forces

'''

import math


class Girder_Design():
    def __init__ (self):
        self.span= 42.4 #m
        self.type= "Simply Supported"
        self.width= 10 #m
        self.carriageway_width= 10.5 #m
        self.CB_left= True
        self.CB_right= True
        self.footpath=True
        if self.footpath ==True:
            self.FP_width= 1.5 #m
            self.FP_thickness=150 #mm
        self.overhang_width=1.25 #m
        self.WC_thickness= 75 #mm
        self.vehicle_type= ['Class A', 'Class 70 R Wheeled', 'Special Vehicle', 'Fatigue Vehicle']

        '''Number of girders need to be changed/ automated to minimise material requirements'''
        self.num_of_girders= 4
        self.num_of_lanes=3
        self.space_between_girder=2.5 #m
        self.slab_depth=250 #mm
        self.servicibility_req="no transverse stiffener provided" #[no transverse stiffener provided, only transverse stiffener provided,transverse stiffener + one level of longitudnal stiffener, second longitudnal stiffener at NA ]
        self.transverse_stiffener_spacing=2000  #mm

        self.fy= 350 #MPa
        self.fck= 40 #MPa
        self.epsilon=math.sqrt(self.fy/250)
        self.E_steel= 200000 #MPa
        self.E_concrete= 5000*math.sqrt(self.fck)
        self.density_steel= 7860 #kg/m3
        #Fatigue Requirments
        self.bridge_location= "Rural Area" #Inputs= ["Near Industrial Area", "Rural Area", "Others"]

        self.section_dimension()
        self.web_thickness_check()
        self.compression_flange_checks()
        self.define_properties()
        self.force_calculation() #Add method to calculate the vehicle loads and how to find Influence Line Diagram
        self.Fatigue_Check()

    def section_dimension(self):
        self.girder_dimension={
            "bt":650,
            "tt":45,
            "dw":2405,
            "tw":20,
            "bf":900,
            "tf":50,
        }
        self.inner_concrete_beam={
            "beff": min(self.span*1000/4,self.space_between_girder*1000),
            "deff": self.slab_depth
        }
        self.outer_concrete_beam={
            "beff": min(self.span*1000/8+(self.overhang_width*1000),self.space_between_girder*1000/2+(self.overhang_width*1000)),
            "deff": self.slab_depth
        }

    def define_properties(self):
        self.steel_section={ 
            "type" :"steel_section",
            "area" :self.girder_dimension["bt"]*self.girder_dimension["tt"] + self.girder_dimension["dw"]*self.girder_dimension["tw"] + self.girder_dimension["bf"]*self.girder_dimension["tf"],
        }
        self.steel_section["self_wt"]=self.steel_section["area"]*self.density_steel/10**8
        self.steel_section["yt"]=((self.girder_dimension["bt"]*self.girder_dimension["tt"]*self.girder_dimension["tt"]/2) + (self.girder_dimension["dw"]*self.girder_dimension["tw"]*(self.girder_dimension["tt"]+self.girder_dimension["dw"]/2)) + (self.girder_dimension["bf"]*self.girder_dimension["tf"]*(self.girder_dimension["tt"]+self.girder_dimension["dw"]+self.girder_dimension["tf"]/2)))/self.steel_section["area"]
        self.steel_section["yb"]=self.girder_dimension["tt"]+self.girder_dimension["dw"]+self.girder_dimension["tf"]-self.steel_section["yt"]
        self.steel_section["Ixx"]=(self.girder_dimension["bt"]*self.girder_dimension["tt"]**3/12)+(self.girder_dimension["tw"]*self.girder_dimension["dw"]**3/12)+(self.girder_dimension["bf"]*self.girder_dimension["tf"]**3/12)+(self.girder_dimension["bt"]*self.girder_dimension["tt"]*(self.steel_section["yt"]-self.girder_dimension["tt"]/2)**2)+(self.girder_dimension["dw"]*self.girder_dimension["tw"]*abs(self.steel_section["yt"]-self.girder_dimension["tt"]-self.girder_dimension["dw"]/2)**2)+(self.girder_dimension["bf"]*self.girder_dimension["tf"]*(self.steel_section["yb"]-self.girder_dimension["tf"]/2)**2)
        self.steel_section["Iyy"]=(self.girder_dimension["dw"]*self.girder_dimension["tw"]**3/12)+(self.girder_dimension["tt"]*self.girder_dimension["bt"]**3/12)+(self.girder_dimension["tf"]*self.girder_dimension["bf"]**3/12)
        self.steel_section["Izz"]=(self.girder_dimension["bt"]*self.girder_dimension["tt"]**3/3)+(self.girder_dimension["dw"]*self.girder_dimension["tw"]**3/3)+(self.girder_dimension["bf"]*self.girder_dimension["tf"]**3/3)
        self.steel_section["Zeb"]=self.steel_section["Ixx"]/self.steel_section["yb"]
        self.steel_section["Zet"]=self.steel_section["Ixx"]/self.steel_section["yt"]
        self.steel_section["Zpt"]=1.12*self.steel_section["Zet"]
        self.steel_section["ryy"]=math.sqrt(self.steel_section["Iyy"]/self.steel_section["area"])

        self.transient_outer={ 
            type :"transient_loading",
            }
        self.transient_outer["m"]=max(7.5,self.E_steel/self.E_concrete)
        self.transient_outer["beff_steel"]=math.floor(self.outer_concrete_beam["beff"]/self.transient_outer["m"])
        self.transient_outer["area"]=self.steel_section["area"]+ self.transient_outer["beff_steel"]*self.outer_concrete_beam["deff"]
        self.transient_outer["yb"]=((self.girder_dimension["bf"]*self.girder_dimension["tf"]**2/2)+(self.girder_dimension["tw"]*self.girder_dimension["dw"]*(self.girder_dimension["tf"]+self.girder_dimension["dw"]/2))+(self.girder_dimension["tt"]*self.girder_dimension["bt"]*(self.girder_dimension["tf"]+self.girder_dimension["dw"]+self.girder_dimension["tt"]/2)+(self.transient_outer["beff_steel"]*self.outer_concrete_beam["deff"]*(self.outer_concrete_beam["deff"]/2+self.girder_dimension["tt"]+self.girder_dimension["dw"]+self.girder_dimension["tf"]))))/self.transient_outer["area"]
        self.transient_outer["yt"]=self.girder_dimension["tf"]+self.girder_dimension["dw"]+self.girder_dimension["tt"]+self.outer_concrete_beam["deff"]-self.transient_outer["yb"]
        self.transient_outer["Ixx"]=(self.transient_outer["beff_steel"]*self.outer_concrete_beam["deff"]**3/12)+(self.transient_outer["beff_steel"]*self.outer_concrete_beam["deff"]*(self.transient_outer["yt"]-self.outer_concrete_beam["deff"]/2)**2)+(self.steel_section["Ixx"])+(self.steel_section["area"]*(self.steel_section["yt"]+self.outer_concrete_beam["deff"]-self.transient_outer["yt"])**2)
        self.transient_outer["Iyy"]=self.steel_section["Iyy"]+((self.transient_outer["beff_steel"]**3)*self.outer_concrete_beam["deff"]/12)
        self.transient_outer["Izz"]=self.steel_section["Izz"]+(self.transient_outer["beff_steel"]*self.outer_concrete_beam["deff"]**3/3)            
        self.transient_outer["Zeb"]=self.transient_outer["Ixx"]/self.transient_outer["yb"]
        self.transient_outer["Zet"]=self.transient_outer["Ixx"]/self.transient_outer["yt"]
        self.transient_outer["Zpt"]=self.transient_outer["Ixx"]/(self.transient_outer["yt"]-self.outer_concrete_beam["deff"])
        self.transient_outer["ryy"]=math.sqrt(self.transient_outer["Iyy"]/self.transient_outer["area"])
        self.transient_inner={ 
            type :"transient_loading",
            }
        self.permanent_outer={ 
            type :"permanent_loading",
            }
        self.permanent_outer["m"]=max(15,2*self.E_steel/self.E_concrete)
        self.permanent_outer["beff_steel"]=math.floor(self.outer_concrete_beam["beff"]/self.permanent_outer["m"])
        self.permanent_outer["area"]=self.steel_section["area"]+ self.permanent_outer["beff_steel"]*self.outer_concrete_beam["deff"]
        self.permanent_outer["yb"]=((self.girder_dimension["bf"]*self.girder_dimension["tf"]**2/2)+(self.girder_dimension["tw"]*self.girder_dimension["dw"]*(self.girder_dimension["tf"]+self.girder_dimension["dw"]/2))+(self.girder_dimension["tt"]*self.girder_dimension["bt"]*(self.girder_dimension["tf"]+self.girder_dimension["dw"]+self.girder_dimension["tt"]/2)+(self.permanent_outer["beff_steel"]*self.outer_concrete_beam["deff"]*(self.outer_concrete_beam["deff"]/2+self.girder_dimension["tt"]+self.girder_dimension["dw"]+self.girder_dimension["tf"]))))/self.permanent_outer["area"]
        self.permanent_outer["yt"]=self.girder_dimension["tf"]+self.girder_dimension["dw"]+self.girder_dimension["tt"]+self.outer_concrete_beam["deff"]-self.permanent_outer["yb"]
        self.permanent_outer["Ixx"]=(self.permanent_outer["beff_steel"]*self.outer_concrete_beam["deff"]**3/12)+(self.permanent_outer["beff_steel"]*self.outer_concrete_beam["deff"]*(self.permanent_outer["yt"]-self.outer_concrete_beam["deff"]/2)**2)+(self.steel_section["Ixx"])+(self.steel_section["area"]*(self.steel_section["yt"]+self.outer_concrete_beam["deff"]-self.permanent_outer["yt"])**2)
        self.permanent_outer["Iyy"]=self.steel_section["Iyy"]+((self.permanent_outer["beff_steel"]**3)*self.outer_concrete_beam["deff"]/12)
        self.permanent_outer["Izz"]=self.steel_section["Izz"]+(self.permanent_outer["beff_steel"]*self.outer_concrete_beam["deff"]**3/3)            
        self.permanent_outer["Zeb"]=self.permanent_outer["Ixx"]/self.permanent_outer["yb"]
        self.permanent_outer["Zet"]=self.permanent_outer["Ixx"]/self.permanent_outer["yt"]
        self.permanent_outer["Zpt"]=self.permanent_outer["Ixx"]/(self.permanent_outer["yt"]-self.outer_concrete_beam["deff"])
        self.permanent_outer["ryy"]=math.sqrt(self.permanent_outer["Iyy"]/self.permanent_outer["area"])
      
        self.permanent_inner={ 
            type :"permanent_loading",
            }


    def web_thickness_check(self):
        #[no transverse stiffener provided, only transverse stiffener provided,transverse stiffener + one level of longitudnal stiffener, second longitudnal stiffener at NA ]
        if self.servicibility_req=="no transverse stiffener provided":
            if (self.girder_dimension["dw"]/self.girder_dimension["tw"])<200*self.epsilon:
                print("Ok")
            else:
                print(" not ok")
        elif self.servicibility_req=="only transverse stiffener provided":
            pass
        elif self.servicibility_req=="transverse stiffener + one level of longitudnal stiffener":
            pass
        elif self.servicibility_req=="second longitudnal stiffener at NA ":
            pass

    def compression_flange_checks(self):
        if self.servicibility_req=="no transverse stiffener provided":
            if (self.girder_dimension["dw"]/self.girder_dimension["tw"])<345*self.epsilon**2:
                print("Ok")
            else:
                print(" not ok")
        elif self.servicibility_req=="only transverse stiffener provided":
            if (self.transverse_stiffener_spacing<1.5*self.girder_dimension["dw"]) and (self.girder_dimension["dw"]/self.girder_dimension["tw"])<345*self.epsilon:
                print("ok for compression flange check")
            elif (self.transverse_stiffener_spacing>=1.5*self.girder_dimension["dw"]) and (self.girder_dimension["dw"]/self.girder_dimension["tw"])<345*self.epsilon**2:
                print("ok for compression flange check")
            else:
                print("fails in compression flange check")

    def force_calculation(self):
        pass

    def Fatigue_Check(self):
        #IRC 6
        if self.bridge_location== "Near Industrial Area":
            self.num_of_cycles= 10000000
        elif self.bridge_location=="Others":
            self.num_of_cycles=2000000
        else:
            print("No fatigue check needed for bridges in rural area")
            return 
        #IRC 22
                

# Girder_Design.__init__(self=Girder_Design())
G1=Girder_Design()
print(G1.permanent_outer["Izz"])
print(G1.permanent_outer["Zeb"])
print(G1.permanent_outer["Zet"])
print(G1.permanent_outer["Zpt"])
print(G1.permanent_outer["ryy"])



#write steps in the report
#write algorithm for the bridge design (entire)
