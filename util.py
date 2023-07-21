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


def getVal(val):
    # handle the case where value has units
    try:
        return float(val)
    except ValueError:
        if 'm' in val: return convertFromMilli(float(val[:-1]))

def convertFromMilli(num):
    return num / 1000

def convertFromMu(num):
    return num / 1000000

def editJson(filename, scale):
    for line in fileinput.input(files=filename, inplace=True):
        target = float(line.split()[1][:-1])
        line = line.replace(line.split()[1][:-1], str(target * scale)) 
        print(line, end="")

if __name__ == "__main__":
    # editLVDSNetlist("1822-2408.inc", 1, 1, 0.5)
    # extractLVDS("test.txt")
    # editJson("logs.json", 10)
    # editECLNetlist("1822-2408/1822-2408.inc", 1, 1, 0.5, 0.5)
    with open("1822-2408/test.txt", "r") as f:
        data = f.read()
    print(extractECL(data))
