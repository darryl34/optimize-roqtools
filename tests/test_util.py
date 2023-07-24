from util import *
import os

'''
Functions to test the util.py module
'''

def test_extractLVDS():
    data = ["Output DOUTP : 1.2", "Output DOUTN : 0.8", "Output delta : 0.4", "Output com : 0.5"]
    lvdsDict = extractLVDS(data)
    assert lvdsDict["Output DOUTP"] == 1.2
    assert lvdsDict["Output DOUTN"] == 0.8
    assert lvdsDict["Output delta"] == 0.4
    assert lvdsDict["Output com"] == 0.5

def test_editLVDSNetlist():
    # Generate test file
    filename = "testLVDS.txt"
    with open(filename, "w") as f:
        f.write("MPD1 W=1\nMND1 W=1\n.model PMOD_OUT UCBMOS PMOS VTO=-0.7 KP=30u RD=200.5 RS=200.5\n")
    
    # Edit test file
    editLVDSNetlist(filename, MPD1_W=0.5, MND1_W=0.5, KP=0.0001, RD=1000, RS=1000)
    
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
