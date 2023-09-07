#! /usr/bin/env python
# -*- coding: utf-8 -*-
# *************************************************************************************
# Digital IC model generator with optimized parameters (UI backend)
# Script version: 2.0
# Python version: Python 3.8.10
# Compatible OS: Windows 10
# Requirements: Tkinter, pyperclip, Hpspice, digital_ic_gui.py, lib_digital_ic.py
# Developer (v2.0): Darryl Ng
# Notes:
#     This is a script to provide backend compute functionality
#       for the UI created by 'digital_ic_gui.py'.
#   Command: python3 digital_ic_support.py
# Version doc:
#  * First version
# *************************************************************************************
#  * Version 2.0
#  * 1. Streamlined modelling process
#  * 2. Implemented necessary functions for GUI widgets
#  * 3. Handle the passing of parameters to the optimization scripts
#  * 4. Existing inc file will be appended with the generated model
# *************************************************************************************
#
# Future improvements:
#  * 1. Refine load pins function logic if necessary
#

import pyperclip as pc
import sys
import tkinter as tk
from tkinter import messagebox
import os

import digital_ic_gui
import lib_digital_ic
import optimizeCML
import optimizeECL
import optimizeLVDS
from util import runCmd

# Global members
PIN_LIST = []

def main(*args):
    '''Main entry point for the application.'''
    global root
    root = tk.Tk()
    root.protocol( 'WM_DELETE_WINDOW' , root.destroy)
    # Creates a toplevel widget.
    global _w1
    _w1 = digital_ic_gui.Toplevel1(root)
    root.mainloop()

def copyBtnClicked(*args):
    print('digital_ic_support.copyBtnClicked')
    pc.copy(_w1.Scrolledtext1.get("1.0", tk.END))


# Generate button clicked
def inputInterfaceButtonClicked(*args):
    print('digital_ic_support.inputInterfaceButtonClicked')
    if not reqFieldsFilled():
        messagebox.showerror("Input Error", "Please fill all the required fields.")
        return
    
    try:
        pinStartNum = len(_w1.resultBox.get("1.0", tk.END).splitlines()) - 1 # account for newline
        inp = lib_digital_ic.gen_hsd_inp_interface(kpn=_w1.kpn.get(), inputType=_w1.inputInterfaceOption.get(),
                                                    pVCC=_w1.vccPinNum.get(), pVEE=_w1.gndPinNum.get(),
                                                    posPinNum=_w1.posPinNum.get(), negPinNum=_w1.negPinNum.get(),
                                                    pinStartNum=pinStartNum)
        _w1.resultBox.insert(tk.END, inp)
    except Exception as e:
        print("Error in updating Listbox: ",e)


def resultBoxClearBtnClicked(*args):
    _w1.resultBox.delete("1.0", tk.END)


# ---------------------- No Output model ----------------------
def createNoneBtnClicked(*args):
    kpn = _w1.kpn.get()
    print("[INFO] Generating model ...", flush=True)
    reg_model = lib_digital_ic.main_gen_no_output_model(pin_list=PIN_LIST, inputText=_w1.resultBox.get("1.0", tk.END),
                    inputSubckts=getInputInterfaces(), pVCC=_w1.vccPinNum.get(), pGND=_w1.gndPinNum.get(), kpn=kpn)

    print("[INFO] Generating model ... done", flush=True)

    _w1.Scrolledtext1.configure(state='normal')
    _w1.Scrolledtext1.insert(tk.INSERT, reg_model)
    _w1.Scrolledtext1.configure(state='disabled')
    print("[INFO] No output modelling completed", flush=True)


# ---------------------- LVDS Output model ----------------------
def createLvdsBtnClicked(*args):
    if not checkPinInfo():
        messagebox.showerror("Input Error", "Please fill all the required fields.")
        return

    global _top2, _w2
    _top2 = tk.Toplevel(root)
    _w2 = digital_ic_gui.Toplevel2(_top2)

