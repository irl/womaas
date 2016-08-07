#!/usr/bin/env python
import sys, subprocess 
import rrdtool, tempfile, time

#fd, path= tempfile.mkstemp('t.png')

MINUTE=100
HALFHOUR=1800
DAY=86400
YEAR=365 * DAY
a=0

var=""
while a == 0 : 
	var=subprocess.Popen(("netstat", "-s"), stdout=subprocess.PIPE)
	var_o=subprocess.check_output(("grep", "OutOctets"), stdin=var.stdout)
	dat=[int(s) for s in var_o.split() if s.isdigit()]
	var=subprocess.Popen(("netstat", "-s"), stdout=subprocess.PIPE)
	var_i=subprocess.check_output(("grep", "InOctets"), stdin=var.stdout)
	dat2=[int(s) for s in var_i.split() if s.isdigit()]
	print dat[0]
	print dat2[0]

	rrdtool.update( 'network.rrd', 'N:%d:%d' %(dat[0], dat2[0]))
	rrdtool.graph('network.png',
		'--imgformat', 'PNG',
		'--width', '550',
		'--height', '150',
		'--start', "-1%s" %MINUTE ,
		'--end', "-1",
		'--vertical-label', 'IN/OUT bits',
		'--title', 'Network Usage',
		'--lower-limit', '0',
		'DEF:test=network.rrd:in:LAST',
		'CDEF:testb=test,8,/',
		'AREA:testb#FF66CC',
		'DEF:test2=network.rrd:out:LAST',
		'CDEF:test2b=test2,8,/',
		'AREA:test2b#9966CC')
	     				
	subprocess.call(["mv", "network.png",  "/home/irl/github/wosaas/static/network.png"])
	time.sleep(2)



