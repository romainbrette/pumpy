'''
A simple patch-clamp GUI

Pressures
'''
from Tkinter import *
from devices import *
from numpy import *

verbose = True

class PatcherApplication(Frame):
    '''
    The main application.
    '''
    def __init__(self, master, controller):
        '''
        Parameters
        ----------
        master : parent window
        controller : the pressure controller
        '''
        Frame.__init__(self, master)
        self.master = master

        self.controller = controller

        Button(self, text='High pressure', command=self.high_pressure).pack()
        Button(self, text='Nearing', command=self.nearing).pack()
        Button(self, text='Seal', command=self.seal).pack()
        Button(self, text='Release', command=self.release).pack()
        Button(self, text='Break in', command=self.break_in).pack()

        self.high_pressure() # We start with high pressure

    def high_pressure(self):
        if verbose:
            print "High pressure"
        self.pressure = 800 # mBar (800-1000 in 2012 Kodandaramaiah paper)
        self.controller.set_pressure(self.pressure)

    def nearing(self):
        if verbose:
            print "Nearing"
        self.pressure = 25 # mBar (25-30)
        self.controller.set_pressure(self.pressure)

    def seal(self):
        # Sealing with small negative pressure
        if verbose:
            print "Sealing"
        self.pressure = -25 #(from Desai)
        # -15 to -20 in Kodandaramaiah paper?
        self.controller.set_pressure(self.pressure)

    def release(self):
        # Release the pressure
        if verbose:
            print "Releasing"
        self.pressure = 0
        # -15 to -20 in Kodandaramaiah paper?
        self.controller.set_pressure(self.pressure)

    def break_in(self):
        # Breaks in with a ramp
        # Holst thesis: 0 to -345 mBar in 1.5 second
        # Desai: -150 mBar for 1 second; repeated attempts
        if verbose:
            print "Breaking in; release after 1 s"
        self.pressure = -150
        self.controller.set_pressure(self.pressure)
        self.master.after(1000, self.release)

if __name__ == '__main__':
    root = Tk()
    root.title('Patcher')

    controller = OB1(calibrate=True)
    app = PatcherApplication(root, controller).pack(side="top", fill="both", expand=True)
    root.mainloop()

