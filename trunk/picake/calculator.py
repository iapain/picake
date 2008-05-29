"""
Calculator module for PI cake
PI cake PI computation project
Author: Deepak Thukral
MiNI 2008 Politehcnika Warsaw
"""
from Tkinter import *
import gmpy
import Tix


class SimpleCalculator:
    """ Creates Calculator """
    def __init__(self, panel):
        self.panel = panel
        self.which = 0
        gmpy.set_minprec(2000)
        
    def draw(self):
        btn_list = [
            '7',  '8',  '9',  '*',  'C',
            '4',  '5',  '6',  '/',  'CMP',
            '1',  '2',  '3',  '-',  'POW',
            '0',  '.',  '=',  '+',  'neg' ]
    
        # create all buttons with a loop
        r = 15
        c = 0
        for b in btn_list:
            rel = 'ridge'
            cmd = lambda x=b: self.click(x)
            Button(self.panel,text=b,width=5, font=('courier',12,'bold'), relief=rel,command=cmd).grid(row=r,column=c)
            c += 1
            if c > 4:
                c = 0
                r += 1
                
        self.v = StringVar()
        self.v2 = StringVar()
        self.v3 = StringVar()
        self.scrollbar = Scrollbar(self.panel, orient=HORIZONTAL)
        self.entry = Entry(self.panel, width=50, font=('courier',16,'bold'), justify=RIGHT, textvariable=self.v)
        self.entry2 = Entry(self.panel, width=50, font=('courier',16,'bold'), justify=RIGHT, textvariable=self.v2)
        self.answer = Entry(self.panel, font=('courier',16,'bold'), bg="yellow", justify=RIGHT, width=50, textvariable=self.v3)

        self.entry.bind('<FocusIn>', setattr(self, 'which', 0))
        self.entry2.bind('<FocusIn>', setattr(self, 'which', 1))
        self.label = Label(self.panel, text="=", font=('courier',16,'bold'))

        
        self.scrollbar.config(command=self.scrollhandler)
        
        self.entry.grid(row=0, column=0, columnspan=5)
        self.entry2.grid(row=1, column=0, columnspan=5)
        self.scrollbar.grid(sticky=E+W, row=2, column=0, columnspan=5)
        self.answer.grid(row=3, column=0, columnspan=5)

        self.entry['xscrollcommand']=self.scrollbar.set

        self.entry.focus_set()

    def scrollhandler(self, *args):
        op, howMany = args[0], args[1]
        op1 = self.entry.get()
        op2 = self.entry2.get()
        ans = self.answer.get()
        
        max_len = max(len(op1), len(op2), len(ans))
        
        self.v.set(self.gen_space(max_len - len(op1)) + op1)
        self.v2.set(self.gen_space(max_len - len(op2)) + op2)
        self.v3.set(self.gen_space(max_len - len(ans)) + ans)
        
        if op == "scroll":
            units = args[2]
            self.entry.xview_scroll ( howMany, units )
            self.entry2.xview_scroll ( howMany, units )
            self.answer.xview_scroll ( howMany, units )
        elif op == "moveto":
            self.entry.xview_moveto ( howMany )
            self.entry2.xview_moveto( howMany )
            self.answer.xview_moveto ( howMany)
        
    def gen_space(self, n):
        buf = ""
        for i in xrange(n):
            buf += " "
        return buf
        
    def click(self, key):
        if not self.which:
            try:
                a = int(key)
                self.entry.insert(END, key)
            except:
                pass
        if self.which:
            try:
                a = int(key)
                self.entry.insert(END, key)
            except:
                pass

        if key == '*':
            self.answer.delete(0, END)
            try:
                self.answer.insert(0, str(gmpy.mpf(self.entry.get())*gmpy.mpf(self.entry2.get())))
            except:
                self.answer.insert(0, 'Error')

        if key == '/':
            self.answer.delete(0, END)
            try:
                self.answer.insert(0, str(gmpy.mpf(self.entry.get())/gmpy.mpf(self.entry2.get())))
            except:
                self.answer.insert(0, 'Error')

        if key == '+':
            self.answer.delete(0, END)
            try:
                self.answer.insert(0, str(gmpy.mpf(self.entry.get())+gmpy.mpf(self.entry2.get())))
            except:
                self.answer.insert(0, 'Error')

        if key == '-':
            self.answer.delete(0, END)
            try:
                self.answer.insert(0, str(gmpy.mpf(self.entry.get())-gmpy.mpf(self.entry2.get())))
            except:
                self.answer.insert(0, 'Error')

        if key == 'CMP':
            self.answer.delete(0, END)
            ret =  ""
            try:
                a = self.entry.get()
                b = self.entry2.get()
                if len(a) == len(b):
                    for i in xrange(len(a)):
                        if a[i] == b[i]:
                            ret+="1"
                        else:
                            ret+="0"
                else:
                    ret="-1"
                self.answer.insert(0, ret)
            except:
                self.answer.insert(0, 'Error')

        if key == 'POW':
            self.answer.delete(0, END)
            try:
                self.answer.insert(0, str(gmpy.mpf(self.entry.get())**gmpy.mpf(self.entry2.get())))
            except:
                self.answer.insert(0, 'Error')
            
            
