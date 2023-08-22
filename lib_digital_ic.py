# *************************************************************************************
# Hpspice regulator model generator library
# Script version: 1.0
# Python version: Python 3.6.5
# Compatible OS: Windows 10
# Requirements: Hpspice, libdiode(v1.6)
# Developer (v1.0): Ramana (ramarang)
# Notes:
#     This is a library to generate regulator (fixed/adjustable) models for Hpspice.
# Version doc:
#  * First version
# *************************************************************************************
import os
import re

#import libdiode as ld

# Max number of pins in a group to be shorted (ignore groups with more pins)
MAX_PIN_COUNT = 50

# ---- LVDS MODEL FUNCTIONS ----
def main_gen_lvds_model(pin_list, inputType, pVCC, pGND, kpn):
    res = gen_lvds_model(kpn, pin_list, inputType, pVCC, pGND)
    res += gen_lvds_clamp_diode(pin_list, pVCC, pGND)
    res += ".ends\n"
    res += "*******************************************************************\n"
    res += "********************** SUB-CIRCUIT ********************************\n"
    res += "*******************************************************************\n\n"
    if inputType != "LVDS":
        res += gen_hsd_inp_subckt(kpn, inputType, pVCC, pGND)
    res += gen_lvds_subckt(kpn)
    return res

def gen_lvds_model(kpn, pin_list, inputType, pVCC, pGND):
    '''Function to generate LVDS model'''
    reg_model = ""

    # generate pin numbers separated by space
    call_pin_list = []
    for pin_index in range(len(pin_list)):
        call_pin_list.append(str(pin_index+1))
    
    reg_model += "* \n"
    reg_model += ".subckt '"+kpn+"' "+" ".join(call_pin_list)+"\n" 
    reg_model += get_lvds_model_configurations(kpn, pin_list, inputType, pVCC, pGND)
    reg_model += "* \n"

    # Generate 1 ohm resistor network for similar pins
    reg_model += short_similar_pins(pin_list, 1)
    reg_model += "*\n"
    return reg_model

def get_lvds_model_configurations(kpn, pin_list, inputType, pVCC, pGND):
    '''Function returns lvds model configuration'''
    gen_lvds_model_config = f"*\n* Model for {kpn} goes here\n"

    gen_lvds_model_config += "* RCSS placed to match supply current\n"
    gen_lvds_model_config += f"RCSS {pVCC} {pGND} 39.22\n*\n"
    
    inp, outp = gen_hsd_io_interfaces(kpn, pin_list, inputType, outputType="LVDS", pVCC=pVCC, pVEE=pGND)
    gen_lvds_model_config += inp + "*\n" + outp
    gen_lvds_model_config += "*\n"
    return gen_lvds_model_config

def gen_lvds_input_pins(pin_list):
    # Input pin setup 
    input_pin_p = []
    input_pin_n = []
    
    for pin in pin_list:
        if "in_neg" in pin[1].lower() or "not_in" in pin[1].lower():
            input_pin_n.append(pin[0])
        elif "in_pos" in pin[1].lower() or "in" in pin[1].lower() and not "_sel" in pin[1].lower():
            input_pin_p.append(pin[0])
    
    # Pull-up and Pull-down resistors on IN_SEL pin
    # Input capacitance
    
    # LVDS input stage
    # input terminators
    rTermination = ""
    if rTermination and len(input_pin_p) == len(input_pin_n):
        inText = "* Input terminations\n"
        for count in range(len(input_pin_p)):
            inText += f"RIN{count} {input_pin_p[count]} {input_pin_n[count]} {rTermination}\n"
        return inText
    else: 
        print("Either Input P pin count and Input N pin count are not the same OR no input for resistor termination value\n")
        return ""

def gen_lvds_output_pins(kpn, pin_list, pVCC, pVEE):
    # Output pin setup
    output_pin_p = []
    output_pin_n = []

    kpn = kpn.replace('-', '_') if '-' in kpn else kpn

    for pin in pin_list:
        if "not_out" in pin[1].lower() or "out_neg" in pin[1].lower():
            output_pin_n.append(pin[0])
        elif "out" in pin[1].lower() or "out_pos" in pin[1].lower():
            output_pin_p.append(pin[0])

    # LVDS output stage
    if len(output_pin_p) == len(output_pin_n):
        outText = "* Output stage\n"
        for count in range(len(output_pin_p)):
            outText += f"XO{count} {pVCC} {output_pin_p[count]} {output_pin_n[count]} {pVEE} lvds_out_{kpn}\n"
        return outText
    else: 
        raise Exception("Output P pin count and Output N pin count are not the same\n")


