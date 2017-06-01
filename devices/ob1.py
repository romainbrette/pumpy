'''
Elveflow OB1 microfluidic flow control system
'''
import os
import sys
from ctypes import *
from array import array

sys.path.append('C:\Users\patch\Elveflow SDK V3_01_04\python_64'.encode('utf-8'))
sys.path.append('C:\Users\patch\Elveflow SDK V3_01_04\python_64\DLL64'.encode('utf-8'))
from Elveflow64 import *

__all__ = ['OB1']


class OB1(object):
    def __init__(self, calibrate=False):
        self.instr_ID = c_int32()
        print('Instrument name and regulator types hardcoded in the python script'.encode('utf-8'))
        # see User guide to determine regulator type NI MAX to determine the instrument name
        error = OB1_Initialization('01868D03'.encode('ascii'), 4, 0, 0, 0, byref(self.instr_ID))
        # all functions will return error code to help you to debug your code, for further information see user guide
        print('error:%d' % error)
        print('OB1 ID: %d' % self.instr_ID.value)

        # add one analog flow sensor
        error = OB1_Add_Sens(self.instr_ID, 1, 4, 0, 1)
        print('error add analog flow sensor:%d' % error)

        calib_path = os.path.expanduser(r'~\ob1_calibration.txt')
        self.calib = (c_double * 1000)()
        if calibrate:
            OB1_Calib(self.instr_ID.value, self.calib, 1000)
            error = Elveflow_Calibration_Save(calib_path.encode('ascii'), byref(self.calib), 1000)
            print ('calib saved in %s' % calib_path.encode('ascii'))
        else:
            if not os.path.isfile(calib_path):
                raise IOError('Calibration file "{}" does not exist'.format(calib_path))
            error = Elveflow_Calibration_Load(calib_path.encode('ascii'), byref(self.calib), 1000)


    def measure(self, port=0):
        '''
        Measures the instantaneous pressure, on designated port.
        '''
        set_channel = int(port)  # convert to int
        set_channel = c_int32(port)  # convert to c_int32
        get_pressure = c_double()
        error =  OB1_Get_Sens_Data(self.instr_ID.value, set_channel, 1, byref(get_pressure))  # Acquire_data =1 -> Read all the analog value
        print('error (get_pressure): ', error)
        return get_pressure.value

    def set_pressure(self, pressure, port=0):
        '''
        Sets the pressure, on designated port.
        '''
        set_channel = int(port)  # convert to int
        set_channel = c_int32(port)  # convert to c_int32
        set_pressure = float(pressure)
        set_pressure = c_double(pressure)  # convert to c_double
        error = OB1_Set_Press(self.instr_ID.value, set_channel, set_pressure, byref(self.calib), 1000)
        print('error: (set_pressure) ', error)
