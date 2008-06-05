"""
Calculator module for PI cake
PI cake PI computation project
Author: Deepak Thukral
MiNI 2008 Politehcnika Warsaw
"""
from Tkinter import *
import Tix
import re


def alert(val):
    import Dialog
    Dialog.Dialog(title="Picake", text=val, bitmap="",default=0,strings=("OK",))

class SimpleGraph:
    """ Creates Graph GUI """
    def __init__(self, panel):
        self.panel = panel
        self.has_prev = 0
        self.has_next = 0
        self.pages = -1
        self.scale = 1
        self.where = 0
        
    def draw(self):
        self.pane = Tix.PanedWindow(self.panel, orientation='vertical')
        self.p1 = self.pane.add('a', min=70, size=100)
        self.p2 = self.pane.add('b', min=70)
        self.pane.pack(fill=BOTH, expand=1)
        
        Label(self.p1, text="Search from: ").pack(fill=Tix.Y, padx=3, pady=3, side=Tix.LEFT)
        self.ma1 = Entry(self.p1)
        self.ma1.pack(fill=Tix.X, padx=3, pady=3, side=Tix.LEFT)
        Label(self.p1, text="to: ").pack(fill=Tix.Y, padx=3, pady=3, side=Tix.LEFT)
        self.ma2 = Entry(self.p1)
        self.ma2.pack(fill=Tix.X, padx=3, pady=3, side=Tix.LEFT)
        
        self.butBox = Tix.ButtonBox(self.p1, orientation=Tix.HORIZONTAL)
        self.butBox.add('run', text="Search and Plot", width=14, command=self.search_plot)
        self.butBox.pack(side=Tix.BOTTOM, fill=Tix.X)
        
        self.canvas = Tix.Canvas(self.p2, width=450, height=300, bg = 'white')
        self.canvas.pack()
        self.but1 = Button(self.p2, text="<< Prev", width=14, state=DISABLED, command=self.scroll_graph_prev)
        self.but1.pack(side=Tix.BOTTOM, fill=Tix.X)
        self.but2 = Button(self.p2, text="Next >>", width=14, state=DISABLED, command=self.scroll_graph_next)
        self.but2.pack(side=Tix.BOTTOM, fill=Tix.X)
        
    def scroll_graph_next(self):
        self.where += 1
        self.plot_graph(self.data, self.fr+10, self.to)
    
    def scroll_graph_prev(self):
        self.where -= 1
        self.plot_graph(self.data, self.fr-10, self.to)


    def plot_graph(self, data, fr, to):
        self.fr = fr
        self.to = to
        
        self.canvas.delete(ALL)
        
        self.canvas['bg'] = 'white'
        
        self.canvas.create_line(20,280,400,280, width=2, arrow=LAST)
        self.canvas.create_line(20,280,20,20,  width=2, arrow=LAST)
        
        self.pages = (fr - to)/10
        
        if self.where >= self.pages:
            self.but2.config(state = DISABLED)
        else:
            self.but2.config(state = NORMAL)
            
        if self.where <= 0:
            self.but1.config(state = DISABLED)
        else:
            self.but1.config(state = NORMAL)
            
        if to - fr > 10:
            self.has_next = 1
            self.but2.config(state = NORMAL)

        for i in range(11):
            x = 20 + (i * 30)
            self.canvas.create_line(x,280,x,275, width=1)
            self.canvas.create_text(x,284, text='%d'% (fr + i*self.scale), anchor=N)

        for i in range(2):
            x = 280 - (i * 160)
            self.canvas.create_line(20,x,25,x, width=2)
            self.canvas.create_text(16,x, text='%d'% (i), anchor=S)
        dat = data[self.where*10:self.where*10 + 11]
        
        cnt = 0
        for xs,ys in dat:
            if ys:
                self.canvas.create_oval(17 + (cnt*30),117,23 + (cnt*30),123, width=1, outline='black', fill='Red')
                self.canvas.create_text(17 + (cnt*30),100, text='%d'% (ys), anchor=N)
            else:
                self.canvas.create_oval(17 + (cnt*30),277,23 + (cnt*30),283, width=1, outline='black', fill='Red')
                self.canvas.create_text(17 + (cnt*30),260, text='%d'% (ys), anchor=N)
                
            cnt+=1
        
    def search_plot(self):
        stat = list()
        try:
            fr = int(self.ma1.get())
            to = int(self.ma2.get())
            if fr < 1 or to <= 1:
                raise ValueError
            if fr > to:
                alert('Please provide an increasing range')
                return
        except ValueError:
                alert('Please provide positive integer values')
                return
        try:
            fp = open('pi', 'r')
        except IOError:
            alert('Error Reading pi dump file')
            return
        T = fp.read()
        fp.close()
        try:
            for i in xrange(fr, to+1):
                stat.append([i, len([match.start() for match in re.finditer(str(i), T)])])
        except:
            alert('Number too large')
            return
        self.data = stat
        self.fr = fr
        self.to = to
        
        self.plot_graph(stat, fr, to)
