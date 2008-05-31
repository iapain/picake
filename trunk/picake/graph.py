"""
Calculator module for PI cake
PI cake PI computation project
Author: Deepak Thukral
MiNI 2008 Politehcnika Warsaw
"""
from Tkinter import *
import Tix
import re

try:
    import Image
    PIL = 1
except ImportError:
    PIL = 0
    print "Application required PIL Imaging module to plot graph"


def alert(val):
    import Dialog
    Dialog.Dialog(title="Picake", text=val, bitmap="",default=0,strings=("OK",))

class SimpleGraph:
    """ Creates Graph GUI """
    def __init__(self, panel):
        self.panel = panel
        self.pil = PIL
        
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
        for i in xrange(fr, to):
            stat.append([match.start() for match in re.finditer(str(i), T)])
        print stat

        
            