# Functions to generate LVDS clamp diode
# if no inputs, use default settings in template
def gen_lvds_clamp_diode(pin_list, pVCC, pGND):

    lvds_clamp_diode = "* clamp protection\n"

    # Extract input pins from pin_list
    input_pin_p = [pin[0] for pin in pin_list if "in_pos" in pin[1].lower() or "in" in pin[1].lower() and not "_sel" in pin[1].lower()]
    input_pin_n = [pin[0] for pin in pin_list if "in_neg" in pin[1].lower() or "not_in" in pin[1].lower()]
    
    if input_pin_p:
        for count, pin in enumerate(input_pin_p, start=1):
            lvds_clamp_diode += f"DEPP{count} {pin} {pVCC} DMOD_0p5_10mA\n"
            lvds_clamp_diode += f"DENP{count} {pGND} {pin} DMOD_0p5_10mA\n"
            lvds_clamp_diode += "*\n"
            if input_pin_n:
                lvds_clamp_diode += f"DEPN{count} {input_pin_n[count-1]} {pVCC} DMOD_0p5_10mA\n"
                lvds_clamp_diode += f"DENN{count} {pGND} {input_pin_n[count-1]} DMOD_0p5_10mA\n"
                lvds_clamp_diode += "*\n"
        
    lvds_clamp_diode += f".model DMOD_0p5_10mA D N=1.0 IS=3.75e-11 RS=150m\n"
    lvds_clamp_diode += "*\n"
    
    return lvds_clamp_diode
    
# Functions to generate LVDS subckt
def gen_lvds_subckt(kpn):
    kpn = kpn.replace('-', '_') if '-' in kpn else kpn

    '''Function returns filled subckt section'''
   
    lvds_subckt = ".subckt lvds_out_"+kpn+""" %VDD %OUTP %OUTN %GND
* Output stage  *
* MP7 and MN8 turn on together to pull 
* OUT high, and MN7 and MP8 turn on
* together to pull OUT low.
*\n"""
    # default values
    lvds_subckt += "MPD1 %MNPA %VDD %VDD %VDD ML2WP2A L=2u W=15u\n"
    lvds_subckt += "MP7 %OUTP %M5D %MNPA %MNPA PMOD_OUT L=1u W=300u\n"
    lvds_subckt += "MP8 %OUTN %M6D %MNPA %MNPA PMOD_OUT L=1u W=300u\n"
    lvds_subckt += "MN7 %OUTP %M5D %MNDA %MNDA NMOD_OUT L=1u W=200u\n"
    lvds_subckt += "MN8 %OUTN %M6D %MNDA %MNDA NMOD_OUT L=1u W=200u\n"
    lvds_subckt += "MND1 %MNDA %GND %GND %GND ML2WN2A L=2u W=15u\n"
    lvds_subckt += """
*
* Default Model state : out(Pin 4) is high,
* outn(Pin 5) is low. Swap PU/PD on m5d and 
* m6d nodes to reverse the state.
*
RPU %VDD %M6D 100K
RPD %M5D %GND 100K
*
* All Models\n"""


    lvds_subckt += ".model PMOD_OUT UCBMOS PMOS VTO=0.7 KP=300u RD=49 RS=49\n"
    lvds_subckt += ".model NMOD_OUT UCBMOS NMOS VTO=-0.7 KP=350u RD=50 RS=50\n"
    lvds_subckt += ".model ML2WN2A UCBMOS NMOS VTO=-0.5 KP=6.20m RD=5m RS=5m\n"
    lvds_subckt += ".model ML2WP2A UCBMOS PMOS VTO=0.5 KP=6.20m RD=5m RS=5m\n"
    lvds_subckt += "* \n.ends \n"
    
    return lvds_subckt

# Harness generation functions
def gen_lvds_harness(kpn, pin_list, vcc=None, vPos=None, vNeg=None):
    '''Function returns filled harness for test'''

    vinb = False
    call_pin_list = []
    for pin in pin_list:
        if "vcc" in pin[1].lower():
            pin = pin[1].replace("VCC", "%VCC")
            call_pin_list.append("%VCC")
        #Check "not_in" before "in" to avoid error on not_in pins
        elif "not_in" in pin[1].lower():
            pin = pin[1].replace("NOT_IN", "%NOT_IN")
            vinb = True
            call_pin_list.append(pin)
        elif "din" in pin[1].lower():
            vin = str(pin[0])
            call_pin_list.append(str(pin[0]))
        elif "in_pos" in pin[1].lower() or "in_neg" in pin[1].lower():
            vin = "%VIN"
            call_pin_list.append("%VIN")
        elif "in" in pin[1].lower():
            pin = pin[1].replace("IN", "%IN")
            vin = pin
            call_pin_list.append(pin)
        #Check "not_out" before "out" to avoid error on not_out pins
        elif "not_out0" in pin[1].lower() or "out_1" in pin[1].lower() or "dout_neg" in pin[1].lower():
            call_pin_list.append("%NOTQ")
        elif "out0" in pin[1].lower() or "out_2" in pin[1].lower() or "dout_pos" in pin[1].lower():
            call_pin_list.append("%Q")
        elif "not_out" in pin[1].lower():
            pin = pin[1].replace("NOT_OUT", "%NOT_OUT")
            call_pin_list.append(pin)
        elif "out" in pin[1].lower() and not "_pos" in pin[1].lower():
            pin = pin[1].replace("OUT", "%OUT")
            call_pin_list.append(pin)
        elif "gnd" in pin[1].lower():
            call_pin_list.append("%GND")
        else:
            call_pin_list.append(str(pin[0]))

    # Configuration for fixture.cki
    reg_lvds = "Test circuit for "+kpn+"\n"
    reg_lvds += ".include '"+kpn+".inc'\n"
    reg_lvds += ".options DCPATH ONECONN\n"
    reg_lvds += "*\n*\n"
    reg_lvds += "X1 "+" ".join(call_pin_list)+" '"+kpn+"'\n"
    reg_lvds += "\n\n"
    reg_lvds += "VCC %VCC 0 dc PWL(0 0 10u "+str(vcc)+")\n"
    if vinb: 
        reg_lvds += "vinb %NOT_IN0 0 dc PWL(0 0 10u "+str(vNeg)+")\n"
        reg_lvds += "VEE %GND 0 dc PWL(0 0 10u 0)\n"
    reg_lvds += "\n\n"
    reg_lvds += "RQ %Q %NOTQ 100\n"
    reg_lvds += ".post tran i(all)\n"
    reg_lvds += ".tran 1u 40u\n"
    reg_lvds += ".end\n"
    
    return reg_lvds

