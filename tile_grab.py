# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 11:22:45 2014
command line: --bbox minx;miny;maxx;maxy --inverty true/false --zoom 3 -urltemplate tokenized_url
@author: dollinsw
"""
import urllib
import os
from optparse import OptionParser
from globalmaptiles import GlobalMercator

parser = OptionParser(usage="usage: %prog [options] filename")
parser.add_option('-b', '--bbox', 
                  action='store',
                  dest='bounds',
                  default='0;0;0;0',
                  help='bounds from which to extract tiles',)
parser.add_option('-d', '--destination', 
                  action='store',
                  dest='destination',
                  default='/',
                  help='file system directory to which tiles will be extracted',)
parser.add_option('-i', '--inverty',
                      type='choice',
                      action='store',
                      dest='inverty',
                      choices=['true', 'false',],
                      default='true',
                      help='indicates inverted y axis',)
parser.add_option("-z", "--zoom", 
                  type='choice',
                  action="store",
                  dest="zoom",
                  choices=['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19',],
                  default='0',
                  help="zoom level (0 - 19)",)
parser.add_option('-u', '--urltemplate', 
                  action='store',
                  dest='template',
                  default='',
                  help='tokenized url template',)
(options, args) = parser.parse_args()
#print options.zoom
#print options.template.format(z=options.zoom,x='x',y='y')
boundsarr = options.bounds.split(';')
lonarr = sorted([float(boundsarr[0]), float(boundsarr[2])])
latarr = sorted([float(boundsarr[1]), float(boundsarr[3])])
z = int(options.zoom)

gm = GlobalMercator()
mx0, my0 = gm.LatLonToMeters(latarr[0], lonarr[0])
mx1, my1 = gm.LatLonToMeters(latarr[1], lonarr[1])

tx0, ty0 = gm.MetersToTile(mx0,my0,z)
tx1, ty1 = gm.MetersToTile(mx1,my1,z)
print tx0,ty0
print tx1,ty1

xarr = sorted([tx0,tx1])
yarr = sorted([ty0,ty1])

root = options.destination + '/' + str(z)
os.makedirs(root)

for x in xarr:
    for y in yarr:
        gx = x
        gy = y
        if options.inverty == 'false':
            gx, gy = gm.GoogleTile(x,y,z)
        url = options.template.format(z=options.zoom,x=gx,y=gy)
        print url
        fname = root + '/' + str(x) + '_' + str(y) + '.png'
        xscale, xshift, yshift, yscale, xorigin, yorigin = gm.WorldFileParameters(x,y,z)
        newline = str(xscale) + '\n' + str(xshift) + '\n' + str(yshift) + '\n' + str(yscale) + '\n' + str(xorigin) + '\n' + str(yorigin)
        file = open(root + '/' + str(x) + '_' + str(y) + '.pgw', 'w')
        file.write(newline)
        file.close()
        image = urllib.URLopener()
        image.retrieve(url, fname)
        

#print args
#print options["-bbox"]