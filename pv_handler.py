import pvaccess as pva
from pvaccess import Channel
from pva_server import TELEMETRY_STRUCT, CONTROL_STRUCT
import time


class PVHandler:
    def __init__(self, name):
        self.name = name
        self.field = None
        self.value = 0
        self.nReceived = 0
        self.nMissed = 0
        self.percentageMissed = 0
        self.startTime = 0
        self.receiveRate = 0

    def toString(self):
        return '%6s: Received: %7d (%6.2f [kHz]); Missed: %7d (%6.2f%%)' % (self.name, self.nReceived, self.receiveRateKHz, self.nMissed, self.percentageMissed)

    def monitor_cb(self, pv_object):
        self.value = pv_object[self.field]
        print("Received update:")
        print(pv_object)


    def pv_monitor(self, field = None):
        tel_m = Channel(self.name)
        field_name = f'field({field})'
        self.field = field_name
        oldValue = self.value
        tel_m.monitor(self.monitor_cb, self.field)
        print(self.value)
        self.nReceived += 1
        diff = self.value - oldValue

        if oldValue > 0:
            self.nMissed += diff-1
        else:
            self.startTime = time.time()
 
        if self.nReceived % 10000 == 0:
            currentTime = time.time()
            deltaT = currentTime - self.startTime
            self.receiveRateKHz = self.nReceived/deltaT/1000.0
            self.percentageMissed = (self.nMissed*100.0)/(self.nReceived+self.nMissed)
            
        if self.nReceived % 100000 == 0:
            print(self.toString())
            print(self.value)


    def pv_get(self, field=None):
        ch = Channel(self.name)
        if field is not None:
            # If ch_name and field is provided
            # Get the current value of the field
            field_name = f'field({field})'
            pv_value = ch.get(field_name)
        else:
            # If only ch_name is provided
            # Get the current value of the structure
            pv_value = ch.get()
        
        print(pv_value)
        return pv_value


    def pv_put(self, value, field=None):
        ch = Channel(self.name)
        if field is not None:
            field_name = f'field({field})'
            ch.put(value, field_name)

        else:
            # Get the current value of the structure
            ch.put(value)


if __name__ == '__main__':
    pv_handler = PVHandler('MPS:TEL')  # Replace with your desired PV name
    pv_handler.pv_get('action_counter')

    t1 = pva.PvObject(TELEMETRY_STRUCT)
    t1['action_counter'] = 5
    # Example of pv_put
    pv_handler.pv_put(t1)
    
    #Check that the put value has applyed
    pv_handler.pv_get('action_counter')

    # pv_handler.pv_monitor('temp')

    time.sleep(20)

    