# core_cmd file generation functions for lvds
def gen_lvds_cmd(DOUTP, DOUTN, delta, com):
    '''Function returns filled core.cmd for testing LVDS '''
    reg_cmd = "si fixture\n"
    reg_cmd += "print \" Supply DVDD : %s\" yvalue(vcc,15u)\n"
    # Not applicable to 1822-1299 ---------------------------------------------
    reg_cmd += "print \" Supply DGND : %s\" yvalue(vee,15u)\n"
    reg_cmd += "print \" \" \n"
    reg_cmd += "print \" Output DOUTP : %s (" + DOUTP + "V)\" yvalue(v(Q),15u)\n"
    reg_cmd += "print \" Output DOUTN : %s (" + DOUTN + "V)\" yvalue(v(NOTQ),15u)\n"
    reg_cmd += "print \" Output delta : %s (" + delta + "mV)\" (yvalue(v(Q),15u)-yvalue(v(NOTQ),15u))\n"
    reg_cmd += "print \" Output com : %s (" + com + "V)\" (yvalue(v(Q),15u)+yvalue(v(NOTQ),15u))/2\n"
    reg_cmd += "print \" \" \n"
    # ------------------------------------------------------------------------
    reg_cmd += "#------PRINTING BRANCH CURRENTS---------------\n"
    reg_cmd += "print \" Analog Supply Current IVCC : %s\" yvalue(abs(i(vcc)),15u)\n"
    reg_cmd += "#print \" Analog Supply Current IVEE : %s\" yvalue(abs(i(vee)),15u)\n"

    reg_cmd += "##------PRINTING CURVES NOW--------------------\n"
    reg_cmd += "##print \"**********************************************************\"\n"
    reg_cmd += "#print \" BUS Supply Current IVCC\"\n"
    reg_cmd += "#print \"***********************************************************\"\n"
    reg_cmd += "#set graphdev IVCC\n"
    reg_cmd += "#gr abs(i(vcc)) ; v(Q) ; v(NOTQ)\n"
    reg_cmd += "##print \"***********************************************************\"\n"
    reg_cmd += "##print \" BUS Supply Current IVEE\"\n"
    reg_cmd += "##print \"***********************************************************\"\n"
    reg_cmd += "##set graphdev IVEE\n"
    reg_cmd += "##gr abs(i(vee))\n"
    return reg_cmd

# ---- END OF LVDS FUNCTIONS ----

# ---- START OF ECL FUNCTIONS ----
def main_gen_ecl_model(pin_list, inputType, pVCC, pGND, kpn):
    res = gen_ecl_model(kpn, pin_list, inputType, pVCC, pGND)
    res += gen_ecl_mcl(pVCC, pGND)
    res += ".ends\n"
    res += "*******************************************************************\n"
    res += "********************** SUB-CIRCUIT ********************************\n"
    res += "*******************************************************************\n\n"
    if inputType != "LVDS":
        res += gen_hsd_inp_subckt(kpn, inputType, pVCC, pGND)
    res += gen_ecl_outp_subckt(kpn)
    return res

def gen_ecl_model(kpn, pin_list, inputType, pVCC, pGND):
    '''Function to generate ECL model'''
    reg_model = ""

    call_pin_list = []
    for pin_index in range(len(pin_list)):
        call_pin_list.append(str(pin_index+1))

    reg_model += "* \n"
    reg_model += ".subckt '"+kpn+"' "+" ".join(call_pin_list)+"\n" 
    reg_model += get_ecl_model_configurations(kpn, pin_list, inputType, pVCC, pGND)
    reg_model += "* \n"

    # Generate 1 ohm resistor network for similar pins
    reg_model += short_similar_pins(pin_list, 1)

    reg_model+= "*\n"
    return reg_model

def get_ecl_model_configurations(kpn, pin_list, inputType, pVCC, pGND):
    '''Function returns ecl model configuration'''
    en_ecl_model_config = "*\n"
    en_ecl_model_config += "* Model for "+kpn+" goes here\n"
    inp, outp = gen_hsd_io_interfaces(kpn, pin_list, inputType, outputType="ECL", pVCC=pVCC, pVEE=pGND)
    en_ecl_model_config += inp + '*\n' + outp
    return en_ecl_model_config


