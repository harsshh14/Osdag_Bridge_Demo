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