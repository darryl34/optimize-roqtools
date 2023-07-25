#Command file
set clobber
set nomarks
si harness

print "T"
se 8
printf "******** Printing and Plotting the Transfer characteristics of FET******** \n" >> out.txt
print "DS VG: 3.92E+00 Model VG: %s V  @ ID:4.16E+00 Delta: %s" abs(xcross(abs(i(vd)),4.16E+00)) abs(abs(xcross(abs(i(vd)),4.16E+00))-3.92E+00)
print "DS VG: 4.36E+00 Model VG: %s V  @ ID:2.32E+01 Delta: %s" abs(xcross(abs(i(vd)),2.32E+01)) abs(abs(xcross(abs(i(vd)),2.32E+01))-4.36E+00)
print "DS VG: 4.60E+00 Model VG: %s V  @ ID:4.51E+01 Delta: %s" abs(xcross(abs(i(vd)),4.51E+01)) abs(abs(xcross(abs(i(vd)),4.51E+01))-4.60E+00)
print "DS VG: 4.81E+00 Model VG: %s V  @ ID:6.63E+01 Delta: %s" abs(xcross(abs(i(vd)),6.63E+01)) abs(abs(xcross(abs(i(vd)),6.63E+01))-4.81E+00)
print "DS VG: 4.94E+00 Model VG: %s V  @ ID:8.03E+01 Delta: %s" abs(xcross(abs(i(vd)),8.03E+01)) abs(abs(xcross(abs(i(vd)),8.03E+01))-4.94E+00)
print "DS VG: 5.02E+00 Model VG: %s V  @ ID:9.18E+01 Delta: %s" abs(xcross(abs(i(vd)),9.18E+01)) abs(abs(xcross(abs(i(vd)),9.18E+01))-5.02E+00)
#print "Total error: %s%%" T_perror*100
#print "Average error: %s%%" T_perror*100/8
#T_err_tot=abs(abs(xcross(abs(i(vd)),1.55E-04))-8.46E-01)+abs(abs(xcross(abs(i(vd)),8.32E-02))-1.03E+00)+abs(abs(xcross(abs(i(vd)),3.24E-01))-1.23E+00)+abs(abs(xcross(abs(i(vd)),7.69E-01))-1.43E+00)+abs(abs(xcross(abs(i(vd)),1.23E+00))-1.60E+00)+abs(abs(xcross(abs(i(vd)),1.66E+00))-1.76E+00)+abs(abs(xcross(abs(i(vd)),2.08E+00))-1.89E+00)+abs(abs(xcross(abs(i(vd)),2.42E+00))-2.01E+00)
#print " ID        Total             Average"
#print " T         %s             %s" T_err_tot T_err_tot/8
set graphdev= transfer_char
set ylin ylim 0 200
set xlin xlim 0 10
gr abs(i(vd)) .vs abs(vg)
set ylin ylim auto
set xlin xlim auto

print "S"
se 1
print "AT VG: 4.00E+00 DS ID: 3.77E+00 Model ID: %sA DELTA: %sA OOD: %sX" yvalue(abs(i(vd)),2.53E+00) abs(yvalue(abs(i(vd)),2.53E+00)-3.77E+00) (yvalue(abs(i(vd)),2.53E+00)/(3.77E+00))
print "AT VG: 4.00E+00 DS ID: 4.31E+00 Model ID: %sA DELTA: %sA OOD: %sX" yvalue(abs(i(vd)),3.32E+00) abs(yvalue(abs(i(vd)),3.32E+00)-4.31E+00) (yvalue(abs(i(vd)),3.32E+00)/(4.31E+00))
se 2
print "AT VG: 5.00E+00 DS ID: 7.76E+01 Model ID: %sA DELTA: %sA OOD: %sX" yvalue(abs(i(vd)),1.92E+00) abs(yvalue(abs(i(vd)),1.92E+00)-7.76E+01) (yvalue(abs(i(vd)),1.92E+00)/(7.76E+01))
print "AT VG: 5.00E+00 DS ID: 8.79E+01 Model ID: %sA DELTA: %sA OOD: %sX" yvalue(abs(i(vd)),2.59E+00) abs(yvalue(abs(i(vd)),2.59E+00)-8.79E+01) (yvalue(abs(i(vd)),2.59E+00)/(8.79E+01))
#S_perror2=abs((yvalue(abs(i(vd)),1.67E+00)-2.50E+00)/2.50E+00)
#print "Error: %s%%" S_perror2
#S_err_tot=abs(yvalue(abs(i(vd)),1.17E+00)-9.26E-01)+abs(yvalue(abs(i(vd)),1.67E+00)-2.50E+00)

print "L"
printf "*******Plotting the output characteristics of FET in Linear Region******* \n" >> out.txt
se 1
print "AT VG: 4.00E+00 DS ID: 2.70E+00 Model ID: %sA DELTA: %sA OOD: %sX" yvalue(abs(i(vd)),4.72E-01) abs(yvalue(abs(i(vd)),4.72E-01)-2.70E+00) (yvalue(abs(i(vd)),4.72E-01)/(2.70E+00))
se 2
print "AT VG: 5.00E+00 DS ID: 4.91E+01 Model ID: %sA DELTA: %sA OOD: %sX" yvalue(abs(i(vd)),5.60E-01) abs(yvalue(abs(i(vd)),5.60E-01)-4.91E+01) (yvalue(abs(i(vd)),5.60E-01)/(4.91E+01))
se 3
print "AT VG: 6.00E+00 DS ID: 9.85E+01 Model ID: %sA DELTA: %sA OOD: %sX" yvalue(abs(i(vd)),3.75E-01) abs(yvalue(abs(i(vd)),3.75E-01)-9.85E+01) (yvalue(abs(i(vd)),3.75E-01)/(9.85E+01))
se 4
print "AT VG: 7.00E+00 DS ID: 1.20E+02 Model ID: %sA DELTA: %sA OOD: %sX" yvalue(abs(i(vd)),3.43E-01) abs(yvalue(abs(i(vd)),3.43E-01)-1.20E+02) (yvalue(abs(i(vd)),3.43E-01)/(1.20E+02))
#L_perror2=abs((yvalue(abs(i(vd)),8.01E-01)-2.09E+00)/2.09E+00)
#print "Error: %s%%" L_perror2
#L_err_tot=abs(yvalue(abs(i(vd)),4.04E-01)-7.06E-01)+abs(yvalue(abs(i(vd)),8.01E-01)-2.09E+00)

#print "Overall deltas:"
#print " ID        Total             Average"
#print " T         %s             %s" T_err_tot T_err_tot/8
#print " S         %s             %s" S_err_tot S_err_tot/2
#print " L         %s             %s" L_err_tot L_err_tot/2
#print " Combined: %s" T_err_tot+S_err_tot+L_err_tot


#set graphdev= output_char
#se 1 2 3 4 5 6 7 
#set ylin ylim 0 200
#set xlin xlim 0 5
#gr abs(i(vd)) .vs abs(vd)
#set ylin ylim auto
#set xlin xlim auto
#
#print "D"
#se 9
#set graphdev= diode_char
#set ylog ylim 0.01 100
#set xlin xlim 0 1.2
#gr abs(i(xm1.d1)) .vs vin
#set ylog ylim auto
#set xlin xlim auto
#
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