def gen_ecl_input_pins(kpn, pin_list, pVCC, pVEE):
    # Input pin setup
    input_pin_p = []
    input_pin_n = []
    
    for pin in pin_list:
        if "not_d" in pin[1].lower():
            input_pin_n.append(pin[0])
        elif "d" in pin[1].lower() and not "gnd" in pin[1].lower():
            input_pin_p.append(pin[0])

    # ECL Input stage
    if len(input_pin_p) == len(input_pin_n):
        inText = "* Input Interface\n"
        for count in range(len(input_pin_p)):
            inText += "XI"+str(count)+" "+str(input_pin_p[count])+" "+str(input_pin_n[count])+" "+pVCC+" "+pVEE+" inp_ecl_"+kpn+"\n"
        return inText
    else: 
        print("Either Input P pin count and Input N pin count are not the same\n")
        return ""


def gen_ecl_output_pins(kpn, pin_list, pVCC, pVEE):
    # Output pin setup 
    output_pin_p = []
    output_pin_n = []
    for pin in pin_list:
        if "not_q" in pin[1].lower():
            output_pin_n.append(pin[0])
        elif "q" in pin[1].lower():
            output_pin_p.append(pin[0])

    # ECL Output stage
    if len(output_pin_p) == len(output_pin_n):
        outText = "* Output Interface\n"
        for count in range(len(output_pin_p)):
            outText += "XO"+str(count)+" "+str(output_pin_p[count])+" "+str(output_pin_n[count])+" "+pVCC+" "+pVEE+" outp_ecl_"+kpn+"\n"
        return outText
    else: 
        print("Output P pin count and Output N pin count are not the same\n")
        return ""


def gen_ecl_mcl(pVCC, pGND): 
    ecl_mcl = f"mcl {pVCC} {pGND} {pGND} {pGND} ML2WN2A L=2u W=78u\n"
    ecl_mcl += ".model ML2WN2A UCBMOS NMOS VTO=-0.7 KP=816.3u RD=500m RS=500m\n"
    return ecl_mcl

def gen_ecl_inp_subckt(kpn, pGND=None, pVEE=None): 
    '''Function returns filled subckt section'''
    
    ecl_in_subckt = ".subckt inp_ecl_"+kpn+""" %in %vbb %vcc %vee
****************
*Input stage IN*
****************\n"""

    ecl_in_subckt += "RIN %in %vee 75k\n"
    ecl_in_subckt += "RIN2 %in %vcc 37k\n"
    if pVEE and not pGND: 
        ecl_in_subckt += "RINB %inb %vee 75k\n"
        
    ecl_in_subckt += "Q1 %c1 %in %e QMOD_IN\n"
    
    if pVEE and not pGND: 
        ecl_in_subckt += "Q2 %c2 %inb %e QMOD_IN\n"
    else: 
        ecl_in_subckt += "Q2 %c2 %vbb %e QMOD_IN\n"
        
    ecl_in_subckt += """* Resistors in RC1 and RC2 are 
* estimates. Typ values for RC1 
* and RC2 for ECL families are 
* used here.
RC1 %c1 %vcc 215
RC2 %c2 %vcc 245
CC1 %c1 %vcc 500p
CC2 %c2 %vcc 500p
* MCA is a 4mA current sink
MCA %e %vee %vee %vee ML2WN4A L=2u W=40u
***************************
*Models*
***************************
.model QMOD_IN  NPN    BF=100 RC=1 RE=1 RB=1 IS=45p
.model ML2WN4A  MOSFET NMOS VTO=-0.4 KP=816.3u 
+                      RD=500m RS=500m
.ends\n"""

    return ecl_in_subckt

def gen_ecl_outp_subckt(kpn):
    kpn = kpn.replace('-', '_') if '-' in kpn else kpn
    '''Function returns filled subckt section'''
    
    ecl_out_subckt = ".subckt outp_ecl_"+kpn+""" %q %qb %vcc %vee
****************
*Output stage*
****************
QO  %vcc %b1 %q  QMOD_OUT
QOB %vcc %b2 %qb QMOD_OUT
* Biased the bases,
* estimated RB1 and RB2 values\n"""

    ecl_out_subckt += "RB1 %vcc %b1 195\n"
    ecl_out_subckt += "RB2 %vcc %b2 125\n"
    
    ecl_out_subckt += "* MB1 and MB2 are 2mA and 6mA current sinks\n"
    ecl_out_subckt += "MB1 %b1 %vee %vee %vee ML2WN2A L=2u W=60u\n"
    ecl_out_subckt += "MB2 %b2 %vee %vee %vee ML2WN2A L=2u W=10u\n"
    ecl_out_subckt += """ ***************************
*Models*
***************************
.model QMOD_OUT  NPN  BF=100 
+      RC=1 RE=4 RB=1 IS=222f
.model ML2WN2A UCBMOS NMOS VTO=-0.7
+      KP=816.3u RD=500m RS=500m
.ends\n"""

    return ecl_out_subckt 

