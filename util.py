import fileinput

# ---- LVDS ---- #
def extractLVDS(data):
    # dict of output data
    lvds = {"Output DOUTP": 0,
            "Output DOUTN": 0,
            "Output delta": 0,
            "Output com": 0}
    
    for line in data:
        for key in lvds.keys():
            if key in line:
                lvds[key] = getVal(line.split()[3])
    return lvds


def editLVDSNetlist(filename, MPD1_W=None, MND1_W=None, KP=None, RD=None, RS=None):
    for line in fileinput.input(files=filename, inplace=True, encoding="utf-8"):
        if MPD1_W and "MPD1" in line:
            line = line.replace(line.split()[-1], "W=" + str(MPD1_W))
        elif MND1_W and "MND1" in line:
            line = line.replace(line.split()[-1], "W=" + str(MND1_W))
        elif ".model PMOD_OUT" in line:
            if KP:
                line = line.replace(line.split()[5], "KP=" + str(KP))
            if RD:
                line = line.replace(line.split()[6], "RD=" + str(RD))
            if RS:
                line = line.replace(line.split()[7], "RS=" + str(RS))
        print(line, end="")


# ---- ECL ---- #
def extractECL(data):
    ecl = {"Output VOH": 0,
            "Output VOL": 0,
            "Output Delta": 0,
            "Output VCM": 0,
            "Analog Supply Current IAVDD": 0}
    
    for line in data:
        for key in ecl.keys():
            if key in line:
                if key == "Analog Supply Current IAVDD":
                    ecl[key] = getVal(line.split()[-1])
                else:
                    ecl[key] = getVal(line.split()[3])
    return ecl

def editECLNetlist(filename, RB1=None, RB2=None, MB1_W=None, MB2_W=None):
    for line in fileinput.input(files=filename, inplace=True, encoding="utf-8"):
        if RB1 and "RB1 %vcc" in line:
            line = line.replace(line.split()[-1], str(RB1))
        elif RB2 and "RB2 %vcc" in line:
            line = line.replace(line.split()[-1], str(RB2))
        elif MB1_W and "MB1 %b1" in line:
            line = line.replace(line.split()[-1], "W=" + str(MB1_W))
        elif MB2_W and "MB2 %b2" in line:
            line = line.replace(line.split()[-1], "W=" + str(MB2_W))
        print(line, end="")


# ---- CML ---- #
def extractCML(data):
    cml = {"Output VOH": 0,
            "Output VOL": 0,
            "Output Delta": 0,
            "Output VCM": 0,
            "IVCC": 0}
    
    for line in data:
        for key in cml.keys():
            if key in line:
                if key == "IVCC":
                    cml[key] = getVal(line.split()[-1])
                else:
                    cml[key] = getVal(line.split()[3])
    return cml

def editCMLNetlist(filename, R1=None, R2=None, R3=None, R4=None, BF=None, RC=None, RE=None, RB=None, MCA_W=None):
    for line in fileinput.input(files=filename, inplace=True, encoding="utf-8"):
        if R1 and "R1" in line:
            line = line.replace(line.split()[-1], str(R1))
        elif R2 and "R2" in line:
            line = line.replace(line.split()[-1], str(R2))
        elif R3 and "R3" in line:
            line = line.replace(line.split()[-1], str(R3))
        elif R4 and "R4" in line:
            line = line.replace(line.split()[-1], str(R4))
        elif ".model QMOD_OUT" in line:
            if BF:
                line = line.replace(line.split()[3], "BF=" + str(BF))
            if RC:
                line = line.replace(line.split()[4], "RC=" + str(RC))
            if RE:
                line = line.replace(line.split()[5], "RE=" + str(RE))
            if RB:
                line = line.replace(line.split()[6], "RB=" + str(RB))
        elif MCA_W and "MCA %e" in line:
            line = line.replace(line.split()[-1], "W=" + str(MCA_W))
        print(line, end="")
        

# ---- MOSFET ---- #
def extractMosText(filename):
    with open(filename, "r") as f:
        data = f.read()
    '''Takes in a text file and returns a dictionary of MOSFET data points'''
    mos_data = {"T": [],
                "S": [],
                "L": []}
    split = list(splitList(data.splitlines(), ["T", "S", "L"]))
    mos_data["T"] = [i.split() for i in split[0]]
    mos_data["S"] = [i.split() for i in split[1]]
    mos_data["L"] = [i.split() for i in split[2]]
    return mos_data

