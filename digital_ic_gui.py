    #! /usr/bin/env python
# *************************************************************************************
# Hpspice regulator model generator (UI frontend)
# Script version: 1.0
# Python version: Python 3.6.5
# Compatible OS: Windows 10
# Requirements: Tkinter, pyperclip, Hpspice, lib_digital_ic(v1.0)
# Developer (v1.0): Corena Tong (listong)
# Notes:
#     This is a script to create and maintain a UI for generating
#        regulator (fixed/adjustable) models.
#   Command: python3 regulator_gui.py
# Version doc:
#  * First version
# *************************************************************************************
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 7.4
#  in conjunction with Tcl version 8.6
#    Jun 14, 2022 08:44:38 AM CST  platform: Windows NT

import sys
import tkinter as tk
import tkinter.ttk as ttk

import digital_ic_support

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
        self.veePinNum = tk.StringVar()
        self.vbbPinNum = tk.StringVar()
        self.inselPinNum = tk.StringVar()
        self.refPinNum = tk.StringVar()
        self.vtrPinNum = tk.StringVar()
        self.kpn = tk.StringVar()
        self.vcc = tk.StringVar()
        self.vpos = tk.StringVar()
        self.vneg = tk.StringVar()
        self.vee = tk.StringVar()
        self.vtt = tk.StringVar()
        
        self.chkgensetup = tk.IntVar()

        # Widget styles
        self.pinLabelStyle = ttk.Style()
        self.pinLabelStyle.configure('pinLabel.TLabel', 
                                     activebackground="#f9f9f9",
                                     anchor='w',
                                     background="#d9d9d9",
                                     disabledforeground="#a3a3a3",
                                     foreground="#000000",
                                     highlightbackground="#d9d9d9",
                                     highlightcolor="black")
        
        self.pinEntryStyle = ttk.Style()
        self.pinEntryStyle.configure('pinEntry.TEntry',
                                     background="white",
                                     disabledforeground="#a3a3a3",
                                     font="TkFixedFont",
                                     foreground="#000000",
                                     highlightbackground="#d9d9d9",
                                     highlightcolor="black",
                                     insertbackground="black",
                                     selectbackground="#c4c4c4",
                                     selectforeground="black")
        
        self.topLvlBtnStyle = ttk.Style()
        self.topLvlBtnStyle.configure('topLvlBtn.TButton',
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

        self.Labelframe1 = tk.LabelFrame(self.top)
        self.Labelframe1.place(relx=0.025, rely=0.025, relheight=0.95
                , relwidth=0.15)
        self.Labelframe1.configure(relief='groove')
        self.Labelframe1.configure(font="-family {Segoe UI} -size 12")
        self.Labelframe1.configure(foreground="#000000")
        self.Labelframe1.configure(text='''Input Pin Information''')
        self.Labelframe1.configure(background="#d9d9d9")
        self.Labelframe1.configure(highlightbackground="#d9d9d9")
        self.Labelframe1.configure(highlightcolor="black")

        self.pinInfoText = tk.Text(self.Labelframe1)
        self.pinInfoText.place(relx=0.040, rely=0.035, relheight=0.85
                , relwidth=0.9, bordermode='ignore')
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

        self.loadPinBtn = ttk.Button(self.Labelframe1, style="topLvlBtn.TButton", takefocus=False)
        self.loadPinBtn.place(relx=0.35, rely=0.9, height=34, width=108
                , bordermode='ignore')
        self.loadPinBtn.configure(text='''Load Pins''')
        self.loadPinBtn.bind('<Button-1>',lambda e:digital_ic_support.loadPinBtnClicked(e))
        self.loadPinBtn.bind('<Return>',lambda e:digital_ic_support.loadPinBtnClicked(e))

        self.pinNumLabel = tk.Label(self.Labelframe1)
        self.pinNumLabel.place(relx=0.35, rely=0.95, height=18, width=120
                , bordermode='ignore')
        self.pinNumLabel.configure(activebackground="#f9f9f9")
        self.pinNumLabel.configure(anchor='w')
        self.pinNumLabel.configure(background="#d9d9d9")
        self.pinNumLabel.configure(compound='left')
        self.pinNumLabel.configure(disabledforeground="#a3a3a3")
        self.pinNumLabel.configure(font="-family {Segoe UI} -size 9 -slant italic")
        self.pinNumLabel.configure(foreground="#000000")
        self.pinNumLabel.configure(highlightbackground="#d9d9d9")
        self.pinNumLabel.configure(highlightcolor="black")
        self.pinNumLabel.configure(text='''Number of Pins :''')
        self.pinNumLabel.configure(textvariable=self.pinNum)
        self.pinNum.set('''Number of Pins :''')

        self.Labelframe2 = tk.LabelFrame(self.top)
        self.Labelframe2.place(relx=0.18, rely=0.025, relheight=0.95
                , relwidth=0.5)
        self.Labelframe2.configure(relief='groove')
        self.Labelframe2.configure(font="-family {Segoe UI} -size 12")
        self.Labelframe2.configure(foreground="#000000")
        self.Labelframe2.configure(text='''Input Model Information''')
        self.Labelframe2.configure(background="#d9d9d9")
        self.Labelframe2.configure(highlightbackground="#d9d9d9")
        self.Labelframe2.configure(highlightcolor="black")

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
        self.vccPinLabel = ttk.Label(self.Labelframe2, style='pinLabel.TLabel')
        self.vccPinLabel.place(relx=0.30, rely=0.03, height=32, width=170
                , bordermode='ignore')
        self.vccPinLabel.configure(text='''*VCC pin number :''')

        self.vccPinEntry = ttk.Entry(self.Labelframe2, style='pinEntry.TEntry')
        self.vccPinEntry.place(relx=0.5, rely=0.035, height=25, relwidth=0.173
                , bordermode='ignore')
        self.vccPinEntry.configure(textvariable=self.vccPinNum)
        
        self.gndPinLabel = ttk.Label(self.Labelframe2, style='pinLabel.TLabel')
        self.gndPinLabel.place(relx=0.30, rely=0.08, height=32, width=170
                , bordermode='ignore')
        self.gndPinLabel.configure(text='''*GND pin number :''')

        self.gndPinEntry = ttk.Entry(self.Labelframe2, style='pinEntry.TEntry')
        self.gndPinEntry.place(relx=0.5, rely=0.085, height=25, relwidth=0.173
                , bordermode='ignore')
        self.gndPinEntry.configure(textvariable=self.gndPinNum)
        
        self.veePinLabel = ttk.Label(self.Labelframe2, style='pinLabel.TLabel')
        self.veePinLabel.place(relx=0.30, rely=0.13, height=32, width=170
                , bordermode='ignore')
        self.veePinLabel.configure(text='''VEE pin number :''')

        self.veePinEntry = ttk.Entry(self.Labelframe2, style='pinEntry.TEntry')
        self.veePinEntry.place(relx=0.5, rely=0.135, height=25, relwidth=0.173
                , bordermode='ignore')
        self.veePinEntry.configure(textvariable=self.veePinNum)
        
        self.inselPinLabel = ttk.Label(self.Labelframe2, style='pinLabel.TLabel')
        self.inselPinLabel.place(relx=0.30, rely=0.18, height=32, width=170
                , bordermode='ignore')
        self.inselPinLabel.configure(text='''IN SEL pin number :''')

        self.inselPinEntry = ttk.Entry(self.Labelframe2, style='pinEntry.TEntry')
        self.inselPinEntry.place(relx=0.5, rely=0.185, height=25, relwidth=0.173
                , bordermode='ignore')
        self.inselPinEntry.configure(textvariable=self.inselPinNum)
        
        self.refPinLabel = ttk.Label(self.Labelframe2, style='pinLabel.TLabel')
        self.refPinLabel.place(relx=0.30, rely=0.23, height=32, width=170
                , bordermode='ignore')
        self.refPinLabel.configure(text='''VAC_REF pin number :''')

        self.refPinEntry = ttk.Entry(self.Labelframe2, style='pinEntry.TEntry')
        self.refPinEntry.place(relx=0.5, rely=0.235, height=25, relwidth=0.173
                , bordermode='ignore')
        self.refPinEntry.configure(textvariable=self.refPinNum)
        
        self.vbbPinLabel = ttk.Label(self.Labelframe2, style='pinLabel.TLabel')
        self.vbbPinLabel.place(relx=0.30, rely=0.28, height=32, width=170
                , bordermode='ignore')
        self.vbbPinLabel.configure(text='''VBB pin number :''')

        self.vbbPinEntry = ttk.Entry(self.Labelframe2, style='pinEntry.TEntry')
        self.vbbPinEntry.place(relx=0.5, rely=0.285, height=25, relwidth=0.173
                , bordermode='ignore')
        self.vbbPinEntry.configure(textvariable=self.vbbPinNum)
        
        self.vtrPinLabel = ttk.Label(self.Labelframe2, style='pinLabel.TLabel')
        self.vtrPinLabel.place(relx=0.30, rely=0.33, height=32, width=170
                , bordermode='ignore')
        self.vtrPinLabel.configure(text='''VTR pin number :''')

        self.vtrPinEntry = ttk.Entry(self.Labelframe2, style='pinEntry.TEntry')
        self.vtrPinEntry.place(relx=0.5, rely=0.335, height=25, relwidth=0.173
                , bordermode='ignore')
        self.vtrPinEntry.configure(textvariable=self.vtrPinNum)
        
        self.kpnLabel = ttk.Label(self.Labelframe2, style='pinLabel.TLabel')
        self.kpnLabel.place(relx=0.70, rely=0.030, height=31, width=84
                , bordermode='ignore')
        self.kpnLabel.configure(text='''*KPN :''')

        self.kpnEntry = ttk.Entry(self.Labelframe2, style='pinEntry.TEntry')
        self.kpnEntry.place(relx=0.78, rely=0.035, height=25, relwidth=0.173
                , bordermode='ignore')
        self.kpnEntry.configure(textvariable=self.kpn)

        self.Labelframe3 = tk.LabelFrame(self.top)
        self.Labelframe3.place(relx=0.33, rely=0.4, relheight=0.5
                , relwidth=0.34)
        self.Labelframe3.configure(relief='groove')
        self.Labelframe3.configure(font="-family {Segoe UI} -size 12")
        self.Labelframe3.configure(foreground="#000000")
        self.Labelframe3.configure(text='''Harness Configuration''')
        self.Labelframe3.configure(background="#d9d9d9")
        self.Labelframe3.configure(highlightbackground="#d9d9d9")
        self.Labelframe3.configure(highlightcolor="black")

        self.vccLabel = ttk.Label(self.Labelframe3, style='pinLabel.TLabel')
        self.vccLabel.place(relx=0.10, rely=0.10, height=31, width=84
                , bordermode='ignore')
        self.vccLabel.configure(text='''*VCC (V):''')

        self.vccEntry = ttk.Entry(self.Labelframe3, style='pinEntry.TEntry')
        self.vccEntry.place(relx=0.30, rely=0.10, height=25, relwidth=0.173
                , bordermode='ignore')
        self.vccEntry.configure(textvariable=self.vcc)

        self.vposLabel = ttk.Label(self.Labelframe3, style='pinLabel.TLabel')
        self.vposLabel.place(relx=0.10, rely=0.20, height=31, width=84, bordermode='ignore')
        self.vposLabel.configure(text='''VIN / V_POS (V):''')

        self.vposEntry = ttk.Entry(self.Labelframe3, style='pinEntry.TEntry')
        self.vposEntry.place(relx=0.30, rely=0.20, height=25, relwidth=0.173, bordermode='ignore')
        self.vposEntry.configure(textvariable=self.vpos)

        self.vnegLabel = ttk.Label(self.Labelframe3, style='pinLabel.TLabel')
        self.vnegLabel.place(relx=0.10, rely=0.30, height=31, width=84, bordermode='ignore')
        self.vnegLabel.configure(text='''V_NEG (V):''')

        self.vnegEntry = ttk.Entry(self.Labelframe3, style='pinEntry.TEntry')
        self.vnegEntry.place(relx=0.30, rely=0.30, height=25, relwidth=0.173, bordermode='ignore')
        self.vnegEntry.configure(textvariable=self.vneg)

        self.veeLabel = ttk.Label(self.Labelframe3, style='pinLabel.TLabel')
        self.veeLabel.place(relx=0.10, rely=0.40, height=31, width=84, bordermode='ignore')
        self.veeLabel.configure(text='''VEE (V):''')

        self.veeEntry = ttk.Entry(self.Labelframe3, style='pinEntry.TEntry')
        self.veeEntry.place(relx=0.30, rely=0.40, height=25, relwidth=0.173, bordermode='ignore')
        self.veeEntry.configure(textvariable=self.vee)

        self.vttLabel = ttk.Label(self.Labelframe3, style='pinLabel.TLabel')
        self.vttLabel.place(relx=0.10, rely=0.50, height=31, width=84, bordermode='ignore')
        self.vttLabel.configure(text='''VT (V):''')

        self.vttEntry = ttk.Entry(self.Labelframe3, style='pinEntry.TEntry')
        self.vttEntry.place(relx=0.30, rely=0.50, height=25, relwidth=0.173, bordermode='ignore')
        self.vttEntry.configure(textvariable=self.vtt)

        self.Label = ttk.Label(self.Labelframe3, style='pinLabel.TLabel')
        self.Label.place(relx=0.55, rely=0.04, height=31, width=200, bordermode='ignore')
        self.Label.configure(compound='left')
        self.Label.configure(text='''Please Key in Harness Configuration''')

        self.Labe2 = ttk.Label(self.Labelframe3, style='pinLabel.TLabel')
        self.Labe2.place(relx=0.55, rely=0.09, height=31, width=200, bordermode='ignore')
        self.Labe2.configure(compound='left')
        self.Labe2.configure(text='''before click on the button below: ''')

        self.createBtn = ttk.Button(self.Labelframe3, style='topLvlBtn.TButton', takefocus=False)
        self.createBtn.place(relx=0.65, rely=0.165, height=34, width=107, bordermode='ignore')
        self.createBtn.configure(text='''Generate LVDS''')
        self.createBtn.bind('<Button-1>', lambda e:digital_ic_support.submitLvdsBtnClicked(e))
        self.createBtn.bind('<Return>', lambda e:digital_ic_support.submitLvdsBtnClicked(e))

        self.createBtn = ttk.Button(self.Labelframe3, style='topLvlBtn.TButton', takefocus=False)
        self.createBtn.place(relx=0.65, rely=0.265, height=34, width=107, bordermode='ignore')
        self.createBtn.configure(text='''Generate ECL''')
        self.createBtn.bind('<Button-1>', lambda e:digital_ic_support.submitEclBtnClicked(e))
        self.createBtn.bind('<Return>', lambda e:digital_ic_support.submitEclBtnClicked(e))

        self.createBtn = ttk.Button(self.Labelframe3, style='topLvlBtn.TButton', takefocus=False)
        self.createBtn.place(relx=0.65, rely=0.365, height=34, width=107, bordermode='ignore')
        self.createBtn.configure(text='''Generate CML''')
        self.createBtn.bind('<Button-1>', lambda e:digital_ic_support.submitCmlBtnClicked(e))
        self.createBtn.bind('<Return>', lambda e:digital_ic_support.submitCmlBtnClicked(e))

        self.resetBtn = ttk.Button(self.Labelframe3, style='topLvlBtn.TButton', takefocus=False)
        self.resetBtn.place(relx=0.65, rely=0.465, height=34, width=107, bordermode='ignore')
        self.resetBtn.configure(text='''Reset Settings''')
        self.resetBtn.bind('<Button-1>',lambda e:digital_ic_support.resetBtnClicked(e))
        self.resetBtn.bind('<Return>', lambda e:digital_ic_support.resetBtnClicked(e))

        self.Label1 = ttk.Label(self.Labelframe2, style='pinLabel.TLabel')
        self.Label1.place(relx=0.35, rely=0.93, height=21, width=75
                , bordermode='ignore')
        self.Label1.configure(text='''*required''')

        self.Labelframe4 = tk.LabelFrame(self.top)
        self.Labelframe4.place(relx=0.68, rely=0.025, relheight=0.95
                , relwidth=0.32)
        self.Labelframe4.configure(relief='groove')
        self.Labelframe4.configure(font="-family {Segoe UI} -size 12")
        self.Labelframe4.configure(foreground="#000000")
        self.Labelframe4.configure(text='''Result''')
        self.Labelframe4.configure(background="#d9d9d9")
        self.Labelframe4.configure(highlightbackground="#d9d9d9")
        self.Labelframe4.configure(highlightcolor="black")

        self.Scrolledtext1 = ScrolledText(self.Labelframe4)
        self.Scrolledtext1.place(relx=0.044, rely=0.037, relheight=0.889
                , relwidth=0.918, bordermode='ignore')
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

        self.copyBtn = ttk.Button(self.Labelframe4, style='topLvlBtn.TButton', takefocus=False)
        self.copyBtn.place(relx=0.7, rely=0.939, height=34, width=97
                , bordermode='ignore')
        self.copyBtn.configure(text='''Copy''')
        self.copyBtn.bind('<Button-1>', lambda e:digital_ic_support.copyBtnClicked(e))
        self.copyBtn.bind('<Return>', lambda e:digital_ic_support.copyBtnClicked(e))


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


if __name__ == '__main__':
    digital_ic_support.main()