def submitLvdsBtnClicked(*args):
    print('digital_ic_support.submitLvdsBtnClicked')

    # Clear existing output
    clearScrollText()
    
    # Check if all required fields are filled
    lvds_params_filled = _w2.mpd1_L.get() and _w2.mpd1_H.get() \
                    and _w2.mnd1_L.get() and _w2.mnd1_H.get() \
                    and _w2.pKp_L.get() and _w2.pKp_H.get() \
                    and _w2.pRd_L.get() and _w2.pRd_H.get() \
                    and _w2.pRs_L.get() and _w2.pRs_H.get() \
                    and _w2.nKp_L.get() and _w2.nKp_H.get() \
                    and _w2.nRd_L.get() and _w2.nRd_H.get() \
                    and _w2.nRs_L.get() and _w2.nRs_H.get() \
                    and _w2.voh.get() and _w2.vol.get() \
                    
    if not reqFieldsFilled() or not lvds_params_filled:
        messagebox.showerror("Input Error", "Please fill all the required fields.")
        return

    _top2.withdraw()
    kpn = _w1.kpn.get()
    
    # Generate model
    print("[INFO] Generating model ...", flush=True)
    reg_model = lib_digital_ic.main_gen_lvds_model(pin_list=PIN_LIST, inputText=_w1.resultBox.get("1.0", tk.END),
                                                   inputSubckts=getInputInterfaces(),
                                                pVCC=_w1.vccPinNum.get(), pGND=_w1.gndPinNum.get(), kpn=kpn,
                                                  rawPinInfo=_w1.pinInfoText.get("1.0","end-1c"))

    print("[INFO] Generating model ... done", flush=True)

    # Append generated model to existing .inc file without overwriting data
    # Else create new .inc file if not exist
    model_file = '{}.inc'.format(kpn)
    if os.path.exists(model_file):
        with open(model_file, "r") as f:
            lines = f.readlines()
        with open(model_file, "w") as f:
            for line in lines:
                if ".subckt" in line:
                    line = line.replace(line, reg_model)
                    f.write(line)
                    break
                f.write(line)
    else:
        with open(model_file, 'w') as f:
            f.write(reg_model)


    # Generate harness and write to file
    print("[INFO] Generating harness ...", flush=True)
    reg_harness = lib_digital_ic.gen_lvds_harness(kpn=kpn, pin_list=PIN_LIST, vcc=_w1.vcc.get(), vPos=_w1.vin.get(), vNeg=_w1.vee.get())

    with open("fixture.cki", "w") as f:
        f.write(reg_harness)
    print("[INFO] Generating harness ... done", flush=True)
    

    # Generate core.cmd and write to file
    print("[INFO] Generating core.cmd..", flush=True)
    # calculate target delta and com
    delta = str(round((float(_w2.voh.get()) - float(_w2.vol.get()))*1000))
    com = str(round((float(_w2.voh.get()) + float(_w2.vol.get())) / 2, 2))
    reg_core_cmd = lib_digital_ic.gen_lvds_cmd(_w2.voh.get(), _w2.vol.get(), delta, com)
    
    with open("core.cmd", "w") as f:
        f.write(reg_core_cmd)
    print("[INFO] Generating core.cmd ... done", flush=True)
    
    # Perform optimization
    print("Optimizing parameters. Please wait...", flush=True)
    optimizeLVDS.run_with_params(model_file, float(_w2.mpd1_L.get()), float(_w2.mpd1_H.get()),
                                 float(_w2.mnd1_L.get()), float(_w2.mnd1_H.get()),
                                 float(_w2.pKp_L.get()), float(_w2.pKp_H.get()),
                                 float(_w2.pRd_L.get()), float(_w2.pRd_H.get()),
                                 float(_w2.pRs_L.get()), float(_w2.pRs_H.get()),
                                 float(_w2.nKp_L.get()), float(_w2.nKp_H.get()),
                                 float(_w2.nRd_L.get()), float(_w2.nRd_H.get()),
                                 float(_w2.nRs_L.get()), float(_w2.nRs_H.get()),
                                 float(_w2.voh.get()) ,float(_w2.vol.get()))
    
    print("[INFO] Performing optimization ... done", flush=True)
    
    # print to result box
    with open(model_file, 'r') as f:
        reg_model = f.read()

    _w1.Scrolledtext1.configure(state='normal')
    _w1.Scrolledtext1.insert(tk.INSERT, reg_model)
    _w1.Scrolledtext1.insert(tk.INSERT, "\n\n*******************************************************************\n")
    _w1.Scrolledtext1.insert(tk.INSERT, "********************END OF MODEL BEGIN HARNESS *********************\n")
    _w1.Scrolledtext1.insert(tk.INSERT, "*******************************************************************\n\n")
    _w1.Scrolledtext1.insert(tk.INSERT, reg_harness)
    _w1.Scrolledtext1.insert(tk.INSERT, "\n\n*******************************************************************\n")
    _w1.Scrolledtext1.insert(tk.INSERT, "********************END OF HARNESS BEGIN CMD *********************\n")
    _w1.Scrolledtext1.insert(tk.INSERT, "*******************************************************************\n\n")
    _w1.Scrolledtext1.insert(tk.INSERT, reg_core_cmd)
    _w1.Scrolledtext1.insert(tk.INSERT, "\n\n*******************************************************************\n")
    _w1.Scrolledtext1.insert(tk.INSERT, str(runCmd()))
    _w1.Scrolledtext1.insert(tk.INSERT, "*******************************************************************\n\n")
    _w1.Scrolledtext1.configure(state='disabled')
    
    #print("[INFO] Generating stress.cmd ... done", flush=True)
    print("[INFO] LVDS modelling completed", flush=True)


