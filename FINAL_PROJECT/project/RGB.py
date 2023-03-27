import math

mRED=[0.97622688,0.19416939,0.09508824]
sRED=[0.00320584,0.01171875,0.00979945]

mORA=[0.96723824,0.23669166, 0.08932122]
sORA=[0.005504517,0.017319306,0.011633717]

mBLU=[0.400153318,0.600500464,0.6917876]
sBLU=[0.014909344,0.014702359,0.016975503]

mGRE=[0.278519669,0.93692692,0.210826172]
sGRE=[0.008122479,0.003685617,0.008426642]

mPUR=[0.949436609,0.207711237,0.233982267]
sPUR=[0.00785332,0.022307818,0.011875954]

mYEL=[0.690929697,0.717638168,0.086923681]
sYEL=[0.00176491,0.001883567,0.007117353]



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
    return std_dist<=2
    
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
        
    
    
    
    
    