# Harness generation functions
def gen_ecl_harness(kpn, pin_list, vcc=None, vin=None, vee=None, vtt=None):
    '''Function returns filled harness for test'''

    if not (vcc and vee and vtt):
        raise Exception("[ERROR] cannot generate ECL harness due to one or more of the required inputs (VCC, VEE/GND & VTD) have not been provided!")
    
    count = 0
    call_pin_list = []
    for i, pin in enumerate(pin_list):
        if "vcc" in pin[1].lower():
            call_pin_list.append("%vcc")
        elif "vee" in pin[1].lower():
            call_pin_list.append("%vee")
        elif "not_q0" in pin[1].lower():
            call_pin_list.append("%NOTQ")
        elif "q0" in pin[1].lower():
            call_pin_list.append("%Q")
        elif "not_q" in pin[1].lower():
            pin = pin[1].replace("NOT_Q", "%NOTQ")
            call_pin_list.append(pin)
        elif "q" in pin[1].lower():
            pin = pin[1].replace("Q", "%Q")
            count +=1
            call_pin_list.append(pin)
        elif "not_d" in pin[1].lower() or "not_d0" in pin[1].lower():
            call_pin_list.append("%vinb")
        elif "d" in pin[1].lower() or "d0" in pin[1].lower():
            call_pin_list.append("%vin")
        elif "vt" in pin[1].lower():
            call_pin_list.append("%vtt")
        elif "gnd" in pin[1].lower():
            call_pin_list.append("0")
        else:
            call_pin_list.append(str(i+1))

    # Configuration for fixture.cki
    reg_ecl = "Test circuit for "+kpn+"\n"
    reg_ecl += ".include '"+kpn+".inc'\n"
    reg_ecl += ".options DCPATH ONECONN\n"
    reg_ecl += "X1 "+" ".join(call_pin_list)+" '"+kpn+"'\n"
    reg_ecl += "\n\n"
    reg_ecl += "VCC %vcc 0 dc PWL(0 0 10u "+vcc+")\n"
    reg_ecl += "VEE %vee 0 dc PWL(0 0 10u "+vee+")\n"
    reg_ecl += "VIN %vin 0 PULSE("+vin+" 0 0 0 0 10u 20u)\n"
    reg_ecl += "VINB %vinb 0 PULSE(-"+vin+" 0 0 0 0 10u 20u)\n"
    reg_ecl += "\n\n"
    reg_ecl += "RQ %vtt %Q 50\n"
    reg_ecl += "RQB %vtt %NOTQ 50\n"
    if count > 0: 
        for index in range(count): 
            reg_ecl += "RQ"+str(index+1)+" %vtt %Q"+str(index+1)+" 50\n"
            reg_ecl += "RQB"+str(index+1)+" %vtt %NOTQ"+str(index+1)+" 50\n"
            reg_ecl += "*\n"   
    reg_ecl += "VTT %vtt 0 PWL(0 0 10u "+vtt+")\n"
    reg_ecl += "\n\n"
    reg_ecl += ".post tran i(all)\n"
    reg_ecl += ".tran 1u 40u\n"
    reg_ecl += ".end\n"
    
    return reg_ecl, count

# core_cmd file generation functions for ecl
def gen_ecl_cmd(VOH, VOL, delta, com):
    '''Function returns filled core.cmd for testing ECL '''
    reg_cmd = "si fixture\n"
    reg_cmd += "#------PRINTING NODE VOLTAGES-----------------\n"
    reg_cmd += "print \" positive Supply Voltage VCC : %s\" yvalue(vcc,15u)\n"
    reg_cmd += "print \"\" \n"
    reg_cmd += "#print \" Input voltage D : %s\" yvalue(vin,15u)\n"
    reg_cmd += "print \"\" \n"
    reg_cmd += "print \" Output VOH : %s (" + VOH + "V)\" yvalue(v(Q),15u)\n"
    reg_cmd += "print \" Output VOL : %s (" + VOL + "V)\" yvalue(v(NOTQ),15u)\n"
    reg_cmd += "print \" Output delta : %s (" + delta + "mV)\" (yvalue(v(Q),15u)-yvalue(v(NOTQ),15u))\n"
    reg_cmd += "print \" Output com : %s (" + com + "V)\" (yvalue(v(Q),15u)+yvalue(v(NOTQ),15u))/2\n"
    reg_cmd += "#------PRINTING BRANCH CURRENTS---------------\n"
    reg_cmd += "print \"\" \n"
    reg_cmd += "print \" Analog Supply Current IVCC : %s\" yvalue(abs(i(vcc)),15u)\n"
    reg_cmd += "print \" Analog Supply Current IVEE : %s\" yvalue(abs(i(vee)),15u)\n"
    reg_cmd += "print \"\" \n"
    reg_cmd += "#print \" CURRENT MCA D input subckt : %s\" yvalue(abs(i(x1.xi.mca.d)),15u)\n"
    reg_cmd += "#print \" CURRENT MB1 : %s\" yvalue(abs(i(x1.xo.mb1.d)),15u)\n"
    reg_cmd += "#print \" CURRENT MB2 : %s\" yvalue(abs(i(x1.xo.mb2.d)),15u)\n"
    reg_cmd += "#print \" \" \n"
    reg_cmd += "#------PRINTING CURVES NOW--------------------\n"
    reg_cmd += "#print \" BUS Supply Current IVCC\"\n"
    reg_cmd += "\n"
    reg_cmd += "#gr abs(i(vcc)) ; abs(vin) ; abs(v(Q)) ; abs(v(NOTQ))\n"
    reg_cmd += "#print \"***********************************************************\"\n"
    return reg_cmd

# ---- END OF ECL FUNCTIONS ----

