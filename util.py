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
    mos_data["T"] = str2floats(split[0])
    mos_data["S"] = str2floats(split[1])
    mos_data["L"] = str2floats(split[2])
    return mos_data


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

def str2floats(lst):
    return [list(map(float, i.split())) for i in lst]

def getVal(val):
    # handle the case where value has units
    try:
        return float(val)
    except ValueError:
        if 'm' in val: return float(val[:-1]) / 1000
        elif 'u' in val: return float(val[:-1]) / 1000000
        else: return 0


def editJson(filename, scale):
    for line in fileinput.input(files=filename, inplace=True):
        target = float(line.split()[1][:-1])
        line = line.replace(line.split()[1][:-1], str(target * scale)) 
        print(line, end="")

if __name__ == "__main__":
    print(extractMosText("1855-3098/mos_data.txt"))
    # editCMLNetlist("1822-6817/1822-6817.inc", R1=1000, R2=1000, R3=1000, R4=1000, BF=10, RC=1000, RE=1000, RB=1000, MCA_W=1e-4)
