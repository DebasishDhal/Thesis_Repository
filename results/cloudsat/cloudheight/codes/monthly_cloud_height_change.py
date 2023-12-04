import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patches as mpatches

topheightdf = pd.DataFrame()
cloud_types = ['Cirrus','Altostratus','Altocumulus','Stratus','Stratocumulus','Cumulus','Nimbostratus','Deep Convective']


jantop = [12.74,7.8,4.95,1.41,2.04,1.68,6.88,12.66]
janthick = [1.55,3.06,1.38,0.53,0.83,0.69,5.59,11.84]
janbottom = [jantop[i] - janthick[i] for i in range(len(jantop))]

febtop = [12.44,7.51,4.91,1.43,2.06,1.66,6.63,12.56]
febthick = [1.54,3.0,1.35,0.55,0.86,0.7,5.47,11.76]
febbottom = [febtop[i] - febthick[i] for i in range(len(febtop))]

martop = [12.23,7.59,5.03,1.31,1.89,1.6,6.66,12.76]
marthick = [1.49,3.1,1.31,0.53,0.86,0.68,5.56,11.94]
marbottom = [martop[i] - marthick[i] for i in range(len(martop))]

aprtop = [12.12,7.75,4.95,1.22,1.78,1.62,6.83,12.56]
aprthick = [1.49,3.26,1.33,0.53,0.84,0.7,5.75,11.74]
aprbottom = [aprtop[i] - aprthick[i] for i in range(len(aprtop))]

maytop = [12.24,7.99,4.93,1.13,1.66,1.69,7.1,12.54]
maythick = [1.52,3.35,1.37,0.53,0.79,0.74,5.98,11.73]
maybottom = [maytop[i] - maythick[i] for i in range(len(maytop))]

juntop = [12.08,8.44,4.81,1.09,1.65,1.79,7.45,12.41]
junthick = [1.52,3.63,1.32,0.46,0.7,0.79,6.35,11.55]
junbottom = [juntop[i] - junthick[i] for i in range(len(juntop))]

jultop = [11.89,8.72,4.85,1.12,1.67,1.82,7.71,12.29]
julthick = [1.51,3.82,1.3,0.41,0.69,0.8,6.59,11.36]
julbottom = [jultop[i] - julthick[i] for i in range(len(jultop))]

augtop = [11.8,8.45,4.2,1.16,1.66,1.76,7.47,12.31]
augthick = [1.5,3.72,1.31,0.45,0.7,0.77,6.36,11.38]
augbottom = [augtop[i] - augthick[i] for i in range(len(augtop))]

septop = [11.81,8.23,4.74,1.36,1.75,1.68,7.24,12.61]
septhick = [1.53,3.61,1.39,0.56,0.77,0.72,6.05,11.73]
sepbottom = [septop[i] - septhick[i] for i in range(len(septop))]

octtop = [11.98,7.86,4.87,1.38,1.86,1.63,6.84,12.87]
octthick = [1.48,3.29,1.35,0.59,0.84,0.69,5.75,12.06]
octbottom = [octtop[i] - octthick[i] for i in range(len(octtop))]

novtop = [12.11,7.81,4.9,1.35,1.94,1.65,6.89,12.74]
novthick = [1.48,3.13,1.34,0.54,0.83,0.68,5.72,11.92]
novbottom = [novtop[i] - novthick[i] for i in range(len(novtop))]

dectop = [12.37,7.83,4.85,1.42,2.00,1.64,6.89,12.80]
decthick = [1.55,3.2,1.32,0.53,0.80,0.67,5.74,11.95]
decbottom = [dectop[i] - decthick[i] for i in range(len(dectop))]

#Plan, 1 plot will be there. Cloud types will be color coded, x-axis will be months, the y-axis will be the height of the cloud. Top-bottom-thickness will be done through linestyles

fig,ax = plt.figure(figsize=(10,8)),plt.gca()

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November','December']
colorcode = ['red', 'blue', 'green', 'orange', 'purple', 'yellow', 'pink', 'black']
linestylecode = ['solid', 'dashed', 'dashdot']

for i in range(8):
    ax.plot(months, [jantop[i], febtop[i], martop[i], aprtop[i], maytop[i], juntop[i], jultop[i], augtop[i], septop[i], octtop[i], novtop[i], dectop[i]],
            color=colorcode[i], linestyle = linestylecode[0]);
    ax.plot(months, [janbottom[i], febbottom[i], marbottom[i], aprbottom[i], maybottom[i], junbottom[i], julbottom[i], augbottom[i], sepbottom[i], octbottom[i], novbottom[i], decbottom[i]],
            color=colorcode[i], linestyle = linestylecode[1]);
    ax.plot(months, [janthick[i], febthick[i], marthick[i], aprthick[i], maythick[i], junthick[i], julthick[i], augthick[i], septhick[i], octthick[i], novthick[i], decthick[i]],
            color=colorcode[i], linestyle = linestylecode[2]);

plt.xticks(rotation=45);
plt.xlabel('Month', fontsize= 16);
plt.ylabel('Height (km) (Log scale)', fontsize = 16);
plt.tick_params(axis='x', labelsize=14)
plt.yscale('log');

legend_patches = []
for i in range(len(cloud_types)):
    patch = mpatches.Patch(color=colorcode[i], label=cloud_types[i])
    legend_patches.append(patch)

#Placing the legend just outside of the plot, to the right
legend_title = "Cloud Types - Colors"
plt.legend(handles=legend_patches, title = "Color - Cloud type",bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.0)


box_x = 0.815 # X-coordinate of the box
box_y = 0.52 # Y-coordinate of the box
box_width = 0.17  # Width of the box
box_height = 0.18  # Height of the box
box_color = 'none'  # Color of the box
box_linewidth = 1  # Linewidth of the box
box_edgecolor = 'black'  # Edge color of the box

# Drawing the box
box = mpatches.Rectangle((box_x, box_y), box_width, box_height, facecolor=box_color, edgecolor=box_edgecolor,
                         linewidth=box_linewidth, transform=fig.transFigure)
fig.add_artist(box)

# Adding text into the box
text = 'Linestyle-Height\n\nSolid-Top\nDashed-Bottom\nDashdot-Thickness'

ax.text(11.8, 3.5, text, fontsize=12,verticalalignment='top')
plt.yticks([0.5,1,2,3,4,5,6,7,8,9,10,11,12], ['0.5','1','2', '3','4','5','6','7','8','9','10','11','12']);

# Hiding the axis and display the plot
plt.tight_layout()
plt.title('Cloud average top, bottom height and thickness over months (2013)', fontsize = 16);
plt.show()
