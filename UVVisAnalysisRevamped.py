# -*- coding: utf-8 -*-
"""
"""
##Racheal Fisher
#To use this code, copy your data and put it in two columns in a txt with nothing else

# Import programs
import matplotlib.pyplot as plt
import csv
import matplotlib.font_manager as fm
from matplotlib.ticker import FormatStrFormatter
import matplotlib.gridspec as gridspec

# Create figure
# Create multiple
# graph, (plot1, plot2) = plt.subplots(1, 2)
fig, ax = plt.subplots(figsize=(3, 3), dpi=600)
gs = gridspec.GridSpec(1, 2, width_ratios=[6, 0.1], wspace=.0002)  # Adjust width ratio for the empty space

ax = plt.subplot(gs[0])

filename = "(RG1-13) CuTA with Zn + Cd.csv"

allWavelength = []
allPercentR = []

with open(filename, 'r') as file:
    csvreader = csv.reader(file)

    # Flag to indicate whether to start adding values
    start_adding_values = False

    for row in csvreader:
        if start_adding_values:
            for i in range(0, len(row), 2):
                # Ensure we have enough elements in the row
                if i + 1 < len(row):
                    # Attempt to convert values to float
                    try:
                        wavelength = float(row[i])
                        percentR = float(row[i + 1])
                        
                        # Append to respective lists
                        if len(allWavelength) <= i // 2:
                            allWavelength.append([])
                        if len(allPercentR) <= i // 2:
                            allPercentR.append([])
                        
                        allWavelength[i // 2].append(wavelength)
                        allPercentR[i // 2].append(percentR)
                    except ValueError:
                        # Print the problematic values
                        print("Unable to convert to float:", row[i], row[i + 1])

        # Check for the marker indicating the start of values
        if row and "Wavelength (nm)" in row:
            start_adding_values = True

# Print the collected values
# print("Wavelengths:", allWavelength)
# print("Percent R:", allPercentR)

# Iterate through each column and plot the data
for index, wavelengths in enumerate(allWavelength):
    percent_r_values = allPercentR[index]

    for x in wavelengths:
        if x > 200 and x < 1500:
            # Check for big change in y values over 1 x value change
            if percent_r_values[wavelengths.index(x)] - percent_r_values[wavelengths.index(x)- 1] >= 0:
                x1 = x
                x2 = wavelengths[wavelengths.index(x) - 1]
                y1 = percent_r_values[wavelengths.index(x)]
                y2 = percent_r_values[wavelengths.index(x) - 1]

    shiftSize = (y2-y1)
    print(shiftSize)

    # Correct the shift
    for x in wavelengths:
        if x>=x1:
            percent_r_values[wavelengths.index(x)] = percent_r_values[wavelengths.index(x)] + shiftSize
    
    maxVal = max(percent_r_values)
    normPercentR = []
    for item in percent_r_values:
        normItem = item/maxVal
        normPercentR.append(normItem)
        
    F_r = []
    for item in normPercentR:
        fr = (1-float(item)**2)/(2*float(item))
        F_r.append(fr)
    # (1-x)^2/(2x)
    maxF_R = max(F_r)
    minF_R = min(F_r)
    
    #CalcFR norm 2-5.5
    F_rnorm = []
    for item in F_r:
        item2 = (item-minF_R)/(maxF_R-minF_R)
        # (x-min)/(max-min)
        F_rnorm.append(item2)
        
        # Convert nm to eV
    eV = []
    for item in wavelengths:
        unitEV = 1242.158/float(item)
        eV.append(unitEV)
    customLabel = input(f"Enter a label for line {index + 1}: ")
    ax.plot(eV, F_rnorm, label=customLabel)
    
# Font properties
font = fm.FontProperties(family='Arial', size=9)

# Set labels, title, and legend
ax.set_xlabel('eV', fontproperties=font)
ax.set_ylabel('%R Normalized', fontproperties=font)
ax.set_title('My title', fontproperties=font)
leg = ax.legend(loc="upper right", bbox_to_anchor=(1.4,1.2), prop=font)

# Set tick labels
ax.set_xticklabels(ax.get_xticks(), fontproperties=font)
ax.set_yticklabels(ax.get_yticks(), fontproperties=font)
ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
ax.margins()

# Empty space on the right
ax_empty = plt.subplot(gs[1])
ax_empty.axis('off')
plt.tight_layout()

print(len(allWavelength))


