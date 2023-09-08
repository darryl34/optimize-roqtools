#! /usr/bin/env python
# -*- coding: utf-8 -*-
# *************************************************************************************
# Digital IC model generator with optimized parameters (UI frontend)
# Script version: 2.0
# Python version: Python 3.8.10
# Compatible OS: Windows 10
# Requirements: Tkinter, pyperclip, Hpspice, digital_ic_support.py
# Developer (v2.0): Darryl Ng
# Notes:
#     This is a script to create and maintain a GUI for generating
#           Digital IC models.
#   Command: python3 digital_ic_gui.py
#
# Version doc:
#  * First version
# *************************************************************************************
#  * Version 2.0
#  * 1. Improved and simplified modelling process
#  * 1. Added LVDS, ECL, CML Input Interface with manual editing functionality
#  * 2. Improved harness configuration page
#  * 3. Incorporated ML parameter optimization with page to set bounds and ideal values
#  * 4. Each widget follows a defined style, previously each widget was configured individually
# *************************************************************************************
#
# Future improvements:
# * 1. Use multithreading to run process in background and GUI will not freeze
# * 2. Make GUI widgets responsive to window resizing
#

import sys
import tkinter as tk
import tkinter.ttk as ttk

import digital_ic_support


# Class for configuring and styling GUI widgets
class GUIStyles:
    def __init__(self, window_to_style):
        window_to_style.style = ttk.Style()
        if sys.platform == "win32":
            window_to_style.style.theme_use('winnative')

        window_to_style.style.configure('label.TLabel', 
                                activebackground="#f9f9f9",
                                anchor='w',
                                background="#d9d9d9",
                                disabledforeground="#a3a3a3",
                                foreground="#000000",
                                highlightbackground="#d9d9d9",
                                highlightcolor="black")
        window_to_style.style.configure('entry.TEntry',
                                        background="white",
                                        disabledforeground="#a3a3a3",
                                        font="TkFixedFont",
                                        foreground="#000000",
                                        highlightbackground="#d9d9d9",
                                        highlightcolor="black",
                                        insertbackground="black",
                                        selectbackground="#c4c4c4",
                                        selectforeground="black")
        window_to_style.style.configure('button.TButton',
                                        activebackground="beige",
                                        activeforeground="#000000",
                                        background="#d9d9d9",
                                        compound='left',
                                        disabledforeground="#a3a3a3",
                                        foreground="#000000",
                                        highlightbackground="#d9d9d9",
                                        highlightcolor="black",
                                        pady="0",
                                        takefocus=False)
        window_to_style.style.configure('labelFrame.TLabelframe',
                                        background="#d9d9d9",
                                        foreground="#000000",
                                        font="-family {Segoe UI} -size 12",
                                        highlightbackground="#d9d9d9",
                                        highlightcolor="black",
                                        relief='groove')
        window_to_style.style.configure('checkbutton.TCheckbutton',
                                        background="#d9d9d9",
                                        foreground="#000000",
                                        highlightbackground="#d9d9d9",
                                        highlightcolor="black",
                                        takefocus=False)

