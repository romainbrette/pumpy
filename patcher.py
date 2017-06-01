'''
A simple patch-clamp GUI
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

        Button(self, text='High pressure', command=self.high_pressure).pack()
        Button(self, text='Seal', command=self.seal).pack()
        Button(self, text='Break in', command=self.break_in).pack()

        self.high_pressure() # We start with high pressure

    def high_pressure(self):
        if verbose:
            print "High pressure"
        self.pressure = 850 # in Pa? check this out in the papers/Holt thesis

    def seal(self):
        # Release the pressure
        if verbose:
            print "Sealing"
        self.pressure = 0

    def break_in(self):
        # Breaks in with a ramp
        if verbose:
            print "Breaking in"
        pass

if __name__ == '__main__':
    root = Tk()
    root.title('Patcher')

    app = PatcherApplication(root, None).pack(side="top", fill="both", expand=True)
    root.mainloop()