def genMosCmd(filename, mos_data, isSignPositive):
    data = []
    data.append("set clobber\nset nomarks\nsi harness\n\n")

    # Transfer characteristics
    data.append('se 8\nprint "******** Printing and Plotting the Transfer characteristics of FET********"\n')
    for i in range(len(mos_data["T"])):
        VGS = str(mos_data["T"][i][0])
        ID = str(mos_data["T"][i][1])
        string = 'print "T DS VG: ' + VGS
        string += ' Model VG: %s V  @ ID: ' + ID
        string += ' Delta: %s" abs(xcross(abs(i(vd)),'+ID+')) abs(abs(xcross(abs(i(vd)),'+ID+'))'+'-'+VGS+')' 
        data.append(string + '\n')

    # Saturation Output characteristics
    data.append('\nprint "*******Plotting the output characteristics of FET in Saturation Region*******"\n')
    for i in range(len(mos_data["S"])):
        VDS = str(mos_data["S"][i][0])
        ID = str(mos_data["S"][i][1])
        VGS = str(mos_data["S"][i][2])
        se = 'se ' + str(int(float(VGS))-3)
        if isSignPositive: '-' + VDS
        string = se + '\nprint "S AT VG: ' + VGS
        string += ' DS ID: ' + ID
        string += ' Model ID: %sA DELTA: %sA OOD: %sX" yvalue(abs(i(vd)),'+VDS+') abs(yvalue(abs(i(vd)),'+VDS+')'+'-'+ID+') (yvalue(abs(i(vd)),'+VDS+')/('+ID+'))'
        data.append(string + '\n')
    
    # Linear Output characteristics
    data.append('\nprint "*******Plotting the output characteristics of FET in Linear Region*******"\n')
    for i in range(len(mos_data["L"])):
        VGS = str(mos_data["L"][i][0])
        VDS = str(mos_data["L"][i][1])
        ID = str(mos_data["L"][i][2])
        if isSignPositive: '-' + VDS
        se = 'se ' + str(int(float(VGS))-3)
        string = se + '\nprint "L AT VG: ' + VGS
        string += ' DS ID: ' + ID
        string += ' Model ID: %sA DELTA: %sA OOD: %sX" yvalue(abs(i(vd)),'+VDS+') abs(yvalue(abs(i(vd)),'+VDS+')'+'-'+ID+') (yvalue(abs(i(vd)),'+VDS+')/('+ID+'))'
        data.append(string + '\n')

    with open(filename, "w") as f:
        f.writelines(data)

def extractMOSCmd(data):
    t = []
    s = []
    l = []

    for line in data:
        if line:
            if "T" == line[0]:
                lst = line.split()
                # Model VG, Delta
                t.append([getVal(lst[6]), getVal(lst[-1])])
            elif "S" == line[0]:
                lst = line.split()
                # Model ID, Delta, OOD
                s.append([getVal(lst[9][:-1]), getVal(lst[11][:-1]), getVal(lst[-1][:-1])])
            elif "L" == line[0]:
                lst = line.split()
                # Model ID, Delta, OOD
                l.append([getVal(lst[9][:-1]), getVal(lst[11][:-1]), getVal(lst[-1][:-1])])
    
    return {"T": t, "S": s, "L": l}

def editMOSNetlist(filename, VTO=None, KP=None, LAMBDA=None, RS=None, RD=None):
    with fileinput.input(files=filename, inplace=True, encoding="utf-8") as f:
        for line in f:
            if "LAMBDA" in line:
                if VTO:
                    line = line.replace(line.split()[4], "VTO=" + str(VTO))
                if KP:
                    line = line.replace(line.split()[5], "KP=" + str(KP))
                if LAMBDA:
                    line = line.replace(line.split()[6], "LAMBDA=" + str(LAMBDA))
            if "CGSO" in line:
                if RS:
                    line = line.replace(line.split()[1], "RS=" + str(RS))
                if RD:
                    line = line.replace(line.split()[2], "RD=" + str(RD))
            print(line, end="")


# ---- Helper functions ---- #
def splitList(lst, sep):
    chunk = []
    for val in lst:
        if val:
            if val in sep:
                if chunk: yield chunk
                chunk = []
            else:
                chunk.append(val)
    if chunk:
        yield chunk


def getVal(val):
    # handle the case where value has units
    try:
        return float(val)
    except ValueError:
        if 'm' in val: return float(val[:-1]) * 1e-3
        elif 'u' in val: return float(val[:-1]) * 1e-6
        elif 'n' in val: return float(val[:-1]) * 1e-9
        elif 'p' in val: return float(val[:-1]) * 1e-12
        elif 'k' in val: return float(val[:-1]) * 1e3
        else: return 0


def editJson(filename, scale):
    for line in fileinput.input(files=filename, inplace=True):
        target = float(line.split()[1][:-1])
        line = line.replace(line.split()[1][:-1], str(target * scale)) 
        print(line, end="")

if __name__ == "__main__":
    genMosCmd("test.cmd", extractMosText("1855-3098/mos_data.txt"), True)
    # with open("1855-3098/test.txt", "r") as f:
    #     data = f.read().splitlines()[1:]
    # extractMOSCmd(data)
    # editMOSNetlist("1855-3098/1855-3098.inc", VTO=0.5, KP=0.0001, LAMBDA=0.01, RS=0.1, RD=0.1)