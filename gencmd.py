import re

def generate(filename, mos_data, isSignPos):
    data = []
    data.append("set clobber\nset nomarks\nsi harness\n\n")

    # Transfer characteristics


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





if __name__ == "__main__":
    extractHarnessFile("harness.cki")