#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# coerbuoy1benchmark.py - Control benchmark COERbuoy1
# 2020/2021 COER Laboratory, Maynooth University
# in cooperation with CorPower Ocean AB
#
# Author:
# Simon H. Thomas, simon.thomas.2021@mumail.ie
"""
Created on Tue Aug 24 14:15:37 2021

@author: Simon H. Thomas
"""

import numpy as np;
import pandas;
from scipy.interpolate import interp1d;
import xml.etree.ElementTree as xml;
from datetime import date;
import os;

pkg_dir=os.path.dirname(__file__);

##Definitions
x_limit=3.5;
omega_cut_off=3.5;

# Regular wave (Height, period, name, control)
def reg_wave(H,p,n,ctrl):
    import COERbuoy;
    print("Regular wave")
    H=float(H)*1.4;
    p=float(p);
    t0=np.max([p*2,0]);#4
    if (p<6):
        t0=p*4;
    t2=np.max([t0+p*3,0]);#6
    t=np.arange(0,t2,1/(omega_cut_off))
    y=H/2*np.sin(2*np.pi/p*t)
    return COERbuoy.start_simu(time=t,wave=y,name=n, t0=t0, control=ctrl )#/(9.81*9.81*1000/(32*np.pi)*H**2*p)


# Brettschneider wave (significant wave height, energy period, name, control)
def brettschneider_wave(Hs,p,n,ctrl):
    import COERbuoy;
    print("Brettschneider wave")
    Hs=float(Hs);
    p=float(p);
    omega=np.linspace(0.001,4,200);
    omega_m=2*np.pi/(p/0.856);
    S=5/16*(omega_m**4)/(omega**5)*(Hs**2)*np.exp(-5*(omega_m**4)/4/(omega**4))
    t0=np.max([p*3,120]);
    t2=np.max([t0+p*3]);#6
    t=np.arange(0,t2,1/(omega_cut_off/np.pi))
    np.random.seed(6)#Maybe replace by fixed phase vector; has to guaranteed that rnadom sequecne is always the same
    phase=np.random.rand(omega.size)*2*np.pi;
    y=np.sum(np.sqrt(2*S*(omega[1]-omega[0]))*np.sin(omega*t.reshape(t.size,1)+phase),1)
    
        
    return COERbuoy.start_simu(time=t,wave=y,name=n, t0=t0, control=ctrl )

# Brettschneider wave (significant wave height, energy period, name, control, WEC parameter file)
def brettschneider2_wave(Hs,p,n,ctrl):
    import COERbuoy;
    print("Brettschneider wave")
    omega=np.linspace(0.001,4,200);
    omega_m=2*np.pi/(p/0.856);
    S=5/16*(omega_m**4)/(omega**5)*(Hs**2)*np.exp(-5*(omega_m**4)/4/(omega**4))
    t0=np.max([p*3,120]);
    t2=np.max([t0+p*6]);
    t=np.arange(0,t2,1/(omega_cut_off/np.pi))
    np.random.seed(6)#Maybe replace by fixed phase vector; Has to guaranteed that random sequecne is always the same
    phase=np.random.rand(omega.size)*2*np.pi;
    y=np.sum(np.sqrt(2*S*(omega[1]-omega[0]))*np.sin(omega*t.reshape(t.size,1)+phase),1)
    
        
    return COERbuoy.start_simu(time=t,wave=y,name=n, t0=t0, control=ctrl)


def quartil (a, p):
    a=np.abs(a);
    b=np.sort(a);
    aa=np.sum(a);
    if (aa==0):
        return 0;
    return b[np.argmax(np.cumsum(b)/aa>p)];
    
