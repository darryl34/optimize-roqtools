import fileinput
import os
import subprocess

# ---- Constants ---- #
# number of decimal places to round to
DECIMALS = 3

# ---- LVDS ---- #
def extractLVDS(data):
    # dict of output data
    lvds = {"Output DOUTP": 0,
            "Output DOUTN": 0,
            "Output delta": 0}
    
    for line in data:
        for key in lvds.keys():
            if key in line:
                lvds[key] = getVal(line.split()[3])
    return lvds


def editLVDSNetlist(filename, MPD1_W=None, MND1_W=None, 
                    P_KP=None, P_RD=None, P_RS=None, 
                    N_KP=None, N_RD=None, N_RS=None, rounded=False):
    for line in fileinput.input(files=filename, inplace=True):
        if MPD1_W and "MPD1" in line and '*' not in line:
            if rounded: MPD1_W = round(MPD1_W, DECIMALS)
            line = line.replace(line.split()[-1], "W=" + str(MPD1_W))
        elif MND1_W and "MND1" in line and '*' not in line:
            if rounded: MND1_W = round(MND1_W, DECIMALS)
            line = line.replace(line.split()[-1], "W=" + str(MND1_W))
        elif ".model PMOD_OUT" in line:
            if P_KP:
                if rounded: P_KP = round(P_KP, DECIMALS)
                line = line.replace(line.split()[5], "KP=" + str(P_KP))
            if P_RD:
                if rounded: P_RD = round(P_RD, DECIMALS)
                line = line.replace(line.split()[6], "RD=" + str(P_RD))
            if P_RS:
                if rounded: P_RS = round(P_RS, DECIMALS)
                line = line.replace(line.split()[7], "RS=" + str(P_RS))
        elif ".model NMOD_OUT" in line:
            if N_KP:
                if rounded: N_KP = round(N_KP, DECIMALS)
                line = line.replace(line.split()[5], "KP=" + str(N_KP))
            if N_RD:
                if rounded: N_RD = round(N_RD, DECIMALS)
                line = line.replace(line.split()[6], "RD=" + str(N_RD))
            if N_RS:
                if rounded: N_RS = round(N_RS, DECIMALS)
                line = line.replace(line.split()[7], "RS=" + str(N_RS))
        print(line, end="")


# ---- ECL ---- #
def extractECL(data):
    ecl = {"Output VOH": 0,
            "Output VOL": 0,
            "Output Delta": 0,
            "Analog Supply Current IAVDD": 0}
    
    for line in data:
        for key in ecl.keys():
            if key in line:
                if key == "Analog Supply Current IAVDD":
                    ecl[key] = getVal(line.split()[-1])
                else:
                    ecl[key] = getVal(line.split()[3])
    return ecl

def editECLNetlist(filename, RB1=None, RB2=None, rounded=False):
    for line in fileinput.input(files=filename, inplace=True):
        if RB1 and "RB1 %vcc" in line:
            if rounded: RB1 = round(RB1, DECIMALS)
            line = line.replace(line.split()[-1], str(RB1))
        elif RB2 and "RB2 %vcc" in line:
            if rounded: RB2 = round(RB2, DECIMALS)
            line = line.replace(line.split()[-1], str(RB2))
        print(line, end="")


# ---- CML ---- #
def extractCML(data):
    cml = {"Output VOH": 0,
            "Output VOL": 0,
            "Output Delta": 0,
            "IVCC": 0}
    
    for line in data:
        for key in cml.keys():
            if key in line:
                if key == "IVCC":
                    cml[key] = getVal(line.split()[-1])
                else:
                    cml[key] = getVal(line.split()[3])
    return cml

def editCMLNetlist(filename, R1=None, R2=None, R3=None, R4=None, rounded=False):
    for line in fileinput.input(files=filename, inplace=True):
        if R1 and "R1" in line and '*' not in line:
            if rounded: R1 = round(R1, DECIMALS)
            line = line.replace(line.split()[-1], str(R1))
        elif R2 and "R2" in line and '*' not in line:
            if rounded: R2 = round(R2, DECIMALS)
            line = line.replace(line.split()[-1], str(R2))
        elif R3 and "R3" in line and '*' not in line:
            if rounded: R3 = round(R3, DECIMALS)
            line = line.replace(line.split()[-1], str(R3))
        elif R4 and "R4" in line and '*' not in line:
            if rounded: R4 = round(R4, DECIMALS)
            line = line.replace(line.split()[-1], str(R4))
        # elif ".model QMOD_OUT" in line:
        #     if BF:
        #         line = line.replace(line.split()[3], "BF=" + str(BF))
        #     if RC:
        #         line = line.replace(line.split()[4], "RC=" + str(RC))
        #     if RE:
        #         line = line.replace(line.split()[5], "RE=" + str(RE))
        #     if RB:
        #         line = line.replace(line.split()[6], "RB=" + str(RB))
        print(line, end="")


# ---- MOSFET ---- #
def extractMOSCmd(data):
    t = []
    s = []
    l = []

    for line in data:
        if line and len(line) > 1:
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

def editMOSNetlist(filename, VTO=None, KP=None, LAMBDA=None, RS=None, RD=None, rounded=False):
    with fileinput.input(files=filename, inplace=True) as f:
        for line in f:
            if "LAMBDA" in line:
                if VTO:
                    if rounded: VTO = round(VTO, DECIMALS)
                    line = line.replace(line.split()[4], "VTO=" + str(VTO))
                if KP:
                    if rounded: KP = round(KP, DECIMALS)
                    line = line.replace(line.split()[5], "KP=" + str(KP))
                if LAMBDA:
                    if rounded: LAMBDA = round(LAMBDA, DECIMALS)
                    line = line.replace(line.split()[6], "LAMBDA=" + str(LAMBDA))
            if "CGSO" in line:
                if RS:
                    if rounded: RS = round(RS, DECIMALS)
                    line = line.replace(line.split()[1], "RS=" + str(RS))
                if RD:
                    if rounded: RD = round(RD, DECIMALS)
                    line = line.replace(line.split()[2], "RD=" + str(RD))
            print(line, end="")


def runCmd():
    if os.name == 'nt':
        return subprocess.run(["C:/KD/cygwin-roq/bin/bash.exe", "-i", "-c", "/cygdrive/c/espy/roq/bin/hpspice.exe -s -f -c '. core.cmd'"], capture_output=True, text=True).stdout
    else:
        return subprocess.run(["/mnt/c/KD/cygwin-roq/bin/bash.exe", "-i", "-c", "/cygdrive/c/espy/roq/bin/hpspice.exe -s -f -c '. core.cmd'"], capture_output=True, text=True).stdout


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
        if 'meg' in val: return float(val[:-3]) * 1e6
        elif 'm' in val: return float(val[:-1]) * 1e-3
        elif 'u' in val: return float(val[:-1]) * 1e-6
        elif 'n' in val: return float(val[:-1]) * 1e-9
        elif 'p' in val: return float(val[:-1]) * 1e-12
        elif 'k' in val: return float(val[:-1]) * 1e3
        else: return 0


def penaltyFunc(x, target, scale=-10):
    return scale*(x - target)**2

if __name__ == "__main__":
    pass