# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import numpy as np
import requests
import sys, os
import matplotlib.pylab as plt
from mpl_toolkits.basemap import Basemap
#print('Matplotlib Version %s' % plt.__version__)

# <headingcell level=2>

# Reverse Geoencoding

# <codecell>

# Source: https://gist.github.com/bradmontgomery/5397472
def getadress(latitude,longitude):
    # grab some lat/long coords from wherever. For this example,
    # I just opened a javascript console in the browser and ran:
    #
    # navigator.geolocation.getCurrentPosition(function(p) {
    #   console.log(p);
    # })
    #
    #latitude = 35.1330343
    #longitude = -90.0625056
 
    # Did the geocoding request comes from a device with a
    # location sensor? Must be either true or false.
    sensor = 'true'
 
    # Hit Google's reverse geocoder directly
    # NOTE: I *think* their terms state that you're supposed to
    # use google maps if you use their api for anything.
    base = "http://maps.googleapis.com/maps/api/geocode/json?"
    params = "latlng={lat},{lon}&sensor={sen}".format(
        lat=latitude,
        lon=longitude,
        sen=sensor
    )
    url = "{base}{params}".format(base=base, params=params)
    response = requests.get(url)

    return response.json()['results'][1]['formatted_address']

# <headingcell level=1>

# Main

# <codecell>

if len(sys.argv) == 5:
    lat1 = float(sys.argv[1])
    lon1 = float(sys.argv[2])
    lat2 = float(sys.argv[3])
    lon2 = float(sys.argv[4])
else:
    # Start
    lat1 = 38.7436265
    lon1 = -9.1602036
    # Ziel
    lat2 = 52.5075419
    lon2 = 13.4261418
    print('Usage: %s latfrom lonfrom latto lonto (in Decimaldegree)' % sys.argv[0])
    
sadr = getadress(lat1, lon1)
eadr = getadress(lat2, lon2)
print('Calculating Distance from %s to %s' % (sadr, eadr))


lat0=(lat1+lat2)/2.0
lon0=(lon1+lon2)/2.0

# <headingcell level=2>

# Einfache Entfernungsberechnung über Pythagoras

# <markdowncell>

# Abstand zwischen zwei Breitenkreisen ist ca. $111.3 \frac{km}{\circ}$.
# Am Äquator ist die Entfernung zwischen zwei Längenkreisen ebenfalls $111.3 \frac{km}{\circ}$, an den Polen allerdings $0 \frac{km}{\circ}$. Daher muss $dx$ mit $\Delta Lon \cdot \cos(Lat)$ berechnet werden.

# <codecell>

plt.plot(np.arange(0,90.0, 1), 111.3*np.cos(np.arange(0,90.0*np.pi/180.0, 1.0*np.pi/180.0)))
plt.xlabel('Lat in $^\circ$')
plt.ylabel('$km/^\circ$ Lon')

# <codecell>

lat = lat0 * np.pi/180.0 # to RAD for Cos()

dx = 111.3 * np.cos(lat) * (lon1-lon2)
dy = 111.3 * (lat1 - lat2)
dist = np.sqrt(dx**2 + dy**2)
print('Entfernung aus Pythagoras:\t\t%.3fm (ca. %dkm)' % (dist*1000.0, dist))

# <headingcell level=2>

# Entfernung des Großkreis über Seitenkosinus

# <markdowncell>

# $$r_\text{Erde}=6378.388km$$
# $$d=r_\text{Erde} \cdot \arccos\left(\sin(lat1)\sin(lat2) + \cos(lat1)\cos(lat2)\cos(lon2-lon1)\right)$$

# <codecell>

dist2 = 6378.388 * np.arccos(np.sin(lat1*np.pi/180.0)*np.sin(lat2*np.pi/180.0)+
                             np.cos(lat1*np.pi/180.0)*np.cos(lat2*np.pi/180.0)*
                             np.cos(lon2*np.pi/180.0-lon1*np.pi/180.0))
print('Entfernung aus Seitencosinus:\t\t%.3fm (ca. %dkm)' % (dist2*1000.0, dist2))

# <headingcell level=2>

# Differenz

# <codecell>

diff = dist2-dist
print('Berechnung über Pythagoras macht %.2fkm (%.2f%%) Fehler.' % (diff, np.abs(diff*100.0/dist2)))

# <headingcell level=2>

# Grafisch

# <codecell>

fig = plt.figure(figsize=(9,9))
m = Basemap(projection='ortho',lon_0=lon0,lat_0=lat0,resolution='l')
m.shadedrelief()

# draw parallels and meridians.
m.drawparallels(np.arange(-90.,120.,30.))
m.drawmeridians(np.arange(0.,420.,10.))

# draw distance
m.drawgreatcircle(lon1,lat1,lon2,lat2,linewidth=2,color='b')

# draw km
x, y = m(lon0, lat0+0.5)
sx,sy= m(lon1, lat1)
ex,ey= m(lon2, lat2)
plt.text(x, y, '%dkm' % (dist2), color='k', ha='center', va='bottom',fontsize=14)
plt.text(sx,sy, sadr, color='k', ha='left',fontsize=9)
plt.text(ex,ey, eadr, color='k', ha='left',fontsize=9)
fig.savefig('Distance.png',dpi=72,transparent=True,bbox_inches='tight')

# <codecell>

print('\'Distance.png\' saved. Done.')

