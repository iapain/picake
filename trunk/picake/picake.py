"""
PI cake PI computation project
Author: Deepak Thukral
MiNI 2008 Politehcnika Warsaw
"""

from Tkinter import *
import Tix
import signal
from pi import pi
import SearchDialog
from Formatter import TextFormatter
from calculator import SimpleCalculator

APP_NAME = "PI Cake - PI computation project"
APP_SIZE = '790x550+134+121'
APP_AUTHOR = "Deepak Thukral"
APP_DESC = "Implementation of PI computation based on various algorithm and searching within result"
APP_MENTOR = "Dr. Wladyslaw Homenda"
APP_MENTOR_HOME = "http://www.mini.pw.edu.pl/~homenda/"
APP_YEAR = "2008"
APP_DEPT = "MiNI, Politechnika Warsaw"
APP_AUTHOR_HOME = "http://gamma.mini.pw.edu.pl/~thukrald/"

class sigHandler:
	""" Adds posibility to stop program while computation """
	def __init__(self):
		self.signaled = 0
	def __call__(self):
		self.signaled += 1


def vp_start_gui():
    global w
    global root
    root = Tix.Tk()
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open", command=None)
    filemenu.add_command(label="Save", command=None)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    
    # create more pulldown menus
    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_command(label="Cut", command=None)
    editmenu.add_command(label="Copy", command=None)
    editmenu.add_command(label="Paste", command=None)
    menubar.add_cascade(label="Edit", menu=editmenu)
    
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About", command=None)
    menubar.add_cascade(label="Help", menu=helpmenu)
    
    # display the menu
    root.config(menu=menubar)

    root.protocol("WM_DELETE_WINDOW", close)
    root.title(APP_NAME)
    root.geometry(APP_SIZE)
    w = piGUI(root)
    root.mainloop()

class piGUI:
    def __init__(self, master=None):
        self.data = []
        self.max_weight = 0
        
        self.nb = Tix.NoteBook(master, name='nb', ipadx=6, ipady=6)
        self.nb['bg'] = 'gray'
        self.nb.nbframe['backpagecolor'] = 'gray'
        self.nb.add('pi', label='PI Computation', underline=0)
        self.nb.add('calculator', label='Calculator', underline=0)
        self.nb.add('about', label='About', underline=0)
        self.nb.pack(expand=1, fill=Tix.BOTH, padx=1, pady=1 ,side=Tix.TOP)
        
        #PI tab
        tab = self.nb.pi
        self.f = Tix.Frame(tab)
        self.common = Tix.Frame(tab)

        self.f.pack(side=Tix.LEFT, padx=0, pady=0, fill=Tix.BOTH, expand=1)
        self.common.pack(side=Tix.RIGHT, padx=0, fill=Tix.Y)
        
        self.pane = Tix.PanedWindow(self.f, orientation='vertical')

        self.p1 = self.pane.add('a', min=70, size=400)
        self.p2 = self.pane.add('b', min=70)

        self.pane.pack(fill=BOTH, expand=1)
        self.lb = Tix.ScrolledText(self.p1, scrollbar='auto')
        self.lb_text = self.lb.subwidget_list["text"]
        self.lb.text['wrap'] = None
        self.lb.pack(fill=BOTH, expand=1)
        
        self.lb_text.bind('<Control-f>', self.find_event)
        self.lb_text.bind('<Control-F>', self.find_event)
        
        self.refresh_text()
        
        
        Label(self.p2, text="Precision: ").pack(fill=Tix.Y, padx=3, pady=3, side=Tix.LEFT)
        self.ma = Entry(self.p2)
        self.ma.pack(fill=Tix.X, padx=3, pady=3, side=Tix.LEFT)
        self.resultLbl = Label(self.p2, text='', font=('courier',24,'bold'))
        self.resultLbl.pack(fill=Tix.X, padx=3, pady=3)
        
        self.butBox = Tix.ButtonBox(self.p2, orientation=Tix.HORIZONTAL)
        self.butBox.add('format', text='Format', width=14, command=self.format_text)
        self.butBox.add('run', text="Run", width=14, command=self.run)
        self.butBox.pack(side=Tix.BOTTOM, fill=Tix.X)
        #Tab for calcualtor
        tab = self.nb.calculator
        self.fc = Tix.Frame(tab)
        self.common = Tix.Frame(tab)
        
        self.fc.pack(side=Tix.LEFT, padx=0, pady=0, fill=Tix.BOTH, expand=1)
        self.common.pack(side=Tix.RIGHT, padx=0, fill=Tix.Y)
        self.calc = SimpleCalculator(self.fc).draw()
        
        #Tab for about
        tab=self.nb.about
        self.f = Tix.Frame(tab)
        self.common = Tix.Frame(tab)
        self.f.pack(side=Tix.LEFT, padx=0, pady=0, fill=Tix.BOTH, expand=1)
        self.common.pack(side=Tix.RIGHT, padx=0, fill=Tix.Y)
        Label(self.f, text=APP_NAME, font=('courier',16,'bold')).pack(fill=Tix.X, padx=3, pady=3)
        Label(self.f, text="Author: %s\n%s" %(APP_AUTHOR, APP_AUTHOR_HOME), font=('courier',12,'bold')).pack(fill=Tix.X, padx=3, pady=3)
        Label(self.f, text="Under guidance of %s\n%s" %(APP_MENTOR, APP_MENTOR_HOME), font=('courier',12,'bold')).pack(fill=Tix.X, padx=3, pady=3)
        Label(self.f, text="%s\n%s\n%s" %(APP_DESC, APP_DEPT, APP_YEAR)).pack(fill=Tix.X, padx=3, pady=3)
            
    def run(self):
        try:
            n = int(self.ma.get())
        except (TypeError, ValueError):
            alert('Percision should be an Integer')
            return
        pii = pi(n)
        try:
            r = pii.compute_chudnovsky()
        finally:
            self.refresh_text()
        
    def refresh_text(self):
        try:
            #self.lb.text['state'] = 'enabled'
            self.lb_text.delete(1.0, END)
            fp = open('pi', 'r')
            data = fp.read()
            #p = TextFormatter(data[2:]).format()
            #print data
            self.lb_text.insert(1.0, data)
            #self.lb.text['state'] = 'disabled'
            fp.close()
            #alert(len(data)-2)
        except Exception, e:
            str(e)
            pass
        
        
    def format_text(self):
        self.lb_text.delete(1.0, END)
        fp = open('pi', 'r')
        data = fp.readlines()
        fp.close()
	#print data
        p = TextFormatter(data[0]).format()
	#print p
        self.lb_text.insert(1.0, ''.join(p))
        
    def find_event(self, event=None):
        SearchDialog.find(self.lb_text)
        return "break"

def alert(val):
    import Dialog
    Dialog.Dialog(title=APP_NAME, text=val, bitmap="",default=0,strings=("OK",))
    

    
def close(self=None):
    root.destroy()
    w = None
    return

if __name__ == '__main__':
    vp_start_gui()