# Main GUI class
class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = 'gray40' # X11 color: #666666
        _ana1color = '#c3c3c3' # Closest X11 color: 'gray76'
        _ana2color = 'beige' # X11 color: #f5f5dc
        _tabfg1 = 'black' 
        _tabfg2 = 'black' 
        _tabbg1 = 'grey75' 
        _tabbg2 = 'grey89' 
        _bgmode = 'light'
        GUIStyles(window_to_style=self)
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        #top.geometry("1344x866+106+11")
        top.geometry("1344x866+106+20")
        top.minsize(120, 1)
        top.maxsize(3460, 1061)
        top.resizable(1,  1)
        top.title("LVDS/ECL/CML")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.top = top
        self.pinNum = tk.StringVar()
        self.gndPinNum = tk.StringVar()
        self.vccPinNum = tk.StringVar()
        self.posPinNum = tk.StringVar()
        self.negPinNum = tk.StringVar()
        self.inputInterfaceOption = tk.StringVar()
        self.kpn = tk.StringVar()
        self.vcc = tk.StringVar()
        self.vin = tk.StringVar()
        self.vee = tk.StringVar()
        self.vtt = tk.StringVar()
        self.lvdsSubckt = tk.IntVar()
        self.eclSubckt = tk.IntVar()
        self.cmlSubckt = tk.IntVar()
        

        self.Labelframe1 = ttk.LabelFrame(self.top, style='labelFrame.TLabelframe')
        self.Labelframe1.place(relx=0.025, rely=0.025, relheight=0.95, relwidth=0.15)
        self.Labelframe1.configure(text='''Input Pin Information''')

        self.pinInfoText = tk.Text(self.Labelframe1)
        self.pinInfoText.place(relx=0.040, rely=0.035, relheight=0.85, relwidth=0.9, bordermode='ignore')
        self.pinInfoText.configure(background="white")
        self.pinInfoText.configure(borderwidth="2")
        self.pinInfoText.configure(font="TkTextFont")
        self.pinInfoText.configure(foreground="black")
        self.pinInfoText.configure(highlightbackground="#d9d9d9")
        self.pinInfoText.configure(highlightcolor="black")
        self.pinInfoText.configure(insertbackground="black")
        self.pinInfoText.configure(selectbackground="#c4c4c4")
        self.pinInfoText.configure(selectforeground="black")
        self.pinInfoText.configure(wrap="word")

        self.loadPinBtn = ttk.Button(self.Labelframe1, style="button.TButton", takefocus=False)
        self.loadPinBtn.place(relx=0.35, rely=0.9, height=34, width=108
                , bordermode='ignore')
        self.loadPinBtn.configure(text='''Load Pins''')
        self.loadPinBtn.bind('<Button-1>',lambda e:digital_ic_support.loadPinBtnClicked(e))
        self.loadPinBtn.bind('<Return>',lambda e:digital_ic_support.loadPinBtnClicked(e))

        self.pinNumLabel = ttk.Label(self.Labelframe1, style='label.TLabel')
        self.pinNumLabel.place(relx=0.35, rely=0.95, height=18, width=120
                , bordermode='ignore')
        self.pinNumLabel.configure(compound='left')
        self.pinNumLabel.configure(font="-family {Segoe UI} -size 9 -slant italic")
        self.pinNumLabel.configure(text='''Number of Pins :''')
        self.pinNumLabel.configure(textvariable=self.pinNum)

        self.Labelframe2 = ttk.LabelFrame(self.top, style='labelFrame.TLabelframe')
        self.Labelframe2.place(relx=0.18, rely=0.025, relheight=0.95
                , relwidth=0.5)
        self.Labelframe2.configure(text='''Input Model Information''')

        self.Listbox1 = tk.Listbox(self.Labelframe2)
        self.Listbox1.place(relx=0.040, rely=0.035, relheight=0.95
                , relwidth=0.25, bordermode='ignore')
        self.Listbox1.configure(background="#d9d9d9")
        self.Listbox1.configure(disabledforeground="#a3a3a3")
        self.Listbox1.configure(font="TkFixedFont")
        self.Listbox1.configure(foreground="#000000")
        self.Listbox1.configure(highlightbackground="#d9d9d9")
        self.Listbox1.configure(highlightcolor="black")
        self.Listbox1.configure(selectbackground="#c4c4c4")
        self.Listbox1.configure(selectforeground="black")
        
        # Pin labels and entries configuration
        self.vccPinLabel = ttk.Label(self.Labelframe2, style='label.TLabel')
        self.vccPinLabel.place(relx=0.30, rely=0.03, height=32, width=170, bordermode='ignore')
        self.vccPinLabel.configure(text='''*VCC pin number :''')
        self.vccPinEntry = ttk.Entry(self.Labelframe2, style='entry.TEntry', textvariable=self.vccPinNum)
        self.vccPinEntry.place(relx=0.5, rely=0.035, height=25, relwidth=0.173, bordermode='ignore')
        
        self.gndPinLabel = ttk.Label(self.Labelframe2, style='label.TLabel')
        self.gndPinLabel.place(relx=0.30, rely=0.08, height=32, width=170, bordermode='ignore')
        self.gndPinLabel.configure(text='''*GND pin number :''')
        self.gndPinEntry = ttk.Entry(self.Labelframe2, style='entry.TEntry', textvariable=self.gndPinNum)
        self.gndPinEntry.place(relx=0.5, rely=0.085, height=25, relwidth=0.173, bordermode='ignore')
        
        self.kpnLabel = ttk.Label(self.Labelframe2, style='label.TLabel')
        self.kpnLabel.place(relx=0.70, rely=0.030, height=31, width=84, bordermode='ignore')
        self.kpnLabel.configure(text='''*KPN :''')
        self.kpnEntry = ttk.Entry(self.Labelframe2, style='entry.TEntry', textvariable=self.kpn)
        self.kpnEntry.place(relx=0.78, rely=0.035, height=25, relwidth=0.173, bordermode='ignore')

        self.posLabel = ttk.Label(self.Labelframe2, style='label.TLabel')
        self.posLabel.place(relx=0.71, rely=0.08, height=31, width=84, bordermode='ignore')
        self.posLabel.configure(text='''POS :''')
        self.posEntry = ttk.Entry(self.Labelframe2, style='entry.TEntry', textvariable=self.posPinNum)
        self.posEntry.place(relx=0.77, rely=0.085, height=25, relwidth=0.05, bordermode='ignore')

        self.negLabel = ttk.Label(self.Labelframe2, style='label.TLabel')
        self.negLabel.place(relx=0.84, rely=0.08, height=31, width=84, bordermode='ignore')
        self.negLabel.configure(text='''NEG :''')
        self.negEntry = ttk.Entry(self.Labelframe2, style='entry.TEntry', textvariable=self.negPinNum)
        self.negEntry.place(relx=0.90, rely=0.085, height=25, relwidth=0.05, bordermode='ignore')

        self.Label = ttk.Label(self.Labelframe2, style='label.TLabel')
        self.Label.place(relx=0.30, rely=0.15, height=30, width=200, bordermode='ignore')
        self.Label.configure(text='''Input Interface''')

        self.inputInterface = ttk.Combobox(self.Labelframe2, textvariable=self.inputInterfaceOption, state='readonly', takefocus=False)
        self.inputInterface.place(relx=0.30, rely=0.20, relheight=0.03, relwidth=0.20, bordermode='ignore')
        self.inputInterface["values"] = ('NONE', 'LVDS', 'ECL', 'CML')
        self.inputInterface.current(0)
        self.inputInterface.bind('<<ComboboxSelected>>', self.Labelframe2.focus())

        self.inputInterfaceButton = ttk.Button(self.Labelframe2, style='button.TButton', takefocus=False)
        self.inputInterfaceButton.place(relx=0.54, rely=0.19, height=34, width=107, bordermode='ignore')
        self.inputInterfaceButton.configure(text='''Generate''')
        self.inputInterfaceButton.bind('<ButtonRelease-1>', lambda e:digital_ic_support.inputInterfaceButtonClicked(e))

        self.resultLabel = ttk.Label(self.Labelframe2, style='label.TLabel')
        self.resultLabel.place(relx=0.30, rely=0.25, height=30, width=200, bordermode='ignore')
        self.resultLabel.configure(text='''Result box''')

        self.resultBox = tk.Text(self.Labelframe2)
        self.resultBox.place(relx=0.30, rely=0.29, relheight=0.12, relwidth=0.47, bordermode='ignore')
        self.resultBox.configure(background="white")
        self.resultBox.configure(borderwidth="2")
        self.resultBox.configure(font="TkTextFont")
        self.resultBox.configure(foreground="black")
        self.resultBox.configure(highlightbackground="#d9d9d9")
        self.resultBox.configure(highlightcolor="black")
        self.resultBox.configure(insertbackground="black")
        self.resultBox.configure(selectbackground="#c4c4c4")
        self.resultBox.configure(selectforeground="black")

        self.resultBoxSaveBtn = ttk.Button(self.Labelframe2, style='button.TButton', takefocus=False)
        self.resultBoxSaveBtn.place(relx=0.8, rely=0.33, height=34, width=107, bordermode='ignore')
        self.resultBoxSaveBtn.configure(text='''Clear''')
        self.resultBoxSaveBtn.bind('<Button-1>', lambda e:digital_ic_support.resultBoxClearBtnClicked(e))

        self.Labelframe3 = ttk.LabelFrame(self.top, style='Labelframe.TLabelframe')
        self.Labelframe3.place(relx=0.33, rely=0.45, relheight=0.45, relwidth=0.34)
        self.Labelframe3.configure(text='''Harness Configuration''')

        self.vccLabel = ttk.Label(self.Labelframe3, style='label.TLabel')
        self.vccLabel.place(relx=0.05, rely=0.10, height=31, width=84, bordermode='ignore')
        self.vccLabel.configure(text='''*VCC (V):''')
        self.vccEntry = ttk.Entry(self.Labelframe3, style='entry.TEntry', textvariable=self.vcc)
        self.vccEntry.place(relx=0.30, rely=0.10, height=25, relwidth=0.173, bordermode='ignore')

        self.vposLabel = ttk.Label(self.Labelframe3, style='label.TLabel')
        self.vposLabel.place(relx=0.05, rely=0.20, height=31, width=90, bordermode='ignore')
        self.vposLabel.configure(text='''VIN / V_POS (V):''')
        self.vposEntry = ttk.Entry(self.Labelframe3, style='entry.TEntry', textvariable=self.vin)
        self.vposEntry.place(relx=0.30, rely=0.20, height=25, relwidth=0.173, bordermode='ignore')

        self.vnegLabel = ttk.Label(self.Labelframe3, style='label.TLabel')
        self.vnegLabel.place(relx=0.05, rely=0.30, height=31, width=90, bordermode='ignore')
        self.vnegLabel.configure(text='''VEE/ V_NEG (V):''')
        self.vnegEntry = ttk.Entry(self.Labelframe3, style='entry.TEntry', textvariable=self.vee)
        self.vnegEntry.place(relx=0.30, rely=0.30, height=25, relwidth=0.173, bordermode='ignore')

        self.vttLabel = ttk.Label(self.Labelframe3, style='label.TLabel')
        self.vttLabel.place(relx=0.05, rely=0.40, height=31, width=84, bordermode='ignore')
        self.vttLabel.configure(text='''VTT (V):''')
        self.vttEntry = ttk.Entry(self.Labelframe3, style='entry.TEntry', textvariable=self.vtt)
        self.vttEntry.place(relx=0.30, rely=0.40, height=25, relwidth=0.173, bordermode='ignore')

        self.createBtn = ttk.Button(self.Labelframe3, style='button.TButton', takefocus=False)
        self.createBtn.place(relx=0.65, rely=0.1, height=34, width=107, bordermode='ignore')
        self.createBtn.configure(text='''Generate None''')
        self.createBtn.bind('<ButtonRelease-1>', lambda e:digital_ic_support.createNoneBtnClicked(e))
        self.createBtn.bind('<Return>', lambda e:digital_ic_support.createNoneBtnClicked(e))

        self.createBtn = ttk.Button(self.Labelframe3, style='button.TButton', takefocus=False)
        self.createBtn.place(relx=0.65, rely=0.23, height=34, width=107, bordermode='ignore')
        self.createBtn.configure(text='''Generate LVDS''')
        self.createBtn.bind('<ButtonRelease-1>', lambda e:digital_ic_support.createLvdsBtnClicked(e))
        self.createBtn.bind('<Return>', lambda e:digital_ic_support.createLvdsBtnClicked(e))

        self.createBtn = ttk.Button(self.Labelframe3, style='button.TButton', takefocus=False)
        self.createBtn.place(relx=0.65, rely=0.36, height=34, width=107, bordermode='ignore')
        self.createBtn.configure(text='''Generate ECL''')
        self.createBtn.bind('<ButtonRelease-1>', lambda e:digital_ic_support.createEclBtnClicked(e))
        self.createBtn.bind('<Return>', lambda e:digital_ic_support.createEclBtnClicked(e))

        self.createBtn = ttk.Button(self.Labelframe3, style='button.TButton', takefocus=False)
        self.createBtn.place(relx=0.65, rely=0.49, height=34, width=107, bordermode='ignore')
        self.createBtn.configure(text='''Generate CML''')
        self.createBtn.bind('<ButtonRelease-1>', lambda e:digital_ic_support.createCmlBtnClicked(e))
        self.createBtn.bind('<Return>', lambda e:digital_ic_support.createCmlBtnClicked(e))

        self.resetBtn = ttk.Button(self.Labelframe3, style='button.TButton', takefocus=False)
        self.resetBtn.place(relx=0.6, rely=0.66, height=34, width=145, bordermode='ignore')
        self.resetBtn.configure(text='''Reset Settings''')
        self.resetBtn.bind('<Button-1>',lambda e:digital_ic_support.resetBtnClicked(e))
        self.resetBtn.bind('<Return>', lambda e:digital_ic_support.resetBtnClicked(e))

        self.Label1 = ttk.Label(self.Labelframe2, style='label.TLabel')
        self.Label1.place(relx=0.35, rely=0.93, height=21, width=75, bordermode='ignore')
        self.Label1.configure(text='''*required''')

        self.Labelframe4 = ttk.LabelFrame(self.top, style='labelframe.TLabelframe')
        self.Labelframe4.place(relx=0.68, rely=0.025, relheight=0.95, relwidth=0.32)
        self.Labelframe4.configure(text='''Result''')

        self.Scrolledtext1 = ScrolledText(self.Labelframe4)
        self.Scrolledtext1.place(relx=0.044, rely=0.037, relheight=0.889, relwidth=0.918, bordermode='ignore')
        self.Scrolledtext1.configure(background="white")
        self.Scrolledtext1.configure(font="TkTextFont")
        self.Scrolledtext1.configure(foreground="black")
        self.Scrolledtext1.configure(highlightbackground="#d9d9d9")
        self.Scrolledtext1.configure(highlightcolor="black")
        self.Scrolledtext1.configure(insertbackground="black")
        self.Scrolledtext1.configure(insertborderwidth="3")
        self.Scrolledtext1.configure(selectbackground="#c4c4c4")
        self.Scrolledtext1.configure(selectforeground="black")
        self.Scrolledtext1.configure(state='disabled')
        self.Scrolledtext1.configure(wrap="none")

        self.copyBtn = ttk.Button(self.Labelframe4, style='button.TButton', takefocus=False)
        self.copyBtn.place(relx=0.7, rely=0.939, height=34, width=97, bordermode='ignore')
        self.copyBtn.configure(text='''Copy''')
        self.copyBtn.bind('<Button-1>', lambda e:digital_ic_support.copyBtnClicked(e))
        self.copyBtn.bind('<Return>', lambda e:digital_ic_support.copyBtnClicked(e))


