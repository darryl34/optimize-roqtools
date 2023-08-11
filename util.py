import fileinput
import os
import subprocess

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
                    N_KP=None, N_RD=None, N_RS=None):
    for line in fileinput.input(files=filename, inplace=True):
        if MPD1_W and "MPD1" in line and '*' not in line:
            line = line.replace(line.split()[-1], "W=" + str(MPD1_W))
        elif MND1_W and "MND1" in line and '*' not in line:
            line = line.replace(line.split()[-1], "W=" + str(MND1_W))
        elif ".model PMOD_OUT" in line:
            if P_KP:
                line = line.replace(line.split()[5], "KP=" + str(P_KP))
            if P_RD:
                line = line.replace(line.split()[6], "RD=" + str(P_RD))
            if P_RS:
                line = line.replace(line.split()[7], "RS=" + str(P_RS))
        elif ".model NMOD_OUT" in line:
            if N_KP:
                line = line.replace(line.split()[5], "KP=" + str(N_KP))
            if N_RD:
                line = line.replace(line.split()[6], "RD=" + str(N_RD))
            if N_RS:
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

def editECLNetlist(filename, RB1=None, RB2=None):
    for line in fileinput.input(files=filename, inplace=True):
        if RB1 and "RB1 %vcc" in line:
            line = line.replace(line.split()[-1], str(RB1))
        elif RB2 and "RB2 %vcc" in line:
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

def editCMLNetlist(filename, R1=None, R2=None, R3=None, R4=None, BF=None, RC=None, RE=None, RB=None):
    for line in fileinput.input(files=filename, inplace=True):
        if R1 and "R1" in line and '*' not in line:
            line = line.replace(line.split()[-1], str(R1))
        elif R2 and "R2" in line and '*' not in line:
            line = line.replace(line.split()[-1], str(R2))
        elif R3 and "R3" in line and '*' not in line:
            line = line.replace(line.split()[-1], str(R3))
        elif R4 and "R4" in line and '*' not in line:
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