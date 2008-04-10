"""
Calculator module for PI cake
PI cake PI computation project
Author: Deepak Thukral
MiNI 2008 Politehcnika Warsaw
"""
from Tkinter import *

class SimpleCalculator:
    """ Creates Calculator """
    def __init__(self, panel):
        self.panel = panel
        
    def draw(self):
        btn_list = [
            '7',  '8',  '9',  '*',  'C',
            '4',  '5',  '6',  '/',  'CMP',
            '1',  '2',  '3',  '-',  'DIF',
            '0',  '.',  '=',  '+',  'neg' ]
    
        # create all buttons with a loop
        r = 1
        c = 0
        for b in btn_list:
            rel = 'ridge'
            cmd = lambda x=b: self.click(x)
            Button(self.panel,text=b,width=5,relief=rel,command=cmd).grid(row=r,column=c)
            c += 1
            if c > 4:
                c = 0
                r += 1
                
        self.entry = Entry(self.panel, width=50, bg="yellow")
        self.entry.grid(row=0, column=0, columnspan=5)
        
    def click(self, key):
        #print key
        try:
            a = int(key)
            self.entry.insert(END, key)
        except:
            pass