class Toplevel2:
    '''This class configures and populates the LVDS toplevel window.
        top is the toplevel containing window.'''
    def __init__(self, top=None):

        top.geometry("747x700+447+134")
        top.minsize(120, 1)
        top.maxsize(1540, 941)
        top.resizable(1,  1)
        top.title("LVDS bounds and ideal values")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        GUIStyles(window_to_style=self)
        self.style = ttk.Style()
        self.top = top
        self.mpd1_L = tk.StringVar(value='1e-6')
        self.mpd1_H = tk.StringVar(value='1e-3')
        self.mnd1_L = tk.StringVar(value='1e-6')
        self.mnd1_H = tk.StringVar(value='1e-3')
        self.pKp_L = tk.StringVar(value='1e-5')
        self.pKp_H = tk.StringVar(value='1e-3')
        self.pRd_L = tk.StringVar(value='1')
        self.pRd_H = tk.StringVar(value='50')
        self.pRs_L = tk.StringVar(value='1')
        self.pRs_H = tk.StringVar(value='50')
        self.nKp_L = tk.StringVar(value='1e-5')
        self.nKp_H = tk.StringVar(value='1e-3')
        self.nRd_L = tk.StringVar(value='1')
        self.nRd_H = tk.StringVar(value='50')
        self.nRs_L = tk.StringVar(value='1')
        self.nRs_H = tk.StringVar(value='50')
        self.voh = tk.StringVar()
        self.vol = tk.StringVar()

        self.labelFrame = ttk.LabelFrame(self.top, style='labelframe.TLabelframe')
        self.labelFrame.place(relx=0.039, rely=0.017, relheight=0.85, relwidth=0.912)        
        self.labelFrame.configure(text='''Input Model Information''')

        self.labelL = ttk.Label(self.labelFrame, style='label.TLabel')
        self.labelL.place(relx=0.23, rely=0.03, height=25, width=30, bordermode='ignore')
        self.labelL.configure(text='''Low''')

        self.labelH = ttk.Label(self.labelFrame, style='label.TLabel')
        self.labelH.place(relx=0.4, rely=0.03, height=25, width=30, bordermode='ignore')
        self.labelH.configure(text='''High''')

        # MPD1_W
        self.mpd1Label = ttk.Label(self.labelFrame, style='label.TLabel')
        self.mpd1Label.place(relx=0.03, rely=0.1, height=25, width=150, bordermode='ignore')
        self.mpd1Label.configure(text='''MPD1 W''')
        self.mpd1_L_Entry = ttk.Entry(self.labelFrame, textvariable=self.mpd1_L, style='entry.TEntry')
        self.mpd1_L_Entry.place(relx=0.18, rely=0.1, height=25, relwidth=0.15, bordermode='ignore')
        self.mpd1_H_Entry = ttk.Entry(self.labelFrame, textvariable=self.mpd1_H, style='entry.TEntry')
        self.mpd1_H_Entry.place(relx=0.35, rely=0.1, height=25, relwidth=0.15, bordermode='ignore')

        # MND1_W
        self.mnd1Label = ttk.Label(self.labelFrame, style='label.TLabel')
        self.mnd1Label.place(relx=0.03, rely=0.18, height=25, width=150, bordermode='ignore')
        self.mnd1Label.configure(text='''MND1 W''')
        self.mnd1_L_Entry = ttk.Entry(self.labelFrame, textvariable=self.mnd1_L, style='entry.TEntry')
        self.mnd1_L_Entry.place(relx=0.18, rely=0.18, height=25, relwidth=0.15, bordermode='ignore')
        self.mnd1_H_Entry = ttk.Entry(self.labelFrame, textvariable=self.mnd1_H, style='entry.TEntry')
        self.mnd1_H_Entry.place(relx=0.35, rely=0.18, height=25, relwidth=0.15, bordermode='ignore')

        # P_KP
        self.pKpLabel = ttk.Label(self.labelFrame, style='label.TLabel')
        self.pKpLabel.place(relx=0.03, rely=0.26, height=25, width=150, bordermode='ignore')
        self.pKpLabel.configure(text='''PMOS KP''')
        self.pKp_L_Entry = ttk.Entry(self.labelFrame, textvariable=self.pKp_L, style='entry.TEntry')
        self.pKp_L_Entry.place(relx=0.18, rely=0.26, height=25, relwidth=0.15, bordermode='ignore')
        self.pKp_H_Entry = ttk.Entry(self.labelFrame, textvariable=self.pKp_H, style='entry.TEntry')
        self.pKp_H_Entry.place(relx=0.35, rely=0.26, height=25, relwidth=0.15, bordermode='ignore')

        # P_RD
        self.pRdLabel = ttk.Label(self.labelFrame, style='label.TLabel')
        self.pRdLabel.place(relx=0.03, rely=0.34, height=25, width=150, bordermode='ignore')
        self.pRdLabel.configure(text='''PMOS RD''')
        self.pRd_L_Entry = ttk.Entry(self.labelFrame, textvariable=self.pRd_L, style='entry.TEntry')
        self.pRd_L_Entry.place(relx=0.18, rely=0.34, height=25, relwidth=0.15, bordermode='ignore')
        self.pRd_H_Entry = ttk.Entry(self.labelFrame, textvariable=self.pRd_H, style='entry.TEntry')
        self.pRd_H_Entry.place(relx=0.35, rely=0.34, height=25, relwidth=0.15, bordermode='ignore')

        # P_RS
        self.pRsLabel = ttk.Label(self.labelFrame, style='label.TLabel')
        self.pRsLabel.place(relx=0.03, rely=0.42, height=25, width=150, bordermode='ignore')
        self.pRsLabel.configure(text='''PMOS RS''')
        self.pRs_L_Entry = ttk.Entry(self.labelFrame, textvariable=self.pRs_L, style='entry.TEntry')
        self.pRs_L_Entry.place(relx=0.18, rely=0.42, height=25, relwidth=0.15, bordermode='ignore')
        self.pRs_H_Entry = ttk.Entry(self.labelFrame, textvariable=self.pRs_H, style='entry.TEntry')
        self.pRs_H_Entry.place(relx=0.35, rely=0.42, height=25, relwidth=0.15, bordermode='ignore')

        # N_KP
        self.nKpLabel = ttk.Label(self.labelFrame, style='label.TLabel')
        self.nKpLabel.place(relx=0.03, rely=0.5, height=25, width=150, bordermode='ignore')
        self.nKpLabel.configure(text='''NMOS KP''')
        self.nKp_L_Entry = ttk.Entry(self.labelFrame, textvariable=self.nKp_L, style='entry.TEntry')
        self.nKp_L_Entry.place(relx=0.18, rely=0.5, height=25, relwidth=0.15, bordermode='ignore')
        self.nKp_H_Entry = ttk.Entry(self.labelFrame, textvariable=self.nKp_H, style='entry.TEntry')
        self.nKp_H_Entry.place(relx=0.35, rely=0.5, height=25, relwidth=0.15, bordermode='ignore')

        # N_RD
        self.nRdLabel = ttk.Label(self.labelFrame, style='label.TLabel')
        self.nRdLabel.place(relx=0.03, rely=0.58, height=25, width=150, bordermode='ignore')
        self.nRdLabel.configure(text='''NMOS RD''')
        self.nRd_L_Entry = ttk.Entry(self.labelFrame, textvariable=self.nRd_L, style='entry.TEntry')
        self.nRd_L_Entry.place(relx=0.18, rely=0.58, height=25, relwidth=0.15, bordermode='ignore')
        self.nRd_H_Entry = ttk.Entry(self.labelFrame, textvariable=self.nRd_H, style='entry.TEntry')
        self.nRd_H_Entry.place(relx=0.35, rely=0.58, height=25, relwidth=0.15, bordermode='ignore')

        # N_RS
        self.nRsLabel = ttk.Label(self.labelFrame, style='label.TLabel')
        self.nRsLabel.place(relx=0.03, rely=0.66, height=25, width=150, bordermode='ignore')
        self.nRsLabel.configure(text='''NMOS RS''')
        self.nRs_L_Entry = ttk.Entry(self.labelFrame, textvariable=self.nRs_L, style='entry.TEntry')
        self.nRs_L_Entry.place(relx=0.18, rely=0.66, height=25, relwidth=0.15, bordermode='ignore')
        self.nRs_H_Entry = ttk.Entry(self.labelFrame, textvariable=self.nRs_H, style='entry.TEntry')
        self.nRs_H_Entry.place(relx=0.35, rely=0.66, height=25, relwidth=0.15, bordermode='ignore')

        # Ideal VOH
        self.vohLabel = ttk.Label(self.labelFrame, style='label.TLabel')
        self.vohLabel.place(relx=0.03, rely=0.76, height=25, width=150, bordermode='ignore')
        self.vohLabel.configure(text='''Ideal VOH''')
        self.vohEntry = ttk.Entry(self.labelFrame, textvariable=self.voh, style='entry.TEntry')
        self.vohEntry.place(relx=0.18, rely=0.76, height=25, relwidth=0.15, bordermode='ignore')

        # Ideal VOL
        self.volLabel = ttk.Label(self.labelFrame, style='label.TLabel')
        self.volLabel.place(relx=0.03, rely=0.84, height=25, width=150, bordermode='ignore')
        self.volLabel.configure(text='''Ideal VOL''')
        self.volEntry = ttk.Entry(self.labelFrame, textvariable=self.vol, style='entry.TEntry')
        self.volEntry.place(relx=0.18, rely=0.84, height=25, relwidth=0.15, bordermode='ignore')
    
        self.submitBtn = ttk.Button(self.top, style='TButton', command=lambda:digital_ic_support.submitLvdsBtnClicked())
        self.submitBtn.place(relx=0.656, rely=0.904, height=34, width=97)
        self.submitBtn.configure(text='''Submit''')

