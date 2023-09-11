# -*- coding: utf-8 -*-
"""
"""
##Racheal Fisher
#To use this code, copy your data and put it in two columns in a txt with nothing else

# Import programs
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import math

# Create figure
# Create multiple
# graph, (plot1, plot2) = plt.subplots(1, 2)
plt.figure(figsize=(3,3), dpi=300)

# Create lists angle and intensity
nm = []
percentR = []

# Open file and read data. 
file = open('UvVisTest.txt')
data = file.readlines()
file.close()

# Divide text data into two lists, nm and %R
for line in data[151:]:
    split = line.strip().split('\t')
    nm.append(float(split[0]))
    percentR.append(float(split[1]))

# Find where the shift happens
for x in nm:
    # Remove 200 from list(you can't subtract 1 from 200 or it will break)
    if x>200:
        # Check for big change in y values over 1 x value change
        if percentR[nm.index(x)] - percentR[nm.index(x-1)] >= 5:
            x1 = x
            x2 = x-1
            y1 = percentR[nm.index(x)]
            y2 = percentR[nm.index(x2)]
            print(x1, x2)

shiftSize = (y2-y1)
print(shiftSize)

#Correct the shift
for x in nm:
    if x>=x1:
        percentR[nm.index(x)] = percentR[nm.index(x)] + shiftSize

# Label points to be shifted if desired
# plt.plot(x1, y1, marker="o", markersize=4, color = 'blue')
# plt.plot(x2, y2, marker="o", markersize=4, color = 'red')

# Normalizing %R
maxVal = max(percentR)
print(maxVal, nm[percentR.index(maxVal)])
normPercentR = []
for item in percentR:
    normItem = item/maxVal
    normPercentR.append(normItem)

# Use the F(r) function
F_r = []
for item in normPercentR:
    fr = (1-float(item)**2)/(2*float(item))
    F_r.append(fr)

maxF_R = max(F_r)
minF_R = min(F_r)

#CalcFR norm 2-5.5
F_rnorm = []
for item in F_r:
    item2 = (item-minF_R)/(maxF_R-minF_R)
    F_rnorm.append(item2)
    

# Convert nm to eV
eV = []
for item in nm:
    unitEV = 1242.158/float(item)
    eV.append(unitEV)

# Invert x axis
plt.plot(eV, F_rnorm)
plt.gca().invert_xaxis()

plt.ylabel("Adjusted %R")
plt.xlabel("eV")

plt.show()