# ---- START OF CML FUNCTIONS ----
def main_gen_cml_model(pin_list, inputType, pVCC, pGND, kpn):
    res = ""
    res += gen_cml_model(kpn, pin_list, inputType, pVCC, pGND)
    res += ".ends\n"
    res += "*******************************************************************\n"
    res += "********************** SUB-CIRCUIT ********************************\n"
    res += "*******************************************************************\n"
    if inputType != "LVDS":
        res += gen_hsd_inp_subckt(kpn, inputType, pVCC, pGND)
    res += gen_cml_outp_subckt(kpn)
    return res


def gen_cml_model(kpn, pin_list, inputType, pVCC, pGND):
    '''Function to generate CML model'''
    reg_model = ""

    call_pin_list = []
    for pin_index in range(len(pin_list)):
        call_pin_list.append(str(pin_index+1))

    reg_model += "* \n"
    reg_model += ".subckt '"+kpn+"' "+" ".join(call_pin_list)+"\n" 
    reg_model += get_cml_model_configurations(kpn, pin_list, inputType, pVCC, pGND)
    reg_model += "* \n"

    # Resistor shorts
    reg_model += short_similar_pins(pin_list, 1)
    reg_model += "*\n"
    
    return reg_model


def get_cml_model_configurations(kpn, pin_list, inputType, pVCC, pVEE):
    '''Function returns cml model configuration'''
    en_cml_model_config = "*\n* Model for "+kpn+" goes here\n"
    
    # Input and output pin setup 
    # TODO: Add support for multiple inputs and outputs
    
    # Pull-down resistor
    en_cml_model_config+= "* RPD added to match the supply current of 90m at 2.5V\n"
    en_cml_model_config+= "RPD "+pVCC+" "+pVEE+" 38\n"
    en_cml_model_config+= "*\n"
    inp, outp = gen_hsd_io_interfaces(kpn, pin_list, inputType, outputType="CML", pVCC=pVCC, pVEE=pVEE)
    en_cml_model_config += inp + outp
    # Connect exposed pad to VEE
    en_cml_model_config+= "* Connecting Exposed Pad to VEE\n"
    en_cml_model_config+= "RVE "+pVEE+" %PMH1 1\n"
    en_cml_model_config+= "*\n"

    return en_cml_model_config


def gen_cml_input_pins(kpn, pin_list, pVCC, pVEE):
    # Input pin setup
    input_pin_p = []
    input_pin_n = []
    vt = []

    for pin in pin_list:
        if "in" in pin[1].lower() and "_neg" in pin[1].lower():
            input_pin_n.append(pin[0])
        elif "in" in pin[1].lower() and "_pos" in pin[1].lower():
            input_pin_p.append(pin[0])
        elif "vt" in pin[1].lower():
            vt.append(pin[0])

    if len(input_pin_p) == len(input_pin_n):
        inText = "* Input Interface\n"
        for count in range(len(input_pin_p)):
            inText += "XI"+str(count)+" "+str(input_pin_p[count])+" "+str(input_pin_n[count])+" "+str(vt[count])+" "+str(vt[count])+" "+pVCC+" "+pVEE+" diff_inp_"+kpn+"\n"
        return inText
    else: 
        raise Exception("Either Input P pin count and Input N pin count are not the same\n")


def gen_cml_output_pins(kpn, pin_list, pVCC, pVEE):
    # Output pin setup
    output_pin_p = []
    output_pin_n = []
    
    for pin in pin_list:
        if "q" in pin[1].lower() and "_neg" in pin[1].lower():
            output_pin_n.append(pin[0])
        elif "q" in pin[1].lower() and "_pos" in pin[1].lower():
            output_pin_p.append(pin[0])
        
    # CML Output stage
    if len(output_pin_p) == len(output_pin_n):
        outText = "* Output Interface\n"
        for count in range(len(output_pin_p)):
            outText += "XO"+str(count)+" "+str(output_pin_p[count])+" "+str(output_pin_n[count])+" "+pVCC+" "+pVEE+" cml_outp_"+kpn+"\n"
        return outText
    else: 
        raise Exception("Output P pin count and Output N pin count are not the same\n")

def gen_cml_outp_subckt(kpn):
    kpn = kpn.replace('-', '_') if '-' in kpn else kpn
    '''Function returns filled subckt section'''

    cml_subckt = ".subckt cml_outp_"+kpn+""" %q %qb %vcc %gnd
**********************
*  CML output stage  *
**********************
RC50a %vcc %q 50
RC50b %vcc %qb 50
QO1 %qb %b1 %e QMOD_OUT
QO2 %q %b2 %e QMOD_OUT
CC1 %q %vcc 500p
CC2 %qb %vcc 500p
*** MCA = 16mA current sink
MCA %e %gnd %gnd %gnd ML2WN4A L=2u W=1.6u
CE %e %gnd 50p
* Add the resistive divider here
R1 %vcc %b1 200
R2 %b1 %gnd 500
R3 %vcc %b2 500
R4 %b2 %gnd 100
*** All Models
.model QMOD_OUT NPN BF=100 RC=10 RE=10 RB=100
.model ML2WN4A MOSFET NMOS VTO=-0.7 KP=81.63m RD=5m RS=5m 
+RD=5m RS=5m
.ends\n"""
    return cml_subckt

