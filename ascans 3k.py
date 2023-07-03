import os
# Importing important libraries
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.signal import savgol_filter
import time
import configparser
from scipy.signal import find_peaks
from datetime import datetime
import tkinter as tk 
from tkinter.filedialog import askdirectory 
import requests
import time as T
import peakutils
import csv
import os.path

#gc.enable()
#For ascan files




"""------------------------------------------------------------Reading from config file------------------------------------------------------------------"""
config = configparser.ConfigParser()
p = os.path.join(os.path.dirname(__file__), 'PoRTs_csharp.ini')
config.read(p)


OutputDest = config['PATH']['Outputdest']

samplefreq_in_MHz = 250
Amplitude_Threshold =   float(config['THRESHOLDS']['Amplitude_Threshold'])
Distance =   int(config['THRESHOLDS']['Distance'])
Trigger =   0

#samp_freq= 500 #Sampling Frequency in MHz
dt=1/samplefreq_in_MHz #sampling time

# Initialising figure
fig = plt.figure("Manish 4 Sensor Ascans")
plt.tight_layout()


Temperature = pd.DataFrame(columns=['Ascan File No.','Temp1', 'tof1', 'G_tof1'])
rheology = pd.DataFrame(columns=['Ascan File No.', 'Shear_Imp','Amplitude ratio', 'Amplitude_notch', 'Amplitude_end', 'G_Amplitude Ratio'])
sen_peaks =  pd.DataFrame(columns=['Ascan File No.', 'peak1', 'peak2','peak3','peak4'])
sen_peaks1 =  pd.DataFrame(columns=['Ascan File No.', 'peak1', 'peak2','peak3','peak4'])

isEmpty=1
root = tk.Tk()
root.withdraw()
##        
current_directory = askdirectory()
#current_directory = "D:/Desktop/code1/XYMA DATA/Manish_probe_200deg"


i = 3