# ---------------------- ECL Output model ----------------------
def createEclBtnClicked(*args):
    if not checkPinInfo():
        messagebox.showerror("Input Error", "Please fill all the required fields.")
        return
    
    global _top3, _w3
    _top3 = tk.Toplevel(root)
    _w3 = digital_ic_gui.Toplevel3(_top3)

def submitEclBtnClicked(*args):
    print('digital_ic_support.submitEclBtnClicked')

    # Clear existing output
    clearScrollText()

    # check if all required fields are filled
    ecl_params_filled = _w3.rb1_L.get() and _w3.rb1_H.get() \
                and _w3.rb1_L.get() and _w3.rb1_H.get() \
                and _w3.voh.get() and _w3.vol.get()

    if not reqFieldsFilled() or not ecl_params_filled:
        messagebox.showerror("Input Error", "Please fill all the required fields.")
        return
    
    _top3.withdraw()
    kpn = _w1.kpn.get()

    # Generate model
    print("[INFO] Generating model ...", flush=True)
    
    # Generating model based on user's inputs
    reg_model = lib_digital_ic.main_gen_ecl_model(pin_list=PIN_LIST, inputText=_w1.resultBox.get("1.0", tk.END), 
                                                  inputSubckts=getInputInterfaces(),
                                                  pVCC=_w1.vccPinNum.get(), pGND=_w1.gndPinNum.get(), kpn=kpn,
                                                  rawPinInfo=_w1.pinInfoText.get("1.0","end-1c"))

    print("[INFO] Generating model ... done", flush=True)

    # Append generated model to existing .inc file without overwriting data
    # Else create new .inc file if not exist
    model_file = "{}.inc".format(kpn)
    if os.path.exists(model_file):
        with open(model_file, "r") as f:
            lines = f.readlines()
        with open(model_file, "w") as f:
            for line in lines:
                if ".subckt" in line:
                    line = line.replace(line, reg_model)
                    f.write(line)
                    break
                f.write(line)
    else:
        with open(model_file, "w") as f:
            f.write(reg_model)


    # Generate harness
    print("[INFO] Generating harness ...", flush=True)
    reg_harness, _ = lib_digital_ic.gen_ecl_harness(kpn=kpn, pin_list=PIN_LIST, vcc=_w1.vcc.get(), vin=_w1.vin.get(), vee=_w1.vee.get(), vtt=_w1.vtt.get())

    with open("fixture.cki", "w") as f:
        f.write(reg_harness)
    print("[INFO] Generating harness ... done", flush=True)

    # Generate core.cmd
    print("[INFO] Generating core.cmd..", flush=True)
    delta = str(round((float(_w3.voh.get()) - float(_w3.vol.get()))*1000))
    com = str(round((float(_w3.voh.get()) + float(_w3.vol.get())) / 2, 2))
    reg_core_cmd = lib_digital_ic.gen_ecl_cmd(_w3.voh.get(), _w3.vol.get(), delta, com)
    
    with open("core.cmd", "w") as f:
        f.write(reg_core_cmd)
    print("[INFO] Generating core.cmd ... done", flush=True)
    
    print("Optimizing parameters. Please wait...", flush=True)
    optimizeECL.run_with_params(model_file, int(_w3.rb1_L.get()), int(_w3.rb1_H.get()),
                int(_w3.rb2_L.get()), int(_w3.rb2_H.get()),
                float(_w3.voh.get()), float(_w3.vol.get()))
    
    with open(model_file, "r") as f:
        reg_model = f.read()

    _w1.Scrolledtext1.configure(state='normal')
    _w1.Scrolledtext1.insert(tk.INSERT, reg_model)
    _w1.Scrolledtext1.insert(tk.INSERT, "\n\n*******************************************************************\n")
    _w1.Scrolledtext1.insert(tk.INSERT, "********************END OF MODEL BEGIN HARNESS *********************\n")
    _w1.Scrolledtext1.insert(tk.INSERT, "*******************************************************************\n\n")
    _w1.Scrolledtext1.insert(tk.INSERT, reg_harness)
    _w1.Scrolledtext1.insert(tk.INSERT, "\n\n*******************************************************************\n")
    _w1.Scrolledtext1.insert(tk.INSERT, "********************END OF HARNESS BEGIN CMD *********************\n")
    _w1.Scrolledtext1.insert(tk.INSERT, "*******************************************************************\n\n")
    _w1.Scrolledtext1.insert(tk.INSERT, reg_core_cmd)
    _w1.Scrolledtext1.configure(state='disabled')

    #print("[INFO] Generating stress.cmd ... done", flush=True)
    print("[INFO] ECL modelling completed", flush=True)
    

