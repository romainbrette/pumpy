'''
Elveflow OB1 microfluidic flow control system
'''
all = ['OB1']

class OB1(object):
    def __init__(self, calibrate = False):
        # Initializes and possibly calibrate
        pass

    def measure(self, port = 0):
        '''
        Measures the instantaneous pressure, on designated port.
        '''
        pass

    def set_pressure(self, pressure, port = 0):
        '''
        Sets the pressure, on designated port.
        '''
        pass