try:
    file_path = os.path.join(current_directory, f"1 ({i}).csv")
    if not os.path.isfile(file_path):
        print("{i}th file does not exist")
        raise Exception
    data = pd.read_csv(file_path, sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
    a= data[3:]['average(A)']
    n = len(a)
    ydash1 = a.values.ravel()
    y1 = savgol_filter(ydash1, 61, 3)
    y2 = savgol_filter(y1, 61, 3)


    data2 = y2[Trigger:n]
    peaks, _ = find_peaks(data2, height=1.5, distance=5000)


    Start_P11 = (peaks[0]-1000) + Trigger
    End_P11 = (peaks[0]+1000) + Trigger

    Start_P12 = (peaks[1]-1000) + Trigger
    End_P12 = (peaks[1]+1000) + Trigger

    Start_P21 = (peaks[2]-1000) + Trigger
    End_P21 = (peaks[2]+1000) + Trigger

    Start_P22 = (peaks[3]-1000) + Trigger
    End_P22 = (peaks[3]+1000) + Trigger
    
    
    
    
except:
    print("Error in first file")

#try:
while(1):
    isFile=0  # 0- is not a file 1- is a file
    while isEmpty==1:
        file_name1 = "1 (%s).csv"
        file_path1 = os.path.join(current_directory,file_name1)
        next_file=file_path1 % str(i)
        try:
            f=os.path.isfile(next_file)
            if(f==True):
               isFile=1
            
            try:
                df = pd.read_csv(next_file, engine='python')
                #print("(%s) exists. Making isEmpty=1" %next_file)
                isEmpty=0
                #print("yaay file found")
            except pd.errors.EmptyDataError:
                print("file %s is empty" % ("1 (" + str(i) +").csv") )
#                        time.sleep(1)
        except:
#                    print("file not found")
            time.sleep(12)
    isEmpty=1
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    file_name = "1 (%d).csv" 
    file_path = os.path.join(current_directory,file_name)
###-----------reading csv file--------------------------------------------------------------------------------------------------------------------  

    data = pd.read_csv(file_path % i, sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
    data1 = pd.read_csv(file_path % i,sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
    
  
    a = data1[3:]['average(A)']

    y1 = savgol_filter(ydash1, 61, 3)
    y2 = savgol_filter(y1, 61, 3)
   
    
    ydash11 = a.values.ravel()[Start_P11:End_P11]
    ydash12 = a.values.ravel()[Start_P12:End_P12]
    ydash21 = a.values.ravel()[Start_P21:End_P21]
    ydash22 = a.values.ravel()[Start_P22:End_P22]


    
    # y: amplitude values after applying sgolay filter on ydash # sensor2
    y11 = savgol_filter(ydash11, 61, 3)
    y12 = savgol_filter(ydash12, 61, 3)
    y13 = savgol_filter(y11, 61, 3)
    y14 = savgol_filter(y12, 61, 3)
    
  
    max_index11 = np.argmax(y13)
    max_index12 = np.argmax(y14)
    
    max_index21 = np.argmax(13)
    max_index22 = np.argmax(14)

    max_value1 = np.amax(y13)
    max_value2 = np.amax(y14)
    
    min_value1 = np.amin(y13)
    min_value2 = np.amin(y14)
    
    a = a.to_numpy(dtype=np.float64)
   # print(a)
    n = len(a)
    
    
    ydash1 = a.ravel()
    #print(ydash1)
    
    
    indexes = [Start_P11+max_index11,Start_P12+max_index12,Start_P21+max_index21,Start_P22+max_index22]

#        print(indexes)
  
    
      
    interpolatedIndexes = peakutils.interpolate(np.array(list(range(0, len(ydash1)))), ydash1, ind=indexes)

#        print(interpolatedIndexes)
    
    TOF_1 = ((max_index12+Start_P12) - (max_index11+Start_P11) - (max_index22+Start_P22) - (max_index21+Start_P21))*dt
#        print(TOF_1)

    GG = (interpolatedIndexes[1] - interpolatedIndexes[0])*dt;

    print("Ascan Results")
    print("Ascan Number",i)
    print('Normal TOF',TOF_1)
    print("Gaussian TOF",GG)

    
    

    # print(V_Temp)
#        print("Temperature = ",V_Temp)
    
    Temperature = Temperature.append({'Ascan File No.': i,'tof1': TOF_1, 'G_tof1': GG}, ignore_index=True)
    #rheology= rheology.append({'Ascan File No.': i, 'Shear_Imp':Shear_impedance, 'Amplitude ratio':Amp_ratio, 'Amplitude_notch': Amp_notch, 'Amplitude_end':Amp_end}, ignore_index=True)
    sen_peaks = sen_peaks.append({'Ascan File No.': i, 'peak1': (Start_P11 + max_index11), 'peak2': (Start_P12 + max_index12), 'peak3' : (Start_P21 + max_index21), 'peak4' : (Start_P22 + max_index22)},  ignore_index=True)

    
    sen_peaks1 = sen_peaks.diff().fillna(0)
    Start_P11 = Start_P11 + sen_peaks1['peak1'].array[-1]
    End_P11 = End_P11 + sen_peaks1['peak1'].array[-1]
    Start_P12 = Start_P12 + sen_peaks1['peak2'].array[-1]
    End_P12 = End_P12 + sen_peaks1['peak2'].array[-1]
    Start_P21 = Start_P21 + sen_peaks1['peak3'].array[-1]
    End_P21 = End_P21 + sen_peaks1['peak3'].array[-1]
    Start_P22 = Start_P22 + sen_peaks1['peak4'].array[-1]
    End_P22 = End_P22 = sen_peaks1['peak4'].array[-1]
##    Start_P31 = Start_P31 + sen_peaks1['peak5'].array[-1]
##    End_P31 = End_P31 + sen_peaks1['peaks5'].array[-1]
##    # filename = datetime.now().strftime('Rheology measurement_10000CP-%Y-%m-%d %H.xlsx')
    FinalDest=OutputDest + '/'+"First_code.xlsx"      
    with pd.ExcelWriter(FinalDest) as writer:
           rheology.to_excel(writer, sheet_name='viscocity')
           Temperature.to_excel(writer, sheet_name = 'Temperature')

    # Data Visulalization
   
    plt.plot(y2)
    plt.plot((Start_P11+max_index11),y2[(Start_P11+max_index11)],"x")
    plt.plot((Start_P12+max_index12),y2[(Start_P12+max_index12)],"x")
    plt.plot((Start_P21+max_index21),y2[(Start_P21+max_index21)],"x")
    plt.plot((Start_P22+max_index22),y2[(Start_P22+max_index22)],"x")
##    plt.plot((Start_P31+max_index31),y2[(Start_P31+max_index31)],"x")
    plt.title("Ascan Number"+str(i))

    plt.pause(1e-5)
    fig.canvas.draw()
    plt.tight_layout()
    plt.clf()
    

    i = i+1
    #plt.close()
    
    #
##except:
##    print("Error in while Second loop")
  
