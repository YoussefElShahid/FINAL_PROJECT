import math

mRED=[0.988091273,0.125774727,0.067087682]
sRED=[0.020736781,0.047576175,0.026138001]

mORA=[0.9771539,0.202445006, 0.063269789]
sORA=[0.003011615,0.012610372,0.004062792]

mBLU=[0.474500618,0.655742082,0.578824352]
sBLU=[0.038103582,0.051326005,0.075999721]

mGRE=[0.378545937,0.909548983,0.170057355]
sGRE=[0.018611636,0.008907477,0.009167629]

mPUR=[0.97665266,0.15105682,0.151579522]
sPUR=[0.003834311,0.016661019,0.008062835]

mYEL=[0.805509926,0.586944046,0.068516605]
sYEL=[0.02641052,0.031517587,0.01668939]



def color_mapping(color_list,mean_list,std_list):
    r=color_list[0]
    g=color_list[1]
    b=color_list[2]
    
    module=math.sqrt(r**2+g**2+b**2)
    
    nr=r/module
    ng=g/module
    nb=b/module
    
    mR=mean_list[0]
    mG=mean_list[1]
    mB=mean_list[2]
    
    sR=std_list[0]
    sG=std_list[1]
    sB=std_list[2]
    
    
    diffR=(mR-nr)/sR
    diffG=(mG-ng)/sG
    diffB=(mB-nb)/sB
    
    std_dist=math.sqrt(diffR**2+diffG**2+diffB**2)
    return std_dist<=15
    
def color_choosing(color_list):
    if color_mapping(color_list,mRED,sRED):
        color=1
    elif color_mapping(color_list,mORA,sORA):
        color=2
    elif color_mapping(color_list,mBLU,sBLU):
        color=3
    elif color_mapping (color_list,mGRE,sGRE):
        color=4
    elif color_mapping(color_list,mPUR,sPUR):
        color=5
    elif color_mapping(color_list,mYEL,sYEL):
        color=6
    else:
        color=7
    return color
        
    
    
    
    
    
