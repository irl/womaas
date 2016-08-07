#!/usr/bin/env python
import sys, subprocess 
import rrdtool, tempfile, time

#fd, path= tempfile.mkstemp('t.png')

MINUTE=200
HALFHOUR=1800
DAY=86400
YEAR=365 * DAY
a=0


while a == 0 :
	var=subprocess.check_output(["df", "--output=used"])
	dat=[int(s) for s in var.split() if s.isdigit()]
	space1=dat[4]
	space2=dat[8]
	print space1
	print space2
	rrdtool.update( 'storage.rrd', 'N:%d:%d' %(space1, space2))

	rrdtool.graph('storage.png',
		'--imgformat', 'PNG',
		'--width', '540',
		'--height', '180',
		'--start', "-1%s" %MINUTE ,
		'--end', "-1",
		'--vertical-label', 'Usage, GB',
		'--title', 'Storage Space Usage',
#		'--lower-limit', '0',
		'DEF:test=storage.rrd:space1:LAST',
		'CDEF:testb=test,1024,*',
		'AREA:testb#9966CC',
		'DEF:test2=storage.rrd:space2:LAST',
		'CDEF:test2b=test2,1024,*',
		'LINE2:test2b#9966CC')
	     				
	subprocess.call(["mv", "storage.png",  "/home/irl/github/wosaas/static/storage.png"])
	time.sleep(9)



