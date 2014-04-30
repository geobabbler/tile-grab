# -*- coding: utf-8 -*-
"""
The MIT License (MIT)

Copyright (c) 2014 William E. Dollins

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import urllib
import urlparse, os
from optparse import OptionParser
from globalmaptiles import GlobalMercator

def getExtension(urlTemplate):
    path = urlparse.urlparse(urlTemplate).path
    ext = os.path.splitext(path)[1]
    return ext

def getWorldFileExtension(x):
    return {
        '.png': '.pgw',
        '.jpg': '.jgw',
        }.get(x, '.pgw')    # .pgw is default if x not found

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
#parse the bounds
boundsarr = options.bounds.split(';')
lonarr = sorted([float(boundsarr[0]), float(boundsarr[2])])
latarr = sorted([float(boundsarr[1]), float(boundsarr[3])])
z = int(options.zoom)

gm = GlobalMercator()
#Convert bounds to meters
mx0, my0 = gm.LatLonToMeters(latarr[0], lonarr[0])
mx1, my1 = gm.LatLonToMeters(latarr[1], lonarr[1])
#get TMS tile address range
tx0, ty0 = gm.MetersToTile(mx0,my0,z)
tx1, ty1 = gm.MetersToTile(mx1,my1,z)
#sort the tile addresses low to high
xarr = sorted([tx0,tx1])
yarr = sorted([ty0,ty1])
#figure out relevant extensions
extension = getExtension(options.template)
wf = getWorldFileExtension(extension)
#create the destination location using the z value
root = options.destination + '/' + str(z)
try:
    os.makedirs(root)
except:
    print "Could not create destination. It may already exist."


for x in xarr:
    for y in yarr:
        gx = x
        gy = y
        if options.inverty == 'false':
            gx, gy = gm.GoogleTile(x,y,z)
        url = options.template.format(z=options.zoom,x=gx,y=gy)
        
        fname = root + '/' + str(x) + '_' + str(y) + extension
        xscale, xshift, yshift, yscale, xorigin, yorigin = gm.WorldFileParameters(x,y,z)
        newline = str(xscale) + '\n' + str(xshift) + '\n' + str(yshift) + '\n' + str(yscale) + '\n' + str(xorigin) + '\n' + str(yorigin)
        file = open(root + '/' + str(x) + '_' + str(y) + wf, 'w')
        file.write(newline)
        file.close()
        image = urllib.URLopener()
        image.retrieve(url, fname)