class Toplevel3:
    '''This class configures and populates the ECL toplevel window.
        top is the toplevel containing window.'''
    def __init__(self, top=None):

        top.geometry("747x700+447+134")
        top.minsize(120, 1)
        top.maxsize(1540, 941)
        top.resizable(1,  1)
        top.title("ECL bounds and ideal values")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        GUIStyles(window_to_style=self)
        self.style = ttk.Style()
        self.top = top
        self.rb1_L = tk.StringVar(value='1')
        self.rb1_H = tk.StringVar(value='1000')
        self.rb2_L = tk.StringVar(value='1')
        self.rb2_H = tk.StringVar(value='1000')
        self.voh = tk.StringVar()
        self.vol = tk.StringVar()


        self.Labelframe1 = ttk.LabelFrame(self.top, style='labelframe.TLabelframe')
        self.Labelframe1.place(relx=0.039, rely=0.017, relheight=0.85, relwidth=0.912) 
        self.Labelframe1.configure(text='''Input Model Information''')

        # RB1 LOW
        self.rb1Label = ttk.Label(self.Labelframe1, style='label.TLabel')
        self.rb1Label.place(relx=0.023, rely=0.109, height=25, width=215, bordermode='ignore')
        self.rb1Label.configure(text='''RB1 Low: ''')
        self.rb1Entry = ttk.Entry(self.Labelframe1, style='entry.TEntry', textvariable=self.rb1_L)
        self.rb1Entry.place(relx=0.253, rely=0.109, height=25, relwidth=0.20, bordermode='ignore')

        # RB1 HIGH
        self.rb1Label = ttk.Label(self.Labelframe1, style='label.TLabel')
        self.rb1Label.place(relx=0.023, rely=0.209, height=25, width=215, bordermode='ignore')
        self.rb1Label.configure(text='''RB1 High: ''')
        self.rb1Entry = ttk.Entry(self.Labelframe1, style='entry.TEntry', textvariable=self.rb1_H)
        self.rb1Entry.place(relx=0.253, rely=0.209, height=25, relwidth=0.20, bordermode='ignore')
        
        # RB2 LOW
        self.rb2Label = ttk.Label(self.Labelframe1, style='label.TLabel')
        self.rb2Label.place(relx=0.023, rely=0.309, height=25, width=215, bordermode='ignore')
        self.rb2Label.configure(text='''RB2 Low: ''')
        self.rb2Entry = ttk.Entry(self.Labelframe1, style='entry.TEntry', textvariable=self.rb2_L)
        self.rb2Entry.place(relx=0.253, rely=0.309, height=25, relwidth=0.20, bordermode='ignore')

        # RB2 HIGH
        self.rb2Label = ttk.Label(self.Labelframe1, style='label.TLabel')
        self.rb2Label.place(relx=0.023, rely=0.409, height=25, width=215, bordermode='ignore')
        self.rb2Label.configure(text='''RB2 High: ''')
        self.rb2Entry = ttk.Entry(self.Labelframe1, style='entry.TEntry', textvariable=self.rb2_H)
        self.rb2Entry.place(relx=0.253, rely=0.409, height=25, relwidth=0.20, bordermode='ignore')

        # Ideal VOH
        self.vohLabel = ttk.Label(self.Labelframe1, style='label.TLabel')
        self.vohLabel.place(relx=0.023, rely=0.509, height=25, width=215, bordermode='ignore')
        self.vohLabel.configure(text='''*Ideal VOH (V): ''')
        self.vohEntry = ttk.Entry(self.Labelframe1, style='entry.TEntry', textvariable=self.voh)
        self.vohEntry.place(relx=0.253, rely=0.509, height=25, relwidth=0.20, bordermode='ignore')

        # Ideal VOL
        self.volLabel = ttk.Label(self.Labelframe1, style='label.TLabel')
        self.volLabel.place(relx=0.023, rely=0.609, height=25, width=215, bordermode='ignore')
        self.volLabel.configure(text='''*Ideal VOL (V): ''')
        self.volEntry = ttk.Entry(self.Labelframe1, style='entry.TEntry', textvariable=self.vol)
        self.volEntry.place(relx=0.253, rely=0.609, height=25, relwidth=0.20, bordermode='ignore')

        self.submitBtn = ttk.Button(self.top, style='TButton', command=lambda:digital_ic_support.submitEclBtnClicked())
        self.submitBtn.place(relx=0.656, rely=0.904, height=34, width=97)
        self.submitBtn.configure(text='''Submit''')


