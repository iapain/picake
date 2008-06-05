"""
PI cake PI computation project
Author: Deepak Thukral
MiNI 2008 Politehcnika Warsaw
"""
import re
from Tkinter import *
from tkFileDialog import askopenfilename, asksaveasfilename
import Tix
import signal
from pi import pi
import SearchDialog
from Formatter import TextFormatter
from calculator import SimpleCalculator
from graph import SimpleGraph

APP_NAME = "PI Cake - PI computation project"
APP_SIZE = '790x550+134+121'
APP_AUTHOR = "Deepak Thukral"
APP_DESC = "Implementation of PI computation based on various algorithm and searching within result"
APP_MENTOR = "Dr. Wladyslaw Homenda"
APP_MENTOR_HOME = "http://www.mini.pw.edu.pl/~homenda/"
APP_YEAR = "2008"
APP_DEPT = "MiNI, Politechnika Warsaw"
APP_AUTHOR_HOME = "http://gamma.mini.pw.edu.pl/~thukrald/"
APP_LICESNE = "GNU General Public License v2"

class SigHandler:
        def __init__(self):
            self.signaled = 0
            self.sn=None
        def __call__(self, sn, sf):
            self.sn = sn 
            self.signaled += 1


def vp_start_gui():
    global w
    global root
    root = Tix.Tk()
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open", underline=0, command=picake_open)
    filemenu.add_command(label="Save", underline=0, command=picake_save)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", underline=0, command=root.quit)
    menubar.add_cascade(label="File", underline=0, menu=filemenu)
    
    # create more pulldown menus
    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_command(label="Cut (Ctrl+x)", command=picake_cut)
    editmenu.add_command(label="Copy (Ctrl+c)", command=picake_copy)
    editmenu.add_command(label="Paste (Ctrl+v)", command=picake_paste)
    menubar.add_cascade(label="Edit", menu=editmenu)
    
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About", command=picake_about)
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
        self.nb.add('search', label='Search', underline=0)
        self.nb.add('graph', label='Graph', underline=0)
        self.nb.add('about', label='About', underline=0)
        self.nb.pack(expand=1, fill=Tix.BOTH, padx=1, pady=1 ,side=Tix.TOP)
        
        #PI tab
        tab = self.nb.pi
        self.f = Tix.Frame(tab)
        self.common = Tix.Frame(tab)

        self.f.pack(side=Tix.LEFT, padx=0, pady=0, fill=Tix.BOTH, expand=1)
        self.common.pack(side=Tix.RIGHT, padx=0, fill=Tix.Y)
        
        self.pane = Tix.PanedWindow(self.f, orientation='vertical')

        self.p1 = self.pane.add('a', min=70, size=300)
        self.p2 = self.pane.add('b', min=70)

        self.pane.pack(fill=BOTH, expand=1)
        self.lb = Tix.ScrolledText(self.p1, scrollbar='auto')
        self.lb_text = self.lb.subwidget_list["text"]
        self.lb.text['wrap'] = None
        self.lb.pack(fill=BOTH, expand=1)
        
        self.lb_text.bind('<Control-f>', self.find_event)
        self.lb_text.bind('<Control-F>', self.find_event)
        
        self.refresh_text(self.lb_text)
        
        
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

        #Tab for Search
        tab = self.nb.search
        self.fs = Tix.Frame(tab)
        self.common = Tix.Frame(tab)
        
        self.fs.pack(side=Tix.LEFT, padx=0, pady=0, fill=Tix.BOTH, expand=1)
        self.common.pack(side=Tix.RIGHT, padx=0, fill=Tix.Y)

        self.spane = Tix.PanedWindow(self.fs, orientation='horizontal')

        self.p1 = self.spane.add('a', min=70, size=300)
        self.p2 = self.spane.add('b', min=70)

        self.spane.pack(fill=BOTH, expand=1)
        self.lbs = Tix.ScrolledText(self.p1, scrollbar='auto')
        self.lbs_text = self.lbs.subwidget_list["text"]
        self.lbs.text['wrap'] = None
        self.lbs.pack(fill=BOTH, expand=1)
        
        self.lbs_text.bind('<Control-f>', self.find_event)
        self.lbs_text.bind('<Control-F>', self.find_event)
        
        self.refresh_text(self.lbs_text)
        
        self.spane2 = Tix.PanedWindow(self.p2, orientation='vertical')

        self.p3 = self.spane2.add('a', min=70, size=100)
        self.p4 = self.spane2.add('b', min=70)
        self.spane2.pack(fill=BOTH, expand=1)

        Label(self.p3, text="Search for: ").pack(fill=Tix.Y, padx=3, pady=3, side=Tix.LEFT)
        self.ma2 = Entry(self.p3)
        self.ma2.pack(fill=Tix.X, padx=3, pady=3, side=Tix.LEFT)
        self.resultLbl = Label(self.p2, text='', font=('courier',24,'bold'))
        self.resultLbl.pack(fill=Tix.X, padx=3, pady=3)
        
        self.butBox = Tix.ButtonBox(self.p3, orientation=Tix.HORIZONTAL)
        self.butBox.add('run', text="Search", width=14, command=self.run_search)
        self.butBox.pack(side=Tix.BOTTOM, fill=Tix.X)

        self.scrollbar = Scrollbar(self.p4, orient=VERTICAL)
        self.listbox = Listbox(self.p4, font=('courier',14,'bold'), yscrollcommand=self.scrollbar.set)
        self.listbox.bind("<Double-Button-1>", self.get_sel)
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=1)
        
        #Tab for graph
        tab=self.nb.graph
        self.fg = Tix.Frame(tab)
        self.common = Tix.Frame(tab)
        
        self.fg.pack(side=Tix.LEFT, padx=0, pady=0, fill=Tix.BOTH, expand=1)
        self.common.pack(side=Tix.RIGHT, padx=0, fill=Tix.Y)
        self.graph = SimpleGraph(self.fg).draw()
        
        
        #Tab for about
        tab=self.nb.about
        self.f = Tix.Frame(tab)
        self.common = Tix.Frame(tab)
        self.f.pack(side=Tix.LEFT, padx=0, pady=0, fill=Tix.BOTH, expand=1)
        self.common.pack(side=Tix.RIGHT, padx=0, fill=Tix.Y)
        Label(self.f, text=APP_NAME, font=('courier',16,'bold')).pack(fill=Tix.X, padx=3, pady=3)
        Label(self.f, text="Author: %s\n%s" %(APP_AUTHOR, APP_AUTHOR_HOME), font=('courier',12,'bold')).pack(fill=Tix.X, padx=3, pady=3)
        Label(self.f, text="Under guidance of %s\n%s" %(APP_MENTOR, APP_MENTOR_HOME), font=('courier',12,'bold')).pack(fill=Tix.X, padx=3, pady=3)
        Label(self.f, text="%s\n%s\n%s\n%s" %(APP_DESC, APP_DEPT, APP_LICESNE, APP_YEAR)).pack(fill=Tix.X, padx=3, pady=3)
            
    def run(self):
        v = self.ma.get().strip()
        unit = v[len(v)-1]
        try:
            n = int(v[:len(v)-1])
        except (TypeError, ValueError):
            alert('Percision should be an Integer')
            return
        try:
            uni = int(unit)
            n = n*10 + uni
        except:
            if unit == 'm' or unit == 'M':
                n*=1000000
            elif unit == 'k' or unit == 'K':
                n*=1000
            else:
                alert('Percision should be an Integer with unit K or M for thousand and million')
                return
        pii = pi(n)
        try:
            if n > 10000:
                r = pii.gmp_arch_tan()
            else:
                r = pii.compute_chudnovsky()
        finally:
            self.refresh_text(self.lb_text)
            self.refresh_text(self.lbs_text) 
            
    def run_search(self):
        global ql
        i = 0
        fp = open('pi', 'r')
        T = fp.read()
        fp.close()
        q = self.ma2.get()
        ql = len(q)
        starts =  [match.start() for match in re.finditer(re.escape(q), T)]
        self.resultLbl['text'] = str(len(starts)) + " Matches Found."
        self.listbox.delete(0, END)
        for start in starts:
            i+=1
            self.listbox.insert(END, "%d   ...%s... : %d" % (i, self.near(T, len(q), start), start)) 

    def near(self, T, q, start=0):
        if start - 5 < 0 and start + q + 5 < len(T):
            return T[start:start+q+5]
        elif start - 5 >=0 and start + q + 5 < len(T):
            return T[start-5:start+q+5]
        elif start - 5 >=0 and start + q + 5 >= len(T):
            return T[start-5:start+q+5]
        else:
            return "?????"

    def get_sel(self, event):
        a = int(self.listbox.get(self.listbox.curselection()[0]).split(':')[1].strip())
        
        first = "%d.%d" % (1, a)
        last = "%d.%d" % (1, a+ql)
        self.lbs_text.tag_remove("sel", "1.0", "end")
        self.lbs_text.tag_add("sel", first, last)
        self.lbs_text.mark_set(INSERT, first)
        self.lbs_text.see(INSERT)
        self.lbs_text.focus()


            
        
    def refresh_text(self, a):
        try:
            #self.lb.text['state'] = 'enabled'
            a.delete(1.0, END)
            fp = open('pi', 'r')
            data = fp.read()
            #p = TextFormatter(data[2:]).format()
            #print data
            a.insert(1.0, data)
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
        p = TextFormatter(data[0]).format()
        self.lb_text.insert(1.0, ''.join(p))
        
    def find_event(self, event=None):
        SearchDialog.find(self.lb_text)
        return "break"


