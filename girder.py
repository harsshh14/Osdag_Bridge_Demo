class Girder_Design():
    def __init__ (self):
        self.span= 48.5 #m
        self.type= "Simply Supported"
        self.width= 13.5 #m
        self.carriageway_width= 10.5 #m
        self.CB_left= True
        self.CB_right= True
        self.footpath=True
        if self.footpath ==True:
            self.FP_width= 1.5 #m
            self.FP_thickness=150 #mm
        self.overhang_width=1.7 #m
        self.WC_thickness= 75 #mm
        self.vehicle_type= ['Class A', 'Class 70 R Wheeled', 'Special Vehicle', 'Fatigue Vehicle']

        '''Number of girders need to be changed/ automated to minimise material requirements'''
        self.num_of_girders= 4
        self.space_between_girder=3.4 #m
        self.slab_depth=240 #mm
        self.servicibility_req="no transverse stiffener provided" #[no transverse stiffener provided, only transverse stiffener provided,transverse stiffener + one level of longitudnal stiffener, second longitudnal stiffener at NA ]

        self.fy= 350 #MPa
        self.fck= 40 #MPa

        #Fatigue Requirments
        self.bridge_location= "Rural Area" #Inputs= ["Near Industrial Area", "Rural Area", "Others"]

        self.section_dimension()
        self.web_thickness_check()
        self.define_properties()
        self.Fatigue_Check()

    def section_dimension(self):
        self.girder_dimension={
            "bt":630,
            "tt":32,
            "dw":2678,
            "tw":16,
            "bf":770,
            "tf":40,
        }
        self.inner_concrete_beam={
            "beff": min(self.span*1000/4,self.space_between_girder*1000),
            "deff": self.slab_depth
        }
        self.outer_concrete_beam={
            "beff": min(self.span*1000/8+(self.overhang_width*1000),self.space_between_girder*1000/2+(self.overhang_width*1000)),
            "deff": self.slab_depth
        }

    def web_thickness_check(self):
        #[no transverse stiffener provided, only transverse stiffener provided,transverse stiffener + one level of longitudnal stiffener, second longitudnal stiffener at NA ]
        if self.servicibility_req="no transverse stiffener provided":
            pass
        elif 

    def define_properties(self):
        self.steel_section={ 
            type :"steel_section"

            }


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
print(G1.inner_concrete_beam["beff"])