def gen_cml_inp_subckt(kpn):
    cml_subckt = ".subckt diff_inp_"+kpn+""" %in %inb %vtin %vtinb %vcc %gnd
**********************
*  CML input stage  *
**********************
RC50a %vcc %q 50
RC50b %vcc %qb 50
QO1 %q %in %e QMOD_IN
QO2 %qb %inb %e QMOD_IN
CC1 %q %vcc 500p
CC2 %qb %vcc 500p
Rinp %in %vtin 50 
Rinn %inb %vtinb 50
*** MSA = 4mA current sink
MSA %e %gnd %gnd %gnd ML2WN2A L=2u W=40u
CE %e %gnd 50p
* Protection diode at IN\n"""

    cml_subckt += "DINP %in %vcc DMOD_0p5v_10mA\n"
    cml_subckt += "DINN %gnd %in DMOD_0p5v_10mA\n"
    cml_subckt += "*** All Models \n"
    cml_subckt += ".model QMOD_IN NPN BF=100 RC=1 RE=1 RB=10\n"
    cml_subckt += ".model DMOD_0p5v_10mA D N=1 IS=33n RS=3.5\n"
    cml_subckt += ".model ML2WN2A UCBMOS NMOS VTO=-0.7 KP=816.3u RD=500m RS=500m\n"
    cml_subckt += "* +RD=5m RS=5m\n"
    cml_subckt += ".ends\n"
    return cml_subckt


# Harness generation functions
def gen_cml_harness(kpn, pin_list, vcc=None, vee=None, vin=None):
    '''Function returns filled harness for test'''
    
    if not (vcc and vee):
        raise Exception("[ERROR] cannot generate CML harness due to one or more of the required inputs (VCC, VEE/GND) have not been provided!")

    call_pin_list = []
    for i, pin in enumerate(pin_list):
        if "vcc" in pin[1].lower():
            call_pin_list.append("%VCC")
        #elif "not_q" in pin_list[pin_index][1].lower():
        #    call_pin_list.append("%NOTQ")
        #elif "q" in pin_list[pin_index][1].lower():
        #    call_pin_list.append("%Q")
        elif "in" in pin[1].lower() and "_pos" in pin[1].lower():
            call_pin_list.append("%VIN")
        #elif "vt" in pin_list[pin_index][1].lower():
        #    call_pin_list.append("%VT")
        elif "gnd" in pin[1].lower():
            call_pin_list.append("0")
        else:
            call_pin_list.append(str(i+1))

    # Configuration for fixture.cki
    reg_cml = "Test circuit for "+kpn+"\n"
    reg_cml += ".include '"+kpn+".inc'\n"
    reg_cml += ".options DCPATH ONECONN\n"
    reg_cml += "X1 "+" ".join(call_pin_list)+" '"+kpn+"'\n"
    reg_cml += "\n\n"
    reg_cml += "VCC %vcc 0 dc PWL(0 0 10u "+vcc+")\n"
    reg_cml += "VEE %GND 0 dc PWL(0 0 10u "+vee+")\n"
    # reg_cml += "VIN %vin 0 dc PWL(0 0 10u "+vin+")\n"
    reg_cml += "* VIN %VIN 0 PULSE(3.3 0 0 0 0 10u 20u)\n"
    reg_cml += "*VINB %VINB 0 PULSE(3.3 0 0 0 0 10u 20u)\n"
    reg_cml += "\n\n"
    reg_cml += "RQ %vcc %Q 50\n"
    reg_cml += "RQB %vcc %NOTQ 50\n"
    reg_cml += "\n\n"
    reg_cml += ".post tran i(all)\n"
    reg_cml += ".tran 1u 40u\n"
    reg_cml += ".end\n"
    
    return reg_cml


# core_cmd file generation functions for cml
def gen_cml_cmd(VOH, VOL, delta, com):
    '''Function returns filled core.cmd for testing CML '''
    reg_cmd = "si fixture\n"
    reg_cmd += "#------PRINTING NODE VOLTAGES-----------------\n"
    reg_cmd += "print \" positive Supply Voltage VCC : %s\" yvalue(VCC,15u)\n"
    reg_cmd += "print \"\" \n"
    reg_cmd += "#print \" Input voltage D : %s\" yvalue(VIN,15u)\n"
    reg_cmd += "print \"\" \n"
    reg_cmd += "print \" Output VOH : %s (" + VOH + "V)\" yvalue(v(Q),15u)\n"
    reg_cmd += "print \" Output VOL : %s (" + VOL + "V)\" yvalue(v(NOTQ),15u)\n"
    reg_cmd += "print \" Output delta : %s (" + delta + "mV)\" (yvalue(v(Q),15u)-yvalue(v(NOTQ),15u))\n"
    reg_cmd += "print \" Output com : %s (" + com + "V)\" (yvalue(v(Q),15u)+yvalue(v(NOTQ),15u))/2\n"
    reg_cmd += "\n\n"
    reg_cmd += "#------PRINTING BRANCH CURRENTS---------------\n"
    reg_cmd += "print \"\" \n"
    reg_cmd += "print \" Analog Supply Current IVCC : %s\" yvalue(abs(i(VCC)),15u)\n"
    reg_cmd += "print \" Analog Supply Current IVEE : %s\" yvalue(abs(i(VEE)),15u)\n"
    reg_cmd += "print \"\" \n"
    reg_cmd += "#print \" CURRENT MCA D input subckt : %s\" yvalue(abs(i(x1.xi.mca.d)),15u)\n"
    reg_cmd += "#print \" CURRENT MB1 : %s\" yvalue(abs(i(x1.xo.mb1.d)),15u)\n"
    reg_cmd += "#print \" CURRENT MB2 : %s\" yvalue(abs(i(x1.xo.mb2.d)),15u)\n"
    reg_cmd += "#print \"\" \n"
    reg_cmd += "#------PRINTING CURVES NOW--------------------\n"
    reg_cmd += "#print \"**********************************************************\"\n"
    reg_cmd += "#print \" BUS Supply Current IVCC\"\n"
    reg_cmd += "\n"
    reg_cmd += "#gr abs(i(VCC)) ; abs(VIN) ; abs(v(Q)) ; abs(v(NOTQ))\n"
    reg_cmd += "#print \"***********************************************************\"\n"
    
    return reg_cmd

