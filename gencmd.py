import re
import fileinput

from util import splitList, getVal

def generate(filename, mos_data, isSignPos):
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
        if isSignPos: '-' + VDS
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
        if isSignPos: '-' + VDS
        se = 'se ' + str(int(float(VGS))-3)
        string = se + '\nprint "L AT VG: ' + VGS
        string += ' DS ID: ' + ID
        string += ' Model ID: %sA DELTA: %sA OOD: %sX" yvalue(abs(i(vd)),'+VDS+') abs(yvalue(abs(i(vd)),'+VDS+')'+'-'+ID+') (yvalue(abs(i(vd)),'+VDS+')/('+ID+'))'
        data.append(string + '\n')

    with open(filename, "w") as f:
        f.writelines(data)


def extractHarnessFile(filename):
    """
    Extracts relevant data from a given file containing test cases for a circuit.

    Args:
    - filename: a string representing the name of the file to be processed.

    Returns:
    - test_data: a dictionary containing the extracted data from the file, including the test case numbers for 'MOSFET' and 'diode', and a list of voltage values and their corresponding test case numbers.
    """


    with open(filename, "r") as f:
        data = f.read()
    
    caseBlocks = re.split(r'\bcase\(\d+\)', data)[1:]
    
    test_data = {"voltages": []}

    for i, case in enumerate(caseBlocks, start=1):
        if "MOSFET" in case:
            test_data["MOSFET"] = i
        elif "diode" in case:
            test_data["diode"] = i
        else:
            match = re.search(r'vg .* (\d+(?:\.\d*)?)', case)
            if match:
                test_data["voltages"].append([float(match.group(1)), i])
    
    return test_data


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

def editMOSNetlist(filename, VTO=None, KP=None, LAMBDA=None, RS=None, RD=None):
    with fileinput.input(files=filename, inplace=True) as f:
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


if __name__ == "__main__":
    extractHarnessFile("harness.cki")