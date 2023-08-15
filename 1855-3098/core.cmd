#Command file
set clobber
set nomarks
si harness

print "T"
se 8
printf "******** Printing and Plotting the Transfer characteristics of FET******** \n" >> out.txt
print "T DS VG: 3.92E+00 Model VG: %s V  @ ID:4.16E+00 Delta: %s" abs(xcross(abs(i(vd)),4.16E+00)) abs(abs(xcross(abs(i(vd)),4.16E+00))-3.92E+00)
print "T DS VG: 4.36E+00 Model VG: %s V  @ ID:2.32E+01 Delta: %s" abs(xcross(abs(i(vd)),2.32E+01)) abs(abs(xcross(abs(i(vd)),2.32E+01))-4.36E+00)
print "T DS VG: 4.60E+00 Model VG: %s V  @ ID:4.51E+01 Delta: %s" abs(xcross(abs(i(vd)),4.51E+01)) abs(abs(xcross(abs(i(vd)),4.51E+01))-4.60E+00)
print "T DS VG: 4.81E+00 Model VG: %s V  @ ID:6.63E+01 Delta: %s" abs(xcross(abs(i(vd)),6.63E+01)) abs(abs(xcross(abs(i(vd)),6.63E+01))-4.81E+00)
print "T DS VG: 4.94E+00 Model VG: %s V  @ ID:8.03E+01 Delta: %s" abs(xcross(abs(i(vd)),8.03E+01)) abs(abs(xcross(abs(i(vd)),8.03E+01))-4.94E+00)
print "T DS VG: 5.02E+00 Model VG: %s V  @ ID:9.18E+01 Delta: %s" abs(xcross(abs(i(vd)),9.18E+01)) abs(abs(xcross(abs(i(vd)),9.18E+01))-5.02E+00)

print "S"
se 1
print "S AT VG: 4.00E+00 DS ID: 3.77E+00 Model ID: %sA DELTA: %sA OOD: %sX" yvalue(abs(i(vd)),2.53E+00) abs(yvalue(abs(i(vd)),2.53E+00)-3.77E+00) (yvalue(abs(i(vd)),2.53E+00)/(3.77E+00))
print "S AT VG: 4.00E+00 DS ID: 4.31E+00 Model ID: %sA DELTA: %sA OOD: %sX" yvalue(abs(i(vd)),3.32E+00) abs(yvalue(abs(i(vd)),3.32E+00)-4.31E+00) (yvalue(abs(i(vd)),3.32E+00)/(4.31E+00))
se 2 
print "S AT VG: 5.00E+00 DS ID: 7.76E+01 Model ID: %sA DELTA: %sA OOD: %sX" yvalue(abs(i(vd)),1.92E+00) abs(yvalue(abs(i(vd)),1.92E+00)-7.76E+01) (yvalue(abs(i(vd)),1.92E+00)/(7.76E+01))
print "S AT VG: 5.00E+00 DS ID: 8.79E+01 Model ID: %sA DELTA: %sA OOD: %sX" yvalue(abs(i(vd)),2.59E+00) abs(yvalue(abs(i(vd)),2.59E+00)-8.79E+01) (yvalue(abs(i(vd)),2.59E+00)/(8.79E+01))

print "L"
printf "*******Plotting the output characteristics of FET in Linear Region******* \n" >> out.txt
se 1
print "L AT VG: 4.00E+00 DS ID: 2.70E+00 Model ID: %sA DELTA: %sA OOD: %sX" yvalue(abs(i(vd)),4.72E-01) abs(yvalue(abs(i(vd)),4.72E-01)-2.70E+00) (yvalue(abs(i(vd)),4.72E-01)/(2.70E+00))
se 2
print "L AT VG: 5.00E+00 DS ID: 4.91E+01 Model ID: %sA DELTA: %sA OOD: %sX" yvalue(abs(i(vd)),5.60E-01) abs(yvalue(abs(i(vd)),5.60E-01)-4.91E+01) (yvalue(abs(i(vd)),5.60E-01)/(4.91E+01))
se 3
print "L AT VG: 6.00E+00 DS ID: 9.85E+01 Model ID: %sA DELTA: %sA OOD: %sX" yvalue(abs(i(vd)),3.75E-01) abs(yvalue(abs(i(vd)),3.75E-01)-9.85E+01) (yvalue(abs(i(vd)),3.75E-01)/(9.85E+01))
se 4
print "L AT VG: 7.00E+00 DS ID: 1.20E+02 Model ID: %sA DELTA: %sA OOD: %sX" yvalue(abs(i(vd)),3.43E-01) abs(yvalue(abs(i(vd)),3.43E-01)-1.20E+02) (yvalue(abs(i(vd)),3.43E-01)/(1.20E+02))


#si rdson
#printf "**********Rds(on) test********* \n "
#se 1
#print "When Id= 20A and vgs=10V  Model's Rds=%s ohm DS Rds(max)=2.88m ohm\n" abs(xcross(abs(i(vd)),20))/20
#se 2
#print "When Id= 15A and vgs=7.5V  Model's Rds=%s ohm DS Rds(max)=3.50m ohm\n" abs(xcross(abs(i(vd)),15))/15
##
##
#si cap
#print " ***********Capacitance test************** \n "
#print " Measured ciss: %s pf DS ciss: 4415pf \n" (1/(2*3.14*1meg*yvalue(abs(((v(g)-v(d))/i(rd))),1meg)))*1e12+(1/(2*3.14*1meg*yvalue(abs(((v(g)-v(s))/i(rs))),1meg)))*1e12
#print " Measured crss: %s pf DS crss: 26f \n" (1/(2*3.14*1meg*yvalue(abs(((v(g)-v(d))/i(rd))),1meg)))*1e12
#print " Ratio of Crss and Ciss is : %s \n" (26/4415)