# ---- END OF CML FUNCTIONS ----

# Supporting functions
def gen_hsd_io_interfaces(kpn, pin_list, inputType, outputType, pVCC, pVEE=None):
    input_pins = ""
    output_pins = ""

    kpn = kpn.replace('-', '_') if '-' in kpn else kpn

    if inputType == "LVDS":
        input_pins = gen_lvds_input_pins(pin_list)
    elif inputType == "ECL":
        input_pins = gen_ecl_input_pins(kpn, pin_list, pVCC, pVEE)
    elif inputType == "CML":
        input_pins = gen_cml_input_pins(kpn, pin_list, pVCC, pVEE)

    if outputType == "LVDS":
        output_pins = gen_lvds_output_pins(kpn, pin_list, pVCC, pVEE)
    elif outputType == "ECL":
        output_pins = gen_ecl_output_pins(kpn, pin_list, pVCC, pVEE)
    elif outputType == "CML":
        output_pins = gen_cml_output_pins(kpn, pin_list, pVCC, pVEE)

    return input_pins, output_pins

def gen_hsd_inp_subckt(kpn, inputType, pVCC=None, pVEE=None):
    kpn = kpn.replace('-', '_') if '-' in kpn else kpn
    if inputType == "ECL":
        return gen_ecl_inp_subckt(kpn, pVCC, pVEE)
    elif inputType == "CML":
        return gen_cml_inp_subckt(kpn)


def convert_sci_to_eng(number):
    '''Function converts scientific notation to engineering notation'''
    # Use Hpspice to convert
    if os.name == 'nt':
        number = os.popen("C:/cygwin/bin/bash.exe --login -i -c \"/cygdrive/c/es/roq/bin/hpspice.exe -s -c '"+str(number)+"'\"").read()
    else:
        number = os.popen("C:/cygwin/bin/bash.exe --login -i -c \"/cygdrive/c/es/roq/bin/hpspice.exe -s -c '"+str(number)+"'\" 2>/dev/null").read()
    number = number.strip(" \n")
    return number

def convert_eng_to_sci(number):
    '''Function converts engineering notation to scientific notation'''
    if number[-1].lower() == "m":
        number = number[:-1]+"e-3"
    elif number[-1].lower() == "u":
        number = number[:-1]+"e-6"
    elif number[-1].lower() == "n":
        number = number[:-1]+"e-9"
    elif number[-1].lower() == "a":
        number = number[:-1]+"e-10"
    elif number[-1].lower() == "p":
        number = number[:-1]+"e-12"
    elif number[-1].lower() == "f":
        number = number[:-1]+"e-15"
    elif number[-1].lower() == "k":
        number = number[:-1]+"e+3"
    elif number[-3:].lower() == "meg":
        number = number[:-3]+"e+6"
    elif number[-1].lower() == "g":
        number = number[:-1]+"e+9"
    return float(number)

def short_similar_pins(pin_list, resistance=1):
    """Function returns resistor interconnection network for given pin list"""
    global MAX_PIN_COUNT
    merged_pin_list = "\n".join([" ".join(row) for row in pin_list])
    # List of pin groups to be shorted
    pin_groups = re.findall(".* ([a-zA-Z0-9_]*)_1", merged_pin_list)
    # Dictionary for group wise pin list
    pin_group_list = {}
    # Get pin numbers for pins to be shorted in each group
    for group in pin_groups:
        group_pins = re.findall("(.*) "+group+"_[0-9]+", merged_pin_list)
        if len(group_pins) <= MAX_PIN_COUNT:
            pin_group_list[group] = group_pins
    # Generate pin short resistors shorted pins
    shorted_pins = ""
    for group in pin_group_list.keys():
        count = 1
        shorted_pins += "* Resistor shorts for "+group+" pins\n"
        for index1 in range(len(pin_group_list[group])):
            for index2 in range(len(pin_group_list[group])):
                if index2 > index1:
                    shorted_pins += "R"+str(group)+str(count)+" "+str(pin_group_list[group][index1])+" "+str(pin_group_list[group][index2])+" "+str(resistance)+"\n"
                    count += 1
    return shorted_pins
