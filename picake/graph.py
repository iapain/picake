"""
Calculator module for PI cake
PI cake PI computation project
Author: Deepak Thukral
MiNI 2008 Politehcnika Warsaw
"""
from Tkinter import *
import Tix

try:
    from Image import *
    PIL = 1
except ImportError:
    PIL = 0
    print "Application required PIL Imaging module to plot graph"

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
        pass