def picake_open():
    f = askopenfilename()
    try:
        fp = open(f, 'r')
    except IOError:
        alert('Error reading file')
        return
    data = fp.read()
    fp.close()
    w.lb_text.delete(1.0, END)
    w.lb_text.insert(1.0, data)
    return
    

def picake_save():
    f = asksaveasfilename()
    data = w.lb_text.get(1.0, END)
    try:
        fp = open(f, 'w')
    except IOError:
        alert('Error writing file')
        return
    
    fp.write(data)
    fp.close()
    return

def picake_cut():
    try:
        selection = w.lb_text.get(SEL_FIRST, SEL_LAST)
        w.lb_text.clipboard_clear()
        w.lb_text.clipboard_append(selection)
        w.lb_text.delete(SEL_FIRST, SEL_LAST)
    except:
        pass

def picake_paste():
    try:
        topaste = w.lb_text.selection_get(selection="CLIPBOARD")
        w.lb_text.insert(INSERT, topaste)
    except:
        pass

def picake_copy():
    try:
        selection = w.lb_text.get(SEL_FIRST, SEL_LAST)
        w.lb_text.clipboard_clear()
        w.lb_text.clipboard_append(selection)
    except:
        pass

def picake_about():
    alert('%s - %s\n Written by %s\n Under supervision of %s' % (APP_NAME, APP_DESC, APP_AUTHOR, APP_MENTOR))

def alert(val):
    import Dialog
    Dialog.Dialog(title=APP_NAME, text=val, bitmap="",default=0,strings=("OK",))
    

    
def close(self=None):
    root.destroy()
    w = None
    return

if __name__ == '__main__':
    vp_start_gui()
