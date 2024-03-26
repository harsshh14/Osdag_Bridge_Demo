class Girder_Design():
    def __init__ (self):
        self.span= 30 #m
        self.type= "Simply Supported"
        self.width= 13.5 #m
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

        self.fy= 350 #MPa
        self.fck= 40 #MPa

        #Fatigue Requirments
        self.bridge_location= "Rural Area" #Inputs= ["Near Industrial Area", "Rural Area", "Others"]


        self.Fatigue_Check()


    
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
                

Girder_Design.__init__(self=Girder_Design())