class Toplevel4:
    '''This class configures and populates the CML toplevel window.
        top is the toplevel containing window.'''
    def __init__(self, top=None):

        top.geometry("747x700+447+134")
        top.minsize(120, 1)
        top.maxsize(1540, 941)
        top.resizable(1,  1)
        top.title("CML bounds and ideal values")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        GUIStyles(window_to_style=self)
        self.style = ttk.Style()
        self.top = top
        self.rb1_L = tk.StringVar(value='100')
        self.rb1_H = tk.StringVar(value='1000')
        self.rb2_L = tk.StringVar(value='100')
        self.rb2_H = tk.StringVar(value='1000')
        self.rb3_L = tk.StringVar(value='100')
        self.rb3_H = tk.StringVar(value='1000')
        self.rb4_L = tk.StringVar(value='100')
        self.rb4_H = tk.StringVar(value='1000')
        self.voh = tk.StringVar()
        self.vol = tk.StringVar()
        
        self.Labelframe1 = ttk.LabelFrame(self.top, style='labelframe.TLabelframe')
        self.Labelframe1.place(relx=0.039, rely=0.017, relheight=0.85, relwidth=0.912) 
        self.Labelframe1.configure(text='''Input Model Information''')

        # RB1 LOW
        self.rb1Label = ttk.Label(self.Labelframe1, style='label.TLabel')
        self.rb1Label.place(relx=0.023, rely=0.109, height=25, width=215, bordermode='ignore')
        self.rb1Label.configure(text='''RB1 Low: ''')
        self.rb1Entry = ttk.Entry(self.Labelframe1, style='entry.TEntry', textvariable=self.rb1_L)
        self.rb1Entry.place(relx=0.253, rely=0.109, height=25, relwidth=0.20, bordermode='ignore')

        # RB1 HIGH
        self.rb1Label = ttk.Label(self.Labelframe1, style='label.TLabel')
        self.rb1Label.place(relx=0.023, rely=0.209, height=25, width=215, bordermode='ignore')
        self.rb1Label.configure(text='''RB1 High: ''')
        self.rb1Entry = ttk.Entry(self.Labelframe1, style='entry.TEntry', textvariable=self.rb1_H)
        self.rb1Entry.place(relx=0.253, rely=0.209, height=25, relwidth=0.20, bordermode='ignore')
        
        # RB2 LOW
        self.rb2Label = ttk.Label(self.Labelframe1, style='label.TLabel')
        self.rb2Label.place(relx=0.023, rely=0.309, height=25, width=215, bordermode='ignore')
        self.rb2Label.configure(text='''RB2 Low: ''')
        self.rb2Entry = ttk.Entry(self.Labelframe1, style='entry.TEntry', textvariable=self.rb2_L)
        self.rb2Entry.place(relx=0.253, rely=0.309, height=25, relwidth=0.20, bordermode='ignore')

        # RB2 HIGH
        self.rb2Label = ttk.Label(self.Labelframe1, style='label.TLabel')
        self.rb2Label.place(relx=0.023, rely=0.409, height=25, width=215, bordermode='ignore')
        self.rb2Label.configure(text='''RB2 High: ''')
        self.rb2Entry = ttk.Entry(self.Labelframe1, style='entry.TEntry', textvariable=self.rb2_H)
        self.rb2Entry.place(relx=0.253, rely=0.409, height=25, relwidth=0.20, bordermode='ignore')

        # RB3 LOW
        self.rb3Label = ttk.Label(self.Labelframe1, style='label.TLabel')
        self.rb3Label.place(relx=0.623, rely=0.109, height=25, width=215, bordermode='ignore')
        self.rb3Label.configure(text='''RB3 Low: ''')
        self.rb3Entry = ttk.Entry(self.Labelframe1, style='entry.TEntry', textvariable=self.rb3_L)
        self.rb3Entry.place(relx=0.753, rely=0.109, height=25, relwidth=0.20, bordermode='ignore')

        # RB3 HIGH
        self.rb3Label = ttk.Label(self.Labelframe1, style='label.TLabel')
        self.rb3Label.place(relx=0.623, rely=0.209, height=25, width=215, bordermode='ignore')
        self.rb3Label.configure(text='''RB3 High: ''')
        self.rb3Entry = ttk.Entry(self.Labelframe1, style='entry.TEntry', textvariable=self.rb3_H)
        self.rb3Entry.place(relx=0.753, rely=0.209, height=25, relwidth=0.20, bordermode='ignore')

        # RB4 LOW
        self.rb4Label = ttk.Label(self.Labelframe1, style='label.TLabel')
        self.rb4Label.place(relx=0.623, rely=0.309, height=25, width=215, bordermode='ignore')
        self.rb4Label.configure(text='''RB4 Low: ''')
        self.rb4Entry = ttk.Entry(self.Labelframe1, style='entry.TEntry', textvariable=self.rb4_L)
        self.rb4Entry.place(relx=0.753, rely=0.309, height=25, relwidth=0.20, bordermode='ignore')

        # RB4 HIGH
        self.rb4Label = ttk.Label(self.Labelframe1, style='label.TLabel')
        self.rb4Label.place(relx=0.623, rely=0.409, height=25, width=215, bordermode='ignore')
        self.rb4Label.configure(text='''RB4 High: ''')
        self.rb4Entry = ttk.Entry(self.Labelframe1, style='entry.TEntry', textvariable=self.rb4_H)
        self.rb4Entry.place(relx=0.753, rely=0.409, height=25, relwidth=0.20, bordermode='ignore')

        # Ideal VOH
        self.vohLabel = ttk.Label(self.Labelframe1, style='label.TLabel')
        self.vohLabel.place(relx=0.023, rely=0.509, height=25, width=215, bordermode='ignore')
        self.vohLabel.configure(text='''*Ideal VOH (V): ''')
        self.vohEntry = ttk.Entry(self.Labelframe1, style='entry.TEntry', textvariable=self.voh)
        self.vohEntry.place(relx=0.253, rely=0.509, height=25, relwidth=0.20, bordermode='ignore')

        # Ideal VOL
        self.volLabel = ttk.Label(self.Labelframe1, style='label.TLabel')
        self.volLabel.place(relx=0.023, rely=0.609, height=25, width=215, bordermode='ignore')
        self.volLabel.configure(text='''*Ideal VOL (V): ''')
        self.volEntry = ttk.Entry(self.Labelframe1, style='entry.TEntry', textvariable=self.vol)
        self.volEntry.place(relx=0.253, rely=0.609, height=25, relwidth=0.20, bordermode='ignore')

        self.submitBtn = ttk.Button(self.top, style='TButton', command=lambda:digital_ic_support.submitCmlBtnClicked())
        self.submitBtn.place(relx=0.656, rely=0.904, height=34, width=97)
        self.submitBtn.configure(text='''Submit''')


# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''
    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))
        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        # Copy geometry methods of master  (taken from ScrolledText.py)
        methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                  | tk.Place.__dict__.keys()
        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped

class ScrolledText(AutoScroll, tk.Text):
    '''A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        tk.Text.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

import platform
def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))

def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')

def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1*int(event.delta/120),'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1*int(event.delta),'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')

def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')

def start():
    digital_ic_support.main()

if __name__ == '__main__':
    start()
