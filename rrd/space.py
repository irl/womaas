#!/usr/bin/env python
import sys, subprocess 
import rrdtool, tempfile, time

#fd, path= tempfile.mkstemp('t.png')


HOUR=3600
DAY=86400
YEAR=365 * DAY
a=0

while a == 0 :
	var=subprocess.check_output(["df", "--output=used"])
	dat=[int(s) for s in var.split() if s.isdigit()]
	space1=dat[0]
	space2=dat[2]
	print space1
	print space2
	rrdtool.update( 'ana.rrd', 'N:%d:%d' %(space1, space2))

	rrdtool.graph('test.png',
		'--imgformat', 'PNG',
		'--width', '540',
		'--height', '180',
		'--start', "-1%s" %HOUR ,
		'--end', "-1",
		'--vertical-label', 'Usage',
		'--title', 'Storage Space Usage',
		'--lower-limit', '0',
		'DEF:test=ana.rrd:space:AVERAGE',
		'LINE:test#FFF123',
		'DEF:test2=ana.rrd:space2:AVERAGE',
		'LINE2:test2#9966CC')
	     				
	subprocess.call(["mv", "test.png",  "/tmp/test.png"])
	time.sleep(60)



