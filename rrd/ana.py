#!/usr/bin/env python
import sys, subprocess 
import rrdtool, tempfile

rrdtool.create( 'test.rrd' , '--start' , '1445705700' ,
		'DS:number:COUNTER:600:U:U' ,
		'RRA:AVERAGE:0.5:1:24' ,
		'RRA:AVERAGE:0.5:6:10')

#rrdtool.u
#print("wtfwtf")
rrdtool.update( 'test.rrd', '1445706300:12250')
rrdtool.update( 'test.rrd', '1445706600:12450')
rrdtool.update( 'test.rrd', '1445706900:12550')
rrdtool.update( 'test.rrd', '1445707200:12650')
rrdtool.update( 'test.rrd', '1445707500:12250')

var=subprocess.check_output(["df", "--output=used"])
HOUR=3600
DAY=86400
YEAR=365 * DAY
dat=[int(s) for s in var.split() if s.isdigit()]
rrdtool.create( 'banana.rrd' , '--start' , '1445723055' , '--step', '60',
               'DS:space:COUNTER:600:U:U' ,
              'DS:space2:COUNTER:600:U:U' ,
		'RRA:AVERAGE:0.5:1:10')
time=subprocess.check_output(["date","+%s"])
space1=dat[0]
space2=dat[2]
print space1
print space2
#rrdtool.update( 'ana.rrd', 'N:%d:%d' %(space1, space2))

fd, path= tempfile.mkstemp('t.png')
rrdtool.graph('tesit.png',
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
	     				
#subprocess.call(["mv", "test.png",  "/tmp/test.png"])




