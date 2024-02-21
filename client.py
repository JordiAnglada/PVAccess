import sys
import time
from pvaccess import Channel
from collections import OrderedDict

class ClientMonitor:
    def __init__(self, name):
        self.name = name
        self.value = 0
        self.nReceived = 0
        self.nMissed = 0
        self.percentageMissed = 0
        self.startTime = 0
        self.receiveRate = 0
        self.label = ""

    def set_label(self, label):
        self.label = label

    def toString(self):
        return '%6s: Received: %7d (%6.2f [kHz]); Missed: %7d (%6.2f%%)' % (self.name, self.nReceived, self.receiveRateKHz, self.nMissed, self.percentageMissed)
       
    def monitor_pv(self, pv):
        oldValue = self.value
        self.value = pv[self.label]
        self.nReceived += 1
        diff = self.value - oldValue
        if oldValue > 0:
            self.nMissed += diff-1
        else:
            self.startTime = time.time()
 
        # if self.nReceived % 10000 == 0:
        #     currentTime = time.time()
        #     deltaT = currentTime - self.startTime
        #     self.receiveRateKHz = self.nReceived/deltaT/1000.0
        #     self.percentageMissed = (self.nMissed*100.0)/(self.nReceived+self.nMissed)
            
        if self.nReceived % 100000 == 0:
            # print(self.toString())
            print(self.value)

if __name__ == '__main__':
    runtime = 60
    if len(sys.argv) > 1:
        runtime = float(sys.argv[1])

    channelName = 'counter' #pv name
    c_monitor = Channel(channelName)

    tel_name = 'MPS:TEL'
    tel_monitor = Channel(tel_name)
    #print('CONNECT TO %s:\n%s\n' % (channelName, c.get()))



    cnt_m = ClientMonitor(channelName)

    tel_m = ClientMonitor(tel_name)
    tel_m.set_label('temp')

    t0 = time.time()
    print('STARTING MONITOR for %s at %s\n' % (channelName, t0))

    # c_monitor.monitor(cnt_m.monitor, 'field(c)')

    tel_monitor.monitor(tel_m.monitor_pv, "field(" + tel_m.label + ")")
    

    
    # tel_monitor.put(23, "field(action_counter)")


    # telemetry_monitor.monitor(tel_m.monitor, 'field(action_counter)')


    time.sleep(runtime)
    c_monitor.stopMonitor()
    t1 = time.time()
    deltaT = t1-t0
    print('STOP MONITOR at %s\n' % t1)

    print('FINAL STATS:') 
    print(cnt_m.toString())
    print('')
    print('RUNTIME: %.2f [s]' % (deltaT))
    print('\nDONE')