si fixture
#------PRINTING NODE VOLTAGES-----------------
print " positive Supply Voltage VCC (3.3V) : %s" yvalue(VCC,15u)
print ""
print ""
print " Output VOH : %s (3.5V)" yvalue(v(QA0),15u)
print " Output VOL : %s (2.7V)" yvalue(v(NOTQA0),15u)
print " Output Delta : %s (800mV)" abs(yvalue(v(QA0),15u)-yvalue(v(NOTQA0),15u))
print " Output VCM : %s (3.1V)" (yvalue(v(QA0),15u)+yvalue(v(NOTQA0),15u))/2

#------PRINTING BRANCH CURRENTS---------------
print ""
print " Analog Supply Current () IVCC : %s" yvalue(abs(i(VCC)),15u)
print " Analog Supply Current () IVEE : %s" yvalue(abs(i(VEE)),15u)
print ""



