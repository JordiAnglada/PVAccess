import time
from pvaccess import Channel

def clbk(pv):
    print(pv)
    print(pv['action_counter'])

def err(ex):
    print('Error: %s' % ex)

tel_name = 'MPS:TEL'
c = Channel(tel_name)
for i in range(0,2):
    try:
        val = c.asyncGet(clbk, err)
        # val['action_counter'] = 23
        # c.put(val)

        print('Started Async Get #%d' % i)

    except Exception as ex:
        print('Error for request #%d: %s' % (i,ex))
time.sleep(0.01)
print("Destructor begin")
del c
print("Destructor done")
time.sleep(1)