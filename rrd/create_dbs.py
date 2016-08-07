#!/usr/bin/env python
import sys, subprocess 
import rrdtool, tempfile
rrdtool.create( 'storage.rrd' , '--start' , 'N' , '--step', '10',
                'DS:space1:GAUGE:10:U:U' ,
                'DS:space2:GAUGE:10:U:U' ,
		'RRA:LAST:0.5:1:50')