def benchmark(ctrl,easy):
    print("Benchmark COERbuoy1")
    
    #Write settings file
    if (easy):
        with open("coerbuoy_settings.txt","w") as f:
            f.write("""{"hydro":"Floater_BEM",\n"WECfolder":"""+'"'+os.path.join(pkg_dir,"coerbuoy1").replace("\\","/")+'"'+""",\n"resolution":0.01\n,"status_message":[1,1,1,1,1,1,1,1]}""");
    else:
        with open("coerbuoy_settings.txt","w") as f:
            f.write("""{"hydro":"Floater_BEM",\n"WECfolder":"""+'"'+os.path.join(pkg_dir,"coerbuoy1").replace("\\","/")+'"'+""",
"resolution":0.01,
"status_message":[1,0,0,1,1,1,1,1]}""");

    power=0;
    x_lim=x_limit;#dyn_wec.x_lim;
    
    folder=os.path.join(pkg_dir,"benchmark");
    
    import COERbuoy;
    def power (T,H):
        #Calculate (theoretical) absorbed power with constrained complex-conjugate control
        w=2*np.pi/T;
        fe1=[5.02E+05,4.96E+05,4.84E+05,4.68E+05,4.48E+05,4.24E+05,3.98E+05,3.71E+05,3.43E+05,3.16E+05,2.89E+05,2.64E+05,2.40E+05,2.19E+05,1.98E+05,1.80E+05,1.63E+05,1.47E+05,1.33E+05,1.21E+05,1.09E+05,9.87E+04,8.92E+04,8.04E+04,7.11E+04,7.98E+04,6.39E+04,5.76E+04,5.24E+04,4.78E+04,4.37E+04,4.00E+04]
        R1=[1.32E+02,1.03E+03,3.30E+03,7.31E+03,1.31E+04,2.03E+04,2.84E+04,3.68E+04,4.48E+04,5.20E+04,5.81E+04,6.29E+04,6.63E+04,6.84E+04,6.92E+04,6.90E+04,6.79E+04,6.60E+04,6.36E+04,6.07E+04,5.75E+04,5.40E+04,5.03E+04,4.61E+04,3.98E+04,7.11E+04,4.38E+04,3.90E+04,3.55E+04,3.25E+04,2.98E+04,2.73E+04]

        w1=np.linspace(0.1,3.2,len(fe1));
        f_fe=interp1d(w1,fe1,fill_value='extrapolate',bounds_error=False);
        f_R=interp1d(w1,R1,fill_value='extrapolate',bounds_error=False);
     
        fe=f_fe(w);
        R=f_R(w);

        Fe=1.4*H/2*fe;
        Pmax1=Fe**2/(8*R);
        u1=Fe/(2*R);
        if (u1>3.5):
          u=w*3.5;
          Pmax1=u**2/2*(Fe/u-R);
          
        return Pmax1;



    fktdict={"regular_wave":reg_wave,
         "bretschneider_wave":brettschneider_wave}


    #define tests:
    #regular wave: 0-3    
    #irregular waves 4-8
    #modelling errors irregular waves 8-11
    fkt=["regular_wave","regular_wave","regular_wave","regular_wave","bretschneider_wave","bretschneider_wave","bretschneider_wave","bretschneider_wave","bretschneider_wave","bretschneider_wave","bretschneider_wave","bretschneider_wave","bretschneider_wave","bretschneider_wave","bretschneider_wave","bretschneider_wave","bretschneider_wave","bretschneider_wave","bretschneider_wave","bretschneider_wave","bretschneider_wave","bretschneider_wave","bretschneider_wave","bretschneider_wave","bretschneider_wave","bretschneider_wave","bretschneider_wave","bretschneider_wave"]

    heights=[1,1,3,3]*6;
    periods=[6,9,9,12]*6;
    
    rand1=[0,0,0,0,0,0,0,0,0.893,0.332,0.821,0.042,0.108,0.301,0.167,0.323,0.666,0.667,0.398,0.379,0.017,0.12,0.69,0.874]
    rand2=[0,0,0,0,0,0,0,0,0.595,0.5298,0.419,0.335,0.622,0.337,0.99,0.132,0.500,0.287,0.22,0.50,0.636,0.636,0.08,0.68]
    rand3=[0,0,0,0,0,0,0,0,0.438,0.736,0.518,0.579,0.645,0.84,0.29,0.99,0.547,0.959,0.356,0.517,0.988,0.204,0.976,0.04]
    rand4=[0,0,0,0,0,0,0,0,0.990,0.82,0.821,0.413,0.876,0.02,0.2,0.012,0.447,0.652,0.711,0.255,0.764,0.966,0.54,0.43]
    
    rand1=rand1[:6*4];
    
    cw=np.zeros(len(rand1));

    rng=np.random.default_rng();
    arr=np.arange(len(rand1));
    rng.shuffle(arr);
    #regular, irregular tests (normal+modelling errors test)
    for j1 in arr:
        print(j1);
        #if False:
        f=open(os.path.join(pkg_dir,"coerbuoy1","floater.txt"),"w");
        f.write("""{"geo":[{"type":"cone","coord":[-4.5,0,-2,3]},
{"type":"cone","coord":[-2,3,-1,3.7]},
{"type":"cone","coord":[-1,3.7,0,4]},
{"type":"cone","coord":[0,4,1,3.7]},
{"type":"cone","coord":[1,3.7,2,3]},
{"type":"cone","coord":[2,3,4.5,0]}],
"negative_spring_force":"""+str(500000*(1+rand1[j1]*0.2))+""",
"negative_spring_length":1.85,
"negative_spring_stroke":5,
"viscous_drag_coefficient_heave":0.2,
"viscous_drag_coefficient_surge":0.2,
"mass_fraction_floater":0.8,
"generator_Rc":3,
"generator_c_L":60,
"generator_c_lambda":4000,
"generator_I_s":300,
"heave_only":"""+str(easy)+""",
"friction_force_static":"""+str(30000*(1+rand2[j1]*0.2))+""",
"friction_force_kinetic":15000,
"friction_damping":"""+str(7500*(1+rand3[j1]*0.4))+""",
"angle_limit":15,
"l_mooring":"""+str(20*(1+rand4[j1]*0.2))+""",
"angle_limit":15
}""");
        f.close();

        
        print("Write to "+os.path.join(folder,"benchmark"+str(j1)+".csv"));
        cw[j1]=cw[j1]+1/3*fktdict[fkt[j1]](heights[j1],periods[j1],os.path.join(folder,"benchmark"+str(j1)+".csv"),ctrl)/power(periods[j1],heights[j1]);
    print(cw)
    constraint_score=np.zeros(len(rand1));
    power_score=np.zeros(len(rand1));
    total_score=np.zeros(len(rand1));
    max_x=np.zeros(len(rand1));
    max_v=np.zeros(len(rand1));
    max_f=np.zeros(len(rand1));
    #cw=[0.28016265, 0.12318111, 0.08283574, 0.05843654, 0.07473666, 0.03710698, 0.02122793, 0.05248458, 0.07473666, 0.03710698, 0.02122793, 0.02384048, 0.07473666, 0.03710698, 0.02122793, 0.02384048, 0.07473666, 0.02488943, 0.02122793, 0.02384048, 0.07473666, 0.03710698, 0.02122793, 0.02384048]

    for i in range(len(rand1)):
        a=np.array(pandas.read_csv(os.path.join(folder,"benchmark"+str(i)+".csv"), header=1))
        t=a[:,0];
        h=a[:,2];
        v=a[:,3];
        #p=a[:,-1];
        
        ##Scoring
        #constraint score
        constraint_score[i]=1-(t[1]-t[0])*np.sum(np.abs(h)>x_lim)/(t[-1]-t[0]);
        #power score
        power_score[i]=cw[i];
        
        v=quartil(a[:,3],0.95);
        f=quartil(a[:,-2],0.95);
        
        #max. state
        max_x[i]=np.max(h);
        max_v[i]=np.max(v);
        max_f[i]=np.max(f);
        
    #average the 4 runs for the modelling error test
    for j in np.arange(4):
        power_score[8+j]      = np.mean(power_score[8+j::4]);
        constraint_score[8+j] = np.mean(constraint_score[8+j::4]);
        total_score[8+j]      = np.mean(total_score[8+j::4]);
    
    power_score=power_score.round(3);
    constraint_score=constraint_score.round(3);
    total_score = power_score*(constraint_score);

    row0=["category","state1","state2","state3","state4","power","constraints","score"]
    row1=["regular_waves"]+total_score[:4].tolist()+[np.mean(power_score[:4]),np.mean(constraint_score[:4]),np.mean(total_score[:4])]
    row2=["irregular_waves"]+total_score[4:8].tolist()+[np.mean(power_score[4:8]),np.mean(constraint_score[4:8]),np.mean(total_score[4:8])]
    row3=["error_modelling"]+total_score[8:12].tolist()+[np.mean(power_score[8:12]),np.mean(constraint_score[8:12]),np.mean(total_score[8:12])]
    row4=["total",0,0,0,0,np.mean(power_score[:12]),np.mean(constraint_score[:12]),np.mean(total_score[:12])]
    
    pDf=pandas.DataFrame(np.vstack([row1,row2,row3,row4]),columns=row0)
    pDf.round(2).to_csv("benchmark_total.csv",index=False)
    
    
    power_score=(power_score).round(2);
    constraint_score=(constraint_score).round(2);
    total_score=(total_score).round(2);
    #total_score1=[];
    #for idx,t in enumerate(total_score):
    #    total_score1.append(str((int)(t*100))+"%");
    
    cert = xml.parse(pkg_dir+"/cert_raw.svg");
    ro=cert.getroot();
    
    today=date.today();
    if easy==2:
        ctrl=ctrl+" (easy mode)"
    dic={'controller':"for "+ctrl+ ", issued on "+ today.strftime("%d.%m.%y")+".",
         'info':"Work in progress",
         
         's_power11':power_score[0],'s_con11':constraint_score[0],'score11':total_score[0],
         's_power12':power_score[1],'s_con12':constraint_score[1],'score12':total_score[1],
         's_power13':power_score[2],'s_con13':constraint_score[2],'score13':total_score[2],
         's_power14':power_score[3],'s_con14':constraint_score[3],'score14':total_score[3],
         's_power1':np.mean(power_score[:4]).round(2),'s_con1':np.mean(constraint_score[:4]).round(2),'score1':np.mean(total_score[:4]).round(2),
         
         's_power21':power_score[0+4],'s_con21':constraint_score[0+4],'score21':total_score[0+4],
         's_power22':power_score[1+4],'s_con22':constraint_score[1+4],'score22':total_score[1+4],
         's_power23':power_score[2+4],'s_con23':constraint_score[2+4],'score23':total_score[2+4],
         's_power24':power_score[3+4],'s_con24':constraint_score[3+4],'score24':total_score[3+4],
         's_power2':np.mean(power_score[4:8]).round(2),'s_con2':np.mean(constraint_score[4:8]).round(2),'score2':np.mean(total_score[4:8]).round(2),
         
         's_power31':power_score[0+8],'s_con31':constraint_score[0+8],'score31':total_score[0+8],
         's_power32':power_score[1+8],'s_con32':constraint_score[1+8],'score32':total_score[1+8],
         's_power33':power_score[2+8],'s_con33':constraint_score[2+8],'score33':total_score[2+8],
         's_power34':power_score[3+8],'s_con34':constraint_score[3+8],'score34':total_score[3+8],
         's_power3':np.mean(power_score[8:12]).round(2),'s_con3':np.mean(constraint_score[8:12]).round(2),'score3':np.mean(total_score[8:12]).round(2),
         
         
         's_power':np.mean(power_score[:12]).round(2),'s_con':np.mean(constraint_score[:12]).round(2),'score':np.mean(total_score[:12]).round(2)};
    
    for a1 in ro.iter('{http://www.w3.org/2000/svg}text'):
        cd = [b1 for b1 in a1];
            
        #a.text=str(dic[a.attrib['id']]);
        if (a1.attrib['id'] in dic):
          try:
              cd[0].text=format(dic[a1.attrib['id']],".2f");
          except:
              cd[0].text=(dic[a1.attrib['id']]);
        
        print(a1.attrib)
    cert.write("certificate"+ctrl+"_"+today.strftime("%d%m%y")+".svg")
    return power;

def run():
    ctrl="help";
    print("Welcome to the COERbuoy1 benchmark tool!")
    print("2021 by the Centre of Ocean Energy Research at Maynooth University")
    print("\nThis tool aims to test controller for Wave Energy Converter with a realisic numerical model.\n")
    print("\nPlease select a controller to test.")
    print("Enter help for examples and further information.")
    
    #print("\nFor example type python3 <filename.py> or py <filename.py> if your controller is written in python")
    while (ctrl == "help"):
        ctrl=input();
        if ctrl == "help":
            print("The controller you are referring to should be in the folder "+os.getcwd()+", or use absolute filenames.\n")        
            print("Run a controller written in python:\npython <filename.py>\npython3 <filename.py>\npy <filename>")
            print("Run a controller written in octave:\noctave <filename.m>")
            print("\nSpecial commands:\nTCP - opens a TCP socket\nlinear - enter test with a linear damping\nhelp - show help\nexit - close program")
    
    if (ctrl != "exit"):
        print(ctrl)
        benchmark(ctrl,0);

if __name__ == "__main__":
    run();