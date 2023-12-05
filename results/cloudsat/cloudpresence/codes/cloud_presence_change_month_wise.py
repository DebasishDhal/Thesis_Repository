import matplotlib.pyplot as plt
#Output - https://github.com/DebasishDhal/Thesis_Repository/blob/main/results/cloudsat/cloudpresence/images/timeseries2013.png

month = 'January'
janlandthatisclear = 40.6
janlandthatiscloudy = 59.4
janoceanthatisclear = 23.8
janoceanthatiscloudy = 76.2

month = 'February'
feblandthatisclear = 39.7
feblandthatiscloudy = 60.3
feboceanthatisclear = 25.9
feboceanthatiscloudy = 74.1

month = 'March'
marlandthatisclear = 37.8
marlandthatiscloudy = 62.2
maroceanthatisclear = 25
maroceanthatiscloudy = 75

month = 'April'
aprlandthatisclear = 36.2
aprlandthatiscloudy = 63.8
aproceanthatisclear = 23.5
aproceanthatiscloudy = 76.5

month = 'May'
maylandthatisclear = 32.7
maylandthatiscloudy = 67.3
mayoceanthatisclear = 18.1
mayoceanthatiscloudy = 81.9

month = 'June'
junlandthatisclear = 34.7
junlandthatiscloudy = 65.3
junoceanthatisclear = 19.1
junoceanthatiscloudy = 80.9

month = 'July'
jullandthatisclear = 35
jullandthatiscloudy = 65
juloceanthatisclear = 20.4
juloceanthatiscloudy = 79.6

month = 'August'
auglandthatisclear = 32.
auglandthatiscloudy = 68
augoceanthatisclear = 19.4
augoceanthatiscloudy = 80.6

month = 'September'
seplandthatisclear = 30.4
seplandthatiscloudy = 69.6
sepoceanthatisclear = 19.3
sepoceanthatiscloudy = 80.7

month = 'October'
octlandthatisclear = 39
octlandthatiscloudy = 61
octoceanthatisclear = 19.5
octoceanthatiscloudy = 80.5

month = 'November'
novlandthatisclear = 40.3
novlandthatiscloudy = 59.7
novoceanthatisclear = 20.5
novoceanthatiscloudy = 79.5

month = 'December'
declandthatisclear = 41.9
declandthatiscloudy = 58.1
decoceanthatisclear = 21.7
decoceanthatiscloudy = 78.3

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November','December']

landthatisclear = [janlandthatisclear, feblandthatisclear, marlandthatisclear, aprlandthatisclear, maylandthatisclear, junlandthatisclear, jullandthatisclear, auglandthatisclear, seplandthatisclear, octlandthatisclear, novlandthatisclear, declandthatisclear]
landthatiscloudy = [janlandthatiscloudy, feblandthatiscloudy, marlandthatiscloudy, aprlandthatiscloudy, maylandthatiscloudy, junlandthatiscloudy, jullandthatiscloudy, auglandthatiscloudy, seplandthatiscloudy, octlandthatiscloudy, novlandthatiscloudy, declandthatiscloudy]
oceanthatisclear = [janoceanthatisclear, feboceanthatisclear, maroceanthatisclear, aproceanthatisclear, mayoceanthatisclear, junoceanthatisclear, juloceanthatisclear, augoceanthatisclear, sepoceanthatisclear, octoceanthatisclear, novoceanthatisclear, decoceanthatisclear]
oceanthatiscloudy = [janoceanthatiscloudy, feboceanthatiscloudy, maroceanthatiscloudy, aproceanthatiscloudy, mayoceanthatiscloudy, junoceanthatiscloudy, juloceanthatiscloudy, augoceanthatiscloudy, sepoceanthatiscloudy, octoceanthatiscloudy, novoceanthatiscloudy, decoceanthatiscloudy]

cloudycleardf  = pd.DataFrame({'month': months, 'landthatisclear': landthatisclear, 'landthatiscloudy': landthatiscloudy, 'Ocean that is Clear': oceanthatisclear, 'oceanthatiscloudy': oceanthatiscloudy})

#Plot them
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(cloudycleardf['month'], cloudycleardf['landthatisclear'], color='#FF0000', label='Land that is Clear')
ax.plot(cloudycleardf['month'], cloudycleardf['landthatiscloudy'], color='#008000', label='Land that is Cloudy')
ax.plot(cloudycleardf['month'], cloudycleardf['Ocean that is Clear'], color='#0000FF', label='Ocean that is Clear')
ax.plot(cloudycleardf['month'], cloudycleardf['oceanthatiscloudy'], color='#FFA500', label='Ocean that is Cloudy')
ax.set_xlabel('Month', fontsize=14)
ax.set_ylabel('Percentage of Pixels', fontsize=14)
ax.legend(loc='upper right')

#Give the following colors to the lines, land that is clear: red, land that is cloudy:green , ocean that is clear: blue, ocean that is cloudy: orange

#Plot them



plt.legend(bbox_to_anchor=(0.25, 0.65), loc='upper left', borderaxespad=0.)
plt.title('Percentage of Land/Ocean pixels that are Clear/Cloudy for each month (2013)', fontsize=14)
ax.set_xticklabels(cloudycleardf['month'], rotation=45)
#Show numbers at each point

for i, txt in enumerate(cloudycleardf['landthatisclear']):
    ax.annotate(txt, (cloudycleardf['month'][i], cloudycleardf['landthatisclear'][i]+0.5))
for i, txt in enumerate(cloudycleardf['landthatiscloudy']):
    ax.annotate(txt, (cloudycleardf['month'][i], cloudycleardf['landthatiscloudy'][i]+0.5))
for i, txt in enumerate(cloudycleardf['Ocean that is Clear']):
    ax.annotate(txt, (cloudycleardf['month'][i], cloudycleardf['Ocean that is Clear'][i]+0.5))
for i, txt in enumerate(cloudycleardf['oceanthatiscloudy']):
    ax.annotate(txt, (cloudycleardf['month'][i], cloudycleardf['oceanthatiscloudy'][i]+0.5))





plt.show()

