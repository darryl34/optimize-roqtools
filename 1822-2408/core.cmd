si fixture

##ECL
##------PRINTING NODE VOLTAGES-----------------
#print " Supply DVDD : %s" yvalue(vcc,15u)
#print " Supply DGND : %s" yvalue(gnd_1,15u)
#print ""
#print " Output Q : %s (2.32V)" yvalue(v(Q),15u)
#print " Output QN : %s (1.5V)" yvalue(v(NOTQ),15u)
#print ""
##------PRINTING BRANCH CURRENTS---------------
#print " Analog Supply Current IAVDD : %s" yvalue(abs(i(vvcc)),15u)
#print " Analog Supply Current IAGND : %s" yvalue(abs(i(vgnd_1)),15u)
#print "***********************************************************"
##print " BUS Supply Current IDGND"
###print "***********************************************************"
###gr abs(i(vvcc)) ; abs(v(Q)) ; abs(v(NOTQ))
###print "***********************************************************"


#LVDS
#------PRINTING NODE VOLTAGES-----------------
print " Supply DVDD : %s" yvalue(vcc,15u)
print " Supply DGND : %s" yvalue(gnd,15u)
print ""
print " Output DOUTP : %s (1.41V)" yvalue(v(out3),15u)
print " Output DOUTN : %s (1.05V)" yvalue(v(not_out3),15u)
print " Output delta : %s (360mV)" yvalue(v(out3),15u)-yvalue(v(not_out3),15u)
print " Output com : %s (1.23V)" (yvalue(v(out3),15u)+yvalue(v(not_out3),15u))/2
print ""
#------PRINTING BRANCH CURRENTS---------------
print " Digital Supply Current IDVDD : %s" yvalue(abs(i(vvcc)),15u)
print " Digital Supply Current IDGND : %s" yvalue(abs(i(vgnd)),15u)