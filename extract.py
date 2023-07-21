import fileinput

def extractLVDS(data):
    # dict of output data
    lvds = {"Output DOUTP": 0,
            "Output DOUTN": 0,
            "Output delta": 0,
            "Output com": 0}
    
    for line in data:
        for key in lvds.keys():
            if key in line:
                val = line.split()[3]
                # try except to handle the case where value has units
                try:
                    lvds[key] = float(val)
                except ValueError:
                    if 'm' in val: lvds[key] = convertFromMilli(float(val[:-1]))
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
    editJson("logs.json", 10)