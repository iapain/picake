from Tkinter import *
import time

class HaltException(Exception):
    pass

class BusyBar(Frame):
    def __init__(self, master=None, **options):
        # make sure we have sane defaults
        self.master=master
        self.options=options
        self.force=0
        self.width=options.setdefault('width', 100)
        self.height=options.setdefault('height', 10)
        self.background=options.setdefault('background', 'gray')
        self.relief=options.setdefault('relief', 'sunken')
        self.bd=options.setdefault('bd', 2)

        #extract options not applicable to frames
        self._extractOptions(options)

        # init the base class
        Frame.__init__(self, master, options)

        self.incr=self.width*self.increment
        self.busy=0
        self.dir='right'

        # create the canvas which is the container for the bar
        self.canvas=Canvas(self, height=self.height, width=self.width, bd=0,
                           highlightthickness=0, background=self.background)
        # catch canvas resizes
        self.canvas.bind('<Configure>', self.onSize)

        # this is the bar that moves back and forth on the canvas
        self.scale=self.canvas.create_rectangle(0, 0, self.width*self.barWidth, self.height, fill=self.fill)

        # label that is in the center of the widget
        self.label=self.canvas.create_text(self.canvas.winfo_reqwidth() / 2,
                                           self.height / 2, text=self.text,
                                           anchor="c", fill=self.foreground,
                                           font=self.font)
        self.update()
        self.canvas.pack(side=TOP, fill=X, expand=NO)
        self.but = Button(self, text= ' Stop !!!', command=self.off)
        self.but.pack(side=LEFT, expand=NO)

    def _extractOptions(self, options):
        # these are the options not applicable to a frame
        self.foreground=pop(options, 'foreground', 'yellow')
        self.fill=pop(options, 'fill', 'blue')
        self.interval=pop(options, 'interval', 30)
        self.font=pop(options, 'font','helvetica 10')
        self.text=pop(options, 'text', '')
        self.barWidth=pop(options, 'barWidth', 0.2)
        self.increment=pop(options, 'increment', 0.05)

    # todo - need to implement config, cget, __setitem__, __getitem__ so it's more like a reg widget
    # as it is now, you get a chance to set stuff at the constructor but not after

    def onSize(self, e=None):
        self.width = e.width
        self.height = e.height
        # make sure the label is centered
        self.canvas.delete(self.label)
        self.label=self.canvas.create_text(self.width / 2, self.height / 2, text=self.text,
                                           anchor="c", fill=self.foreground, font=self.font)

    def on(self):
        self.busy = 1
        self.force = 0
        self.canvas.after(self.interval, self.update)

    def of(self):
        self.busy = 0

    def off(self, event=None):
        self.of()
        self.force = 1
        

    def getstat(self):
        if self.force:
            raise HaltException
        else:
            pass

    def update(self):
        # do the move
        x1,y1,x2,y2 = self.canvas.coords(self.scale)
        if x2>=self.width:
            self.dir='left'
        if x1<=0:
            self.dir='right'
        if self.dir=='right':
            self.canvas.move(self.scale, self.incr, 0)
        else:
            self.canvas.move(self.scale, -1*self.incr, 0)

        if self.busy:
            self.canvas.after(self.interval, self.update)
        self.canvas.update_idletasks()

def pop(dict, key, default):
    value = dict.get(key, default)
    if dict.has_key(key):
        del dict[key]
    return value


if __name__=='__main__':
    root = Tk()

    def popup():
        win=Toplevel()
        win.title("I'm busy too!")
        bb1=BusyBar(win, text='Wait for me!')
        bb1.pack()
        try:
            for i in xrange(0,300000):
                    print "hello"
                    time.sleep(1)
                    bb1.update()
                    bb1.getstat()
                    root.update()
        except HaltException:
            pass
                
        bb1.of()
        time.sleep(1)
        win.destroy()

    t = Text(root)
    t.pack(side=TOP)
    bb = BusyBar(root, text='Please Wait')
    bb.pack(side=LEFT, expand=NO)
    but = Button(root, text= 'Pop-up BusyBar', command=popup)
    but.pack(side=LEFT, expand=NO)
    q = Button(root, text= 'Quit', command=root.destroy)
    q.pack(side=LEFT, expand=NO)
    l = Label(root, text="I'm a status bar !")
    l.pack(side=RIGHT)
    bb.on()
    root.update_idletasks()
    for i in range(0,30):
        time.sleep(0.1)
        root.update()
    bb.of()
    root.mainloop()
