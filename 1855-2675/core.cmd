set clobber
set nomarks
si harness

se 7
print "******** Printing and Plotting the Transfer characteristics of FET********"
print "T DS VG: 3.88E+00 Model VG: %s V  @ ID: 4.07E-01 Delta: %s" abs(xcross(abs(i(vd)),4.07E-01)) abs(abs(xcross(abs(i(vd)),4.07E-01))-3.88E+00)
print "T DS VG: 4.10E+00 Model VG: %s V  @ ID: 1.25E+00 Delta: %s" abs(xcross(abs(i(vd)),1.25E+00)) abs(abs(xcross(abs(i(vd)),1.25E+00))-4.10E+00)
print "T DS VG: 4.35E+00 Model VG: %s V  @ ID: 3.86E+00 Delta: %s" abs(xcross(abs(i(vd)),3.86E+00)) abs(abs(xcross(abs(i(vd)),3.86E+00))-4.35E+00)
print "T DS VG: 4.74E+00 Model VG: %s V  @ ID: 1.43E+01 Delta: %s" abs(xcross(abs(i(vd)),1.43E+01)) abs(abs(xcross(abs(i(vd)),1.43E+01))-4.74E+00)
print "T DS VG: 5.35E+00 Model VG: %s V  @ ID: 4.22E+01 Delta: %s" abs(xcross(abs(i(vd)),4.22E+01)) abs(abs(xcross(abs(i(vd)),4.22E+01))-5.35E+00)
print "T DS VG: 6.13E+00 Model VG: %s V  @ ID: 7.88E+01 Delta: %s" abs(xcross(abs(i(vd)),7.88E+01)) abs(abs(xcross(abs(i(vd)),7.88E+01))-6.13E+00)
print "T DS VG: 7.12E+00 Model VG: %s V  @ ID: 1.16E+02 Delta: %s" abs(xcross(abs(i(vd)),1.16E+02)) abs(abs(xcross(abs(i(vd)),1.16E+02))-7.12E+00)

print "*******Plotting the output characteristics of FET in Saturation Region*******"
se 1
print "S AT VG: 4.50E+00 DS ID: 4.01E+00 Model ID: %sA DELTA: %sA OOD: %sX" yvalue(abs(i(vd)),7.07E-01) abs(yvalue(abs(i(vd)),7.07E-01)-4.01E+00) (yvalue(abs(i(vd)),7.07E-01)/(4.01E+00))
se 2
print "S AT VG: 4.80E+00 DS ID: 9.54E+00 Model ID: %sA DELTA: %sA OOD: %sX" yvalue(abs(i(vd)),1.12E+00) abs(yvalue(abs(i(vd)),1.12E+00)-9.54E+00) (yvalue(abs(i(vd)),1.12E+00)/(9.54E+00))
se 3
print "S AT VG: 5.00E+00 DS ID: 1.51E+01 Model ID: %sA DELTA: %sA OOD: %sX" yvalue(abs(i(vd)),1.43E+00) abs(yvalue(abs(i(vd)),1.43E+00)-1.51E+01) (yvalue(abs(i(vd)),1.43E+00)/(1.51E+01))
se 4
print "S AT VG: 5.50E+00 DS ID: 3.63E+01 Model ID: %sA DELTA: %sA OOD: %sX" yvalue(abs(i(vd)),4.39E+00) abs(yvalue(abs(i(vd)),4.39E+00)-3.63E+01) (yvalue(abs(i(vd)),4.39E+00)/(3.63E+01))

print "*******Plotting the output characteristics of FET in Linear Region*******"
se 1
print "L AT VG: 4.50E+00 DS ID: 3.48E+00 Model ID: %sA DELTA: %sA OOD: %sX" yvalue(abs(i(vd)),3.22E-01) abs(yvalue(abs(i(vd)),3.22E-01)-3.48E+00) (yvalue(abs(i(vd)),3.22E-01)/(3.48E+00))
se 2
print "L AT VG: 4.80E+00 DS ID: 8.78E+00 Model ID: %sA DELTA: %sA OOD: %sX" yvalue(abs(i(vd)),5.92E-01) abs(yvalue(abs(i(vd)),5.92E-01)-8.78E+00) (yvalue(abs(i(vd)),5.92E-01)/(8.78E+00))
se 3
print "L AT VG: 5.00E+00 DS ID: 1.39E+01 Model ID: %sA DELTA: %sA OOD: %sX" yvalue(abs(i(vd)),7.31E-01) abs(yvalue(abs(i(vd)),7.31E-01)-1.39E+01) (yvalue(abs(i(vd)),7.31E-01)/(1.39E+01))
se 4
print "L AT VG: 5.50E+00 DS ID: 3.46E+01 Model ID: %sA DELTA: %sA OOD: %sX" yvalue(abs(i(vd)),2.00E+00) abs(yvalue(abs(i(vd)),2.00E+00)-3.46E+01) (yvalue(abs(i(vd)),2.00E+00)/(3.46E+01))
se 5
print "L AT VG: 6.00E+00 DS ID: 2.20E+01 Model ID: %sA DELTA: %sA OOD: %sX" yvalue(abs(i(vd)),3.71E-01) abs(yvalue(abs(i(vd)),3.71E-01)-2.20E+01) (yvalue(abs(i(vd)),3.71E-01)/(2.20E+01))
#se 12
#print "L AT VG: 1.50E+01 DS ID: 2.99E+01 Model ID: %sA DELTA: %sA OOD: %sX" yvalue(abs(i(vd)),3.09E-01) abs(yvalue(abs(i(vd)),3.09E-01)-2.99E+01) (yvalue(abs(i(vd)),3.09E-01)/(2.99E+01))
