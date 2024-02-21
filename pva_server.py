import time
import pvaccess as pva
from pvaccess import ULONG
from pvaccess import PvObject
from pvaccess import PvaServer
from pvaccess import PvObject, STRING, INT, BOOLEAN, DOUBLE, PvaServer, SHORT, LONG
from collections import OrderedDict


SAFETY_MONITORING_CHANNEL = pva.PvObject({
    'err_cnt_rc': pva.SHORT,
    'err_cnt_crc': pva.SHORT,
    'err_cnt_md': pva.SHORT,
    'err_cnt_tout': pva.SHORT,
    'qt_latch': pva.SHORT,
    'qt_instant': pva.SHORT,
    'state': pva.SHORT,
    'spare': pva.SHORT
})

TIMESTAMP = {
    'nanoseconds': pva.INT,
    'seconds': pva.INT
}

TELEMETRY_STRUCT = {
  'timestamp': TIMESTAMP,
  'safety_monitoring': [SAFETY_MONITORING_CHANNEL],
  'interlock_events' : [pva.INT],
  'action_counter': pva.LONG,
  'psos_state'    : pva.LONG,
  'temp'          : pva.LONG
}

CONTROL_STRUCT = {
  'psos_cmd': pva.LONG,
  'force' : pva.INT,
  'reset': pva.LONG,
  'timeStamp': TIMESTAMP
}


if __name__ == '__main__':
    pv = PvObject({'c' : ULONG})

    safety_monitoring_pv = pva.PvObject({'safety_monitoring': [SAFETY_MONITORING_CHANNEL]})
    
    telemetry = pva.PvObject(TELEMETRY_STRUCT)
    telemetry['action_counter'] = 11
    telemetry['temp'] = 100
    print(telemetry)

    control = pva.PvObject(CONTROL_STRUCT)

    server = PvaServer()

    server.addRecord('counter', pv)
    server.addRecord('MPS:TEL', telemetry)
    server.addRecord('MPS:CTL', control)

    ch = pva.Channel('MPS:TEL')
    c = 0
    new_temp = 1
    startTime = time.time()
    while True:
        c += 1
        pv = PvObject({'c': ULONG}, {'c': c})

        server.update('counter', pv)
        # tel_mod['temp'] = temp
        # print(tel_mod['tel_md']['psos_state'])

        temp = ch.get()
        temp['temp'] = new_temp
        # Create a PvObject with the updated value
        # Update the server
        server.update('MPS:TEL', temp)


        # server.update('MPS:CTL', {'temp': new_temp})

        if c % 100000 == 0:
            new_temp += 1
            currentTime = time.time()
            runtime = currentTime - startTime
            updateRateKHz = c/runtime/1000.0
            print('Runtime: %.2f; Counter: %9d, Rate: %.2f [kHz]' % (runtime, c, updateRateKHz))
            print(telemetry['action_counter'])
            print(telemetry['temp'])
            
        