# ---------------------- CML Output model ----------------------
def createCmlBtnClicked(*args):
    if not checkPinInfo():
        messagebox.showerror("Input Error", "Please fill all the required fields.")
        return
    
    global _top4, _w4
    _top4 = tk.Toplevel(root)
    _w4 = digital_ic_gui.Toplevel4(_top4)

def submitCmlBtnClicked(*args):
    print('digital_ic_support.submitCmlBtnClicked')

    # Clear existing output
    clearScrollText()

    cml_params_filled = _w4.rb1_L.get() and _w4.rb1_H.get() \
                        and _w4.rb2_L.get() and _w4.rb2_H.get() \
                        and _w4.rb3_L.get() and _w4.rb3_H.get() \
                        and _w4.rb4_L.get() and _w4.rb4_H.get() \
                        and _w4.voh.get() and _w4.vol.get()


    if not reqFieldsFilled() or not cml_params_filled:
        messagebox.showerror("Input Error", "Please fill all the required fields.")
        return
    
    _top4.withdraw()

    kpn = _w1.kpn.get()

    # Generate model
    print("[INFO] Generating model ...", flush=True)
    reg_model = lib_digital_ic.main_gen_cml_model(pin_list=PIN_LIST, inputText=_w1.resultBox.get("1.0", tk.END),
                                                  inputSubckts=getInputInterfaces(),
                                                  pVCC=_w1.vccPinNum.get(), pGND=_w1.gndPinNum.get(), kpn=kpn,
                                                  rawPinInfo=_w1.pinInfoText.get("1.0","end-1c")) 

    print("[INFO] Generating model ... done", flush=True)

    # Append generated model to existing .inc file without overwriting data
    # Else create new .inc file if not exist
    model_file = '{}.inc'.format(kpn)
    if os.path.exists(model_file):
        with open(model_file, "r") as f:
            lines = f.readlines()
        with open(model_file, "w") as f:
            for line in lines:
                if ".subckt" in line:
                    line = line.replace(line, reg_model)
                    f.write(line)
                    break
                f.write(line)
    else:
        with open(model_file, 'w') as f:
            f.write(reg_model)


    # Generate harness
    print("[INFO] Generating harness ...", flush=True)
    reg_harness = lib_digital_ic.gen_cml_harness(kpn=kpn, pin_list=PIN_LIST, vcc=_w1.vcc.get(), vee=_w1.vee.get(), vin=_w1.vpos.get())
    

    # Open harness.cki file and write reg_harness into ds.cki
    with open("fixture.cki", "w") as f:
        f.write(reg_harness)
    print("[INFO] Generating harness ... done", flush=True)
    

    # Generate core.cmd
    print("[INFO] Generating core.cmd..", flush=True)
    delta = str(round((float(_w4.voh.get()) - float(_w4.vol.get()))*1000))
    com = str(round((float(_w4.voh.get()) + float(_w4.vol.get())) / 2, 2))
    reg_core_cmd = lib_digital_ic.gen_cml_cmd(_w4.voh.get(), _w4.vol.get(), delta, com)
    
    
    # create core.cmd and write reg_core_cmd into cmd
    with open("core.cmd", "w") as f:
        f.write(reg_core_cmd)
    print("[INFO] Generating core.cmd ... done", flush=True)
    
    print("Optimizing parameters. Please wait...", flush=True)
    optimizeCML.run_with_params(model_file, int(_w4.rb1_L.get()), int(_w4.rb1_H.get()),
                                int(_w4.rb2_L.get()), int(_w4.rb2_H.get()),
                                int(_w4.rb3_L.get()), int(_w4.rb3_H.get()),
                                int(_w4.rb4_L.get()), int(_w4.rb4_H.get()),
                                float(_w4.voh.get()), float(_w4.vol.get()))

    _w1.Scrolledtext1.configure(state='normal')
    _w1.Scrolledtext1.insert(tk.INSERT, reg_model)
    _w1.Scrolledtext1.insert(tk.INSERT, "\n\n*******************************************************************\n")
    _w1.Scrolledtext1.insert(tk.INSERT, "********************END OF MODEL BEGIN HARNESS *********************\n")
    _w1.Scrolledtext1.insert(tk.INSERT, "*******************************************************************\n\n")
    _w1.Scrolledtext1.insert(tk.INSERT, reg_harness)
    _w1.Scrolledtext1.insert(tk.INSERT, "\n\n*******************************************************************\n")
    _w1.Scrolledtext1.insert(tk.INSERT, "********************END OF HARNESS BEGIN CMD *********************\n")
    _w1.Scrolledtext1.insert(tk.INSERT, "*******************************************************************\n\n")
    _w1.Scrolledtext1.insert(tk.INSERT, reg_core_cmd)
    _w1.Scrolledtext1.configure(state='disabled')
    
    print("[INFO] CML modelling completed", flush=True)
    

