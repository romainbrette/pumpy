'''
A simple patch-clamp GUI

Pressures
'''
from Tkinter import *
from devices import *
from numpy import *
import threading
import inputs

verbose = False

class GamepadReader(threading.Thread):
    def __init__(self, event_container, gamepad):
        self.event_container = event_container
        self.gamepad = gamepad
        super(GamepadReader, self).__init__()

    def run(self):
        while True:
            event = self.gamepad.read()[0]
            if event.code in ['ABS_X', 'ABS_Y', 'BTN_SOUTH', 'BTN_NORTH', 'BTN_WEST', 'BTN_EAST']:
                self.event_container.append(event)

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
        self.pressure_string = StringVar()
        pressure_entry = Entry(self, textvariable=self.pressure_string)
        pressure_entry.bind("<Return>", self.pressure_change)
        pressure_entry.pack()
        #self.pressure_label = Label(self, text='')
        #self.pressure_label.pack()
        self.release() # We start with 0 pressure

        gamepad = inputs.devices.gamepads[0]
        self.event_container = []
        reader = GamepadReader(self.event_container, gamepad)
        reader.start()
        self.speed_x=0
        self.speed_y=0
        self.after(100, self.update_gamepad)

    def update_gamepad(self):
        for event in self.event_container:
            sign = -1 if event.state < 0 else 1
            if abs(event.state) < 4096:
                state = 0
            else:
                state = int(round((abs(event.state) - 4096)/ 1792.) * sign)
            if event.code == 'ABS_X':
                self.speed_x = state
            elif event.code == 'ABS_Y':
                self.speed_y = state
            elif event.code == 'BTN_SOUTH':
                self.break_in()
            elif event.code == 'BTN_NORTH':
                self.nearing()
            elif event.code == 'BTN_WEST':
                self.release()
            elif event.code == 'BTN_EAST':
                self.seal()
        if self.speed_y!=0:
            self.update_pressure(self.pressure+self.speed_y/4.)

        self.event_container[:] = []
        self.after(100, self.update_gamepad)

    def pressure_change(self, e):
        self.update_pressure(int(self.pressure_string.get()))

    def update_pressure(self, pressure):
        self.pressure = pressure
        self.controller.set_pressure(self.pressure)
        #self.pressure_label['text'] = 'Pressure: {}mbar'.format(self.pressure)
        self.pressure_string.set(pressure)

    def high_pressure(self):
        if verbose:
            print "High pressure"
        self.update_pressure(800)  # mBar (800-1000 in 2012 Kodandaramaiah paper)

    def nearing(self):
        if verbose:
            print "Nearing"
        self.update_pressure(25)  # mBar (25-30)

    def seal(self):
        # Sealing with small negative pressure
        if verbose:
            print "Sealing"
        self.update_pressure(-25) #(from Desai)
        # -15 to -20 in Kodandaramaiah paper?

    def release(self):
        # Release the pressure
        if verbose:
            print "Releasing"
        self.update_pressure(0)
        # -15 to -20 in Kodandaramaiah paper?

    def break_in(self):
        # Breaks in with a ramp
        # Holst thesis: 0 to -345 mBar in 1.5 second
        # Desai: -150 mBar for 1 second; repeated attempts
        if verbose:
            print "Breaking in; release after 1 s"
        self.update_pressure(-150)
        self.master.after(1000, self.release)

if __name__ == '__main__':
    root = Tk()
    root.title('Patcher')

    controller = OB1()
    app = PatcherApplication(root, controller).pack(side="top", fill="both", expand=True)
    root.mainloop()

