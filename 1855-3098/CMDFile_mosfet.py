print("Mos=?")
sign=input()
# Number of points in Transfer characteristics
N_tc = 6
# Number of points in output characteristics of FET in Saturation Region
N_otc_sat = 2
# Number of points in output characteristics of FET in Linear Region
N_otc_lin = 4

if sign=='n' or sign=='N':
    s=''
elif sign=='p' or sign=='P':
    s='-'

rf = open("1855-3098/mos_data.txt", "r")
rf.read(2)    
Comm00= 'printf "******** Printing and Plotting the Transfer characteristics of FET******** \\n" >> out.txt'
print(Comm00)
for x in range(0,N_tc):
    VGS=rf.read(8).strip()
    rf.read(1)
    ID=rf.read(8).strip()
    rf.read(1)
    statA='print "DS VG: '+VGS+' Model VG: %s V  @ ID:'+ ID +' Delta: %s" abs(xcross(abs(i(vd)),'+ID+')) abs(abs(xcross(abs(i(vd)),'+ID+'))'+'-'+VGS+')'
    print(statA)

print('')
rf.read(3)
Comm01='printf "*******Plotting the output characteristics of FET in Saturation Region******* \\n" >> out.txt'
print(Comm01)
for x in range(0,N_otc_sat):
    VDS=rf.read(8).strip()
    rf.read(1)
    ID=rf.read(8).strip()
    rf.read(1)
    VGS=rf.read(8).strip()
    rf.read(1)
    se="se "+str(x+1)
    print(se)
    statA='print "AT VG: '+VGS+' DS ID: '+ID+' Model ID: %sA DELTA: %sA OOD: %sX" yvalue(abs(i(vd)),'+s+VDS+') abs(yvalue(abs(i(vd)),'+s+VDS+')'+'-'+ID+") (yvalue(abs(i(vd)),"+s+VDS+')/('+ID+'))'
    print(statA)

print('')
rf.read(3)
Comm02='printf "*******Plotting the output characteristics of FET in Linear Region******* \\n" >> out.txt'
print(Comm02)
for x in range(0,N_otc_lin):
    VGS=rf.read(8).strip()
    rf.read(1)
    VDS=rf.read(8).strip()
    rf.read(1)
    ID=rf.read(8).strip()
    rf.read(1)
    se="se "+str(x+1)
    print(se)
    statA='print "AT VG: '+VGS+' DS ID: '+ID+' Model ID: %sA DELTA: %sA OOD: %sX" yvalue(abs(i(vd)),'+s+VDS+') abs(yvalue(abs(i(vd)),'+s+VDS+')'+'-'+ID+") (yvalue(abs(i(vd)),"+s+VDS+')/('+ID+'))'
    print(statA)
rf.close()
