import pandas as pd
import numpy as np
import math


def def_cl_a():
    Cl_A=[0]*math.ceil((18.8+20)/0.25*3)
    Cl_A[0]=Cl_A[5]=27
    Cl_A[18]=Cl_A[22]=114
    Cl_A[40]=Cl_A[52]=Cl_A[64]=Cl_A[76]=68

    Cl_A[157]=Cl_A[162]=27
    Cl_A[175]=Cl_A[179]=114
    Cl_A[197]=Cl_A[209]=Cl_A[221]=Cl_A[233]=68

    Cl_A[314]=Cl_A[319]=27
    Cl_A[332]=Cl_A[336]=114
    Cl_A[354]=Cl_A[366]=Cl_A[378]=Cl_A[390]=68
    return Cl_A


def def_cl_70r_tr():
    Cl_70R_track=[0]*math.ceil((94.57)/0.25*1)
    for i in range(1,18):
        Cl_70R_track[i]=38.8888888888889
    Cl_70R_track[0]=Cl_70R_track[18]=19.4444444444444

    return Cl_70R_track

def def_cl_70r_wh():
    Cl_70R_wheel=[0]*math.ceil((43.4)/0.25*3)
    Cl_70R_wheel[0]=80
    Cl_70R_wheel[16]=Cl_70R_wheel[22]=120
    Cl_70R_wheel[31]=Cl_70R_wheel[36]=Cl_70R_wheel[48]=Cl_70R_wheel[54]=170

    Cl_70R_wheel[175]=80
    Cl_70R_wheel[191]=Cl_70R_wheel[197]=120
    Cl_70R_wheel[206]=Cl_70R_wheel[211]=Cl_70R_wheel[223]=Cl_70R_wheel[229]=170

    Cl_70R_wheel[350]=80
    Cl_70R_wheel[366]=Cl_70R_wheel[372]=120
    Cl_70R_wheel[381]=Cl_70R_wheel[386]=Cl_70R_wheel[398]=Cl_70R_wheel[404]=170

    return Cl_70R_wheel

def ILD_Long(span, spacing, num_lanes, vehicle_class):
    num_steps= math.ceil(span/spacing)
    
    #Creating ILD for SF and BM
    ILD_BM=[None]*(num_steps+1)
    ILD_SF=[None]*(num_steps+1)
    for x in range(num_steps+1):
        ILD_SF[x]=max(min((span-spacing*(x))/span,1),0)
        if (x)*0.25<span/2:
            ILD_BM[x]=max(x*0.25/2,0)
        else:
            ILD_BM[x]=max((span-(x*0.25))/2,0)
    
    #Creating Vehicle
    if "Class A" in vehicle_class:
        cl_70r_w, cl70r_tr=def_cl_a()
    if "Class 70R (Wheeled)" in vehicle_class:
        cl_70r_w=def_cl_70r_wh()
    if "Class 70R (Tracked)" in vehicle_class:
        cl70r_tr=def_cl_70r_tr()
    
    
    
    results={
        "Class_A_BM":0,
        "Class_B_BM":0,
        "SV_BM":0,
        "Class_70R_wheel_BM":0,
        "Class_70R_track_BM":0,
        "Class_A_SF":0,
        "Class_B_SF":0,
        "SV_SF":0,
        "Class_70R_wheel_SF":0,
        "Class_70R_track_SF":0,
    }
    results["Class_70R_wheel"]=23

    return results


print(ILD_Long(42.4,0.25,2,["Class A","Class 70R (Tracked)", "Class 70R (Wheeled)" ]))
#print()


