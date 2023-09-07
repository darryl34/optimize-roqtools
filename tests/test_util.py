from util import *
import os

'''
Functions to test the util.py module
'''

def test_extractLVDS():
    data = ["Output DOUTP : 1.2", "Output DOUTN : 0.8", "Output delta : 400m"]
    lvdsDict = extractLVDS(data)
    assert lvdsDict["Output DOUTP"] == 1.2
    assert lvdsDict["Output DOUTN"] == 0.8
    assert lvdsDict["Output delta"] == 0.4

def test_editLVDSNetlist():
    # Generate test file
    filename = "testLVDS.txt"
    with open(filename, "w") as f:
        f.write("MPD1 W=1\nMND1 W=1\n.model PMOD_OUT UCBMOS PMOS VTO=-0.7 KP=30u RD=200.5 RS=200.5\n.model NMOD_OUT UCBMOS NMOS VTO=0.7 KP=30u RD=200.5 RS=200.5\n")
    
    # Edit test file
    editLVDSNetlist(filename, MPD1_W=0.5, MND1_W=0.5, P_KP=0.0001, N_KP=0.0001, P_RD=1000, N_RD=1000, P_RS=1000, N_RS=1000)
    
    # Check if test file was edited correctly
    with open(filename, "r") as f:
        data = f.read()
        assert "MPD1 W=0.5" in data
        assert "MND1 W=0.5" in data
        assert "KP=0.0001" in data
        assert "RD=1000" in data
        assert "RS=1000" in data

    # Delete test file
    os.remove(filename)

def test_extractECL():
    data = ["Output VOH : 1.2", "Output VOL : 0.8", "Output Delta : 0.4", "Analog Supply Current IAVDD : 0.6"]
    eclDict = extractECL(data)
    assert eclDict["Output VOH"] == 1.2
    assert eclDict["Output VOL"] == 0.8
    assert eclDict["Output Delta"] == 0.4
    assert eclDict["Analog Supply Current IAVDD"] == 0.6

def test_editECLNetlist():
    # Generate test file
    filename = "testECL.txt"
    with open(filename, "w") as f:
        f.write("RB1 %vcc 100\nRB2 %vcc 100\n")

    # Edit test file
    editECLNetlist(filename, RB1=200, RB2=200)

    # Check if test file was edited correctly
    with open(filename, "r") as f:
        data = f.read()
        assert "RB1 %vcc 200" in data
        assert "RB2 %vcc 200" in data

    # Delete test file
    os.remove(filename)

def test_extractCML():
    data = ["Output VOH : 1.2", "Output VOL : 0.8", "Output Delta : 0.4", "Analog Supply Current () IVCC : 0.6"]
    cmlDict = extractCML(data)
    assert cmlDict["Output VOH"] == 1.2
    assert cmlDict["Output VOL"] == 0.8
    assert cmlDict["Output Delta"] == 0.4
    assert cmlDict["IVCC"] == 0.6

def test_editCMLNetlist():
    # Generate test file
    filename = "testCML.txt"
    with open(filename, "w") as f:
        data = "R1 %vcc %b1 100\nR2 %b1 %gnd 100\nR3 %vcc %b2 1000\nR4 %b2 %gnd 1000\n"
        f.write(data)

    # Edit test file
    editCMLNetlist(filename, R1=200, R2=200, R3=200, R4=200)

    # Check if test file was edited correctly
    with open(filename, "r") as f:
        data = f.read()
        assert "R1 %vcc %b1 200" in data
        assert "R2 %b1 %gnd 200" in data
        assert "R3 %vcc %b2 200" in data
        assert "R4 %b2 %gnd 200" in data

    # Delete test file
    os.remove(filename)

def test_splitList():
    lst = [1, 2, "A", 3, 4, "B", 5, "C", 6]
    assert list(splitList(lst, ["A"])) == [[1, 2], [3, 4, "B", 5, "C", 6]]
    assert list(splitList(lst, ["B"])) == [[1, 2, "A", 3, 4], [5, "C", 6]]
    assert list(splitList(lst, ["C"])) == [[1, 2, "A", 3, 4, "B", 5], [6]]
    assert list(splitList(lst, ["A", "B"])) == [[1, 2], [3, 4], [5, "C", 6]]
    assert list(splitList(lst, ["B", "C"])) == [[1, 2, "A", 3, 4], [5], [6]]
    assert list(splitList(lst, ["A", "B", "C"])) == [[1, 2], [3, 4], [5], [6]]

def test_splitList2():
    lst = ["T", "1 2", "2 3", "S", "3 4", "4 5"]
    assert list(splitList(lst, ["T"])) == [["1 2", "2 3", "S", "3 4", "4 5"]]
    assert list(splitList(lst, ["T", "S"])) == [["1 2", "2 3"], ["3 4", "4 5"]]

def test_splitList3():
    # Test for empty list
    lst = ["A"]
    assert list(splitList(lst, ["A"])) == []


def test_getVal():
    assert getVal("1.2") == 1.2
    assert getVal("1.2m") == 1.2e-3
    assert getVal("1.2u") == 1.2e-6
    assert getVal("1.2n") == 1.2e-9
    assert getVal("1.2p") == 1.2e-12
    assert getVal("1.2f") == 0
    assert getVal("1.2k") == 1.2e3