def loadPinBtnClicked(*args):
    print('digital_ic_support.loadPinBtnClicked')
    '''
    Method to load pin information from textbox(UI).
    '''
    try:
        # Check if the list is filled or empty
        pininfo = _w1.pinInfoText.get("1.0","end-1c")
        if pininfo:
            global PIN_LIST
            #pininfo = _w1.pinInfoText.get("1.0","end-1c")
            pininfo = pininfo.splitlines()
            pin = []
            pin_count = 0
            for x in pininfo:
                temp = x.split()
                if temp[1].isnumeric() or "%" in temp[1]:
                    pin.append([temp[1],temp[2]])
                    pin_count += 1
            PIN_LIST[:] = list(pin)
            
            # Rename pins with same name
            pin_names=[item[1] for item in PIN_LIST]
            pin_nums=[item[0] for item in PIN_LIST]
            p_lst_dups = set()
            PIN_LIST = []
            for i in range(pin_count):
                count = pin_names.count(pin_names[i])
                if count > 1:
                    p_lst_dups.add(pin_names[i])
                    pin_names[i] = pin_names[i]+"_"+str(count)
                elif pin_names[i] in p_lst_dups:
                    pin_names[i] = pin_names[i]+"_1"
                PIN_LIST.append([pin_nums[i], pin_names[i]])
                pin_names[i] = ''
                pin_nums[i] = ''
            # PIN_LIST.reverse()

            updatePinList()
            clrList()
            _w1.pinNum.set('''Number of Pins : '''+str(pin_count)) 

            # set vcc and gnd pins once
            vccPinSet = False
            gndPinSet = False
            for pin in PIN_LIST:
                if not vccPinSet and "vcc" in pin[1].lower():
                    _w1.vccPinNum.set(pin[0])
                    vccPinSet = True
                elif not gndPinSet and ("gnd" in pin[1].lower() or "vee" in pin[1].lower()):
                    _w1.gndPinNum.set(pin[0])
                    gndPinSet = True
        else:
            messagebox.showerror("Input Error", "Either Input Pin Information is empty or first line in the box is empty.")
            
    except Exception as e:
        print("Error in assigning: ",e)

    sys.stdout.flush()
            

