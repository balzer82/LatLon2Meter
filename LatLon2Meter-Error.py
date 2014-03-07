# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import numpy as np
import matplotlib.pylab as plt
print('Matplotlib Version %s' % plt.__version__)
%pylab inline --no-import-all

# <headingcell level=1>

# Difference between Pythagoras and Haversine Distance

# <headingcell level=3>

# Function, which calculates the difference

# <codecell>

def calcD(dla, dlo):
    lat2 = lat1+dla
    lon2 = lon1+dlo
    
    # Pythagoras
    lat = 0.5*(lat1+lat2) * np.pi/180.0 # to RAD for Cos()
    dx = arc * np.cos(lat) * (lon2-lon1)
    dy = arc * (lat2 - lat1)
    dist2=np.sqrt(dx**2 + dy**2)
    
    D['dla'].append(dla)
    D['dlo'].append(dlo)
    D['lat2'].append(lat2)
    D['lon2'].append(lon2)
    D['pythagoras'].append(dist2)
    
    #print('Entfernung aus Pythagoras:\t\t%.3fm (ca. %dkm)' % (dist2*1000.0, dist2))
    
    # Haversine Formula
    dlat=(lat1-lat2)*np.pi/180.0
    dlon=(lon1-lon2)*np.pi/180.0
    
    
    a = np.sin(dlat/2) * np.sin(dlat/2) + np.cos(lat1*np.pi/180.0) \
            * np.cos(lat2*np.pi/180.0) * np.sin(dlon/2) * np.sin(dlon/2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    dist3 = R * c
    
    D['haversine'].append(dist3)
    
    #print('Entfernung aus Haversine:\t\t%.3fm (ca. %dkm)' % (dist3*1000.0, dist3))
    
    # Difference
    diff = 1000.0*(dist3-dist2) # in Meter
    
    D['diff'].append(diff)

# <headingcell level=3>

# Geometric Assumptions and Startpoint

# <codecell>

arc = 111.323872 # km/°
R = 6378.388 # Earth Radius
lat1= 51.32
lon1= 13.20

# <headingcell level=3>

# Prepare the Dictionary

# <codecell>

D={}
D['lat2']=[]
D['lon2']=[]
D['pythagoras']=[]
D['haversine']=[]
D['diff']=[]
D['dla']=[]
D['dlo']=[]

# <codecell>

dla = np.linspace(-5.0, 5.0, 100, endpoint=True)
dlo = np.linspace(-5.0, 5.0, 100, endpoint=True)

# <headingcell level=3>

# Calculate Error for Variation of Latitude

# <codecell>

for i in range(len(dla)):
    calcD(dla[i], 0.0)

# <codecell>

plt.plot(D['dla'], D['diff'], label='Difference Pythagoras/Haversine')
plt.xlabel('$\Delta Lat [^\circ]$')
plt.ylabel('$\Delta m$')
plt.scatter(0.0, 0.0, s=100, c='#FF6700')
plt.annotate('%.2f $^\circ Lat$' % lat1, (0.0, -0.0005),xycoords='data', \
            xytext=(0.0, -0.0012), textcoords='data', ha='center', va='center', \
            arrowprops=dict(arrowstyle="fancy", color='k'), fontsize=16)
plt.legend(loc='best')
plt.savefig('Delta-Latitude.png', dpi=150, transparent=True, bbox_inches='tight')

# <codecell>

D={}
D['lat2']=[]
D['lon2']=[]
D['pythagoras']=[]
D['haversine']=[]
D['diff']=[]
D['dla']=[]
D['dlo']=[]

# <headingcell level=3>

# Calculate Error for Variation of Longitude

# <codecell>

for i in range(len(dlo)):
    calcD(0.0, dlo[i])

# <codecell>

plt.plot(D['dlo'], D['diff'], label='Difference Pythagoras/Haversine')
plt.xlabel('$\Delta Lon [^\circ]$')
plt.ylabel('$\Delta m$')
plt.scatter(0.0, 0.0, s=100, c='#FF6700')
plt.annotate('%.2f $^\circ Lon$' % lon1, (0.0, -10.0),xycoords='data', \
            xytext=(0.0, -30.0), textcoords='data', ha='center', va='center', \
            arrowprops=dict(arrowstyle="fancy", color='k'), fontsize=16)
plt.legend(loc='best')
plt.savefig('Delta-Longitude.png', dpi=150, transparent=True, bbox_inches='tight')

# <headingcell level=2>

# Conclusion

# <markdowncell>

# As you can see, the Error depends, wheather you are going East/West or North/South and where you are (Starting Point).

