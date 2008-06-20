"""
Calculator module for PI cake
PI cake PI computation project
Author: Deepak Thukral
MiNI 2008 Politehcnika Warsaw
"""
from Tkinter import *
import gmpy
import Tix
import os
from tkFileDialog import askopenfilename, asksaveasfilename
from tkMessageBox import showerror


class SimpleCalculator:
    """ Creates Calculator """
    def __init__(self, panel):
        self.panel = panel
        self.which = 0
        self.dir = os.path.dirname(__file__)
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
        self.load1 = Button(self.panel, text=">>", command=self.load_file1)
        self.load2 = Button(self.panel, text=">>", command=self.load_file2)
        self.save1 = Button(self.panel, text="Save", command=self.load_save1)
        self.save2 = Button(self.panel, text="Save", command=self.load_save2)

        self.entry.bind('<FocusIn>', self.set_entry1)
        self.entry2.bind('<FocusIn>', self.set_entry2)
        self.answer.bind('<FocusIn>', self.set_entry3)
        
        self.label = Label(self.panel, text="=", font=('courier',16,'bold'))

        
        self.scrollbar.config(command=self.scrollhandler)
        
        self.entry.grid(row=0, column=0, columnspan=5)
        self.load1.grid(row=0, column=6)
        self.save1.grid(row=0, column=7)
        self.entry2.grid(row=1, column=0, columnspan=5)
        self.load2.grid(row=1, column=6)
        self.save2.grid(row=1, column=7)
        self.scrollbar.grid(sticky=E+W, row=2, column=0, columnspan=5)
        self.answer.grid(row=3, column=0, columnspan=5)

        self.entry['xscrollcommand']=self.scrollbar.set

        self.entry.focus_set()
        
        
    def autocast(self, n):
        loc = n.find(".")
        if loc >= 0:
            return gmpy.mpf(n)
        return gmpy.mpz(n)
        
    def load_file1(self):
        self.load_file(1)
        
    def load_file2(self):
        self.load_file(2)
        
    def load_save1(self):
        self.save_file(1)
        
    def load_save2(self):
        self.save_file(2)
        
    def save_file(self, n=1):
        f = asksaveasfilename(initialdir=self.dir)
        self.dir = os.path.dirname(f)
        dat = ""
        if n == 1:
           dat = self.v.get()
        elif n == 2:
            dat = self.v2.get()
        else:
            dat = self.v3.get()
        try:
            fp = open(f, 'w')
            fp.write(dat)
            fp.close()
        except IOError:
            showerror("Couldn't Write file: IOError")
            
        
    def load_file(self, n=1):
        f = askopenfilename(initialdir=self.dir)
        self.dir = os.path.dirname(f)
        fp = open(f, 'r')
        data = fp.read()
        fp.close()
        if n == 1:
            self.v.set(data)
        elif n == 2:
            self.v2.set(data)
        else:
            self.v3.set(data)
        
    def set_entry1(self, event=None):
        self.which = 0
        
    def set_entry2(self, event=None):
        self.which = 1
        
    def set_entry3(self, event=None):
        self.which = 2

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
        gmpy.set_minprec(1000)
        if not self.which:
            try:
                a = int(key)
                self.entry.insert(END, key)
            except:
                pass
        else:
            try:
                a = int(key)
                self.entry2.insert(END, key)
            except:
                pass

        if key == '*':
            self.answer.delete(0, END)
            try:
                self.answer.insert(0, str(self.autocast(self.entry.get())*self.autocast(self.entry2.get())))
            except Exception, e:
                print str(e)
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
                self.answer.insert(0, str(self.autocast(self.entry.get())+self.autocast(self.entry2.get())))
            except:
                self.answer.insert(0, 'Error')

        if key == '-':
            self.answer.delete(0, END)
            try:
                self.answer.insert(0, str(self.autocast(self.entry.get())-self.autocast(self.entry2.get())))
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
            except Exception, e:
                print str(e)
                self.answer.insert(0, 'Error')
                
        
        if key == 'neg':
            if self.which == 0:
                try:
                    op = int(self.entry.get())
                    if not self.entry.get().startswith('-'):
                        self.v.set('-' + self.entry.get())
                    else:
                        self.v.set(self.entry.get()[1:])
                except ValueError:
                    pass
                
            elif self.which == 1:
                try:
                    op = int(self.entry2.get())
                    if not self.entry2.get().startswith('-'):
                        self.v2.set('-' + self.entry2.get())
                    else:
                        self.v2.set(self.entry2.get()[1:])
                except ValueError:
                    pass
            
            else:
                try:
                    op = int(self.answer.get())
                    if not self.answer.get().startswith('-'):
                        self.v3.set('-' + self.answer.get())
                    else:
                        self.v3.set(self.answer.get()[1:])
                except ValueError:
                    pass
                
                
            