def updatePinList():
    '''
    Method to load given list into Listbox.
    '''
    try:
        _w1.Listbox1.delete(0,'end')
        for i in range(len(PIN_LIST)):
            _w1.Listbox1.insert(i+1, ' '.join(PIN_LIST[i]))
    except Exception as e:
        print("Error in updating Listbox: ",e)

def clrList():
    '''
    Method to clear all selection in list.
    '''
    global sel_pin_list
    _w1.Listbox1.selection_clear(0, tk.END)
    sel_pin_list = []


def resetBtnClicked(*args):
    print('digital_ic_support.resetBtnClicked')
    clearPinInfo()
    resultBoxClearBtnClicked()
    clearScrollText()
    sys.stdout.flush()

def clearPinInfo():
    _w1.vccPinEntry.delete(0, tk.END)
    _w1.gndPinEntry.delete(0, tk.END)
    _w1.kpn.set('')
    _w1.posPinNum.set('')
    _w1.negPinNum.set('')
    _w1.vcc.set('')
    _w1.vin.set('')
    _w1.vee.set('')
    _w1.vtt.set('')

def clearScrollText():
    _w1.Scrolledtext1.configure(state='normal')
    _w1.Scrolledtext1.delete("1.0", tk.END)
    _w1.Scrolledtext1.configure(state='disabled')

def reqFieldsFilled():
    return _w1.vccPinNum.get() and _w1.gndPinNum.get() and _w1.kpn.get()

def checkPinInfo():
    if not _w1.vee.get():
        _w1.vee.set("0")
    if not _w1.vin.get():
        _w1.vin.set("0")
    return _w1.vcc.get() and _w1.vtt.get()

def getInputInterfaces():
    lst = []
    txt = _w1.resultBox.get("1.0", tk.END)
    if "RIN" in txt: lst.append("LVDS")
    if "ecl" in txt: lst.append("ECL")
    if "cml" in txt: lst.append("CML")
    return lst

if __name__ == '__main__':
    digital_ic_gui.start()
