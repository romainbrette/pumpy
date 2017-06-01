'''
Records pressure during an experiment with the OB1
'''
from Tkinter import *
from devices import *
from numpy import *

from os.path import expanduser
home = expanduser("~")
filename = home+'/pressure.txt'

class RecorderApplication(Frame):
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
        self.button_text = StringVar('')
        Button(self, textvariable=self.button_text, command=self.record).pack()
        self.button_text.set('Record')
        self.isrecording = False

        self.measurement = list() # Could also be a numpy array

    def record(self):
        self.isrecording = not self.isrecording
        self.button_text.set(['Record', 'Stop'][self.isrecording])
        if self.isrecording:
            # Here we start clocked recording using a timer - could be different depending on the interface
            self.master.after(50, self.sample) # 20 Hz recording
        else:
            # Save to while when it's finished
            savetxt(filename, array(self.measurement))

    def sample(self):
        if self.isrecording:
            print "recording"
            self.measurement.append(self.controller.get_pressure()) # Here the actual measurement
            self.master.after(50, self.sample)

if __name__ == '__main__':
    root = Tk()
    root.title('Pressure recorder')
    controller = OB1()
    app = RecorderApplication(root, controller).pack(side="top", fill="both", expand=True)

    root.mainloop()

