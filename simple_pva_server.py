import pvaccess as pva
from time import sleep

pv = pva.PvScalarArray(pva.UINT)

x_array = [1, 2, 3]
y_array = [1, 2, 3]
pv.set(x_array)


d =  {
    'array' : [pva.UINT],
}

db = pva.PvObject(d)

var = pva.PvObject({"aux" : [pva.UINT]})


server = pva.PvaServer()
server.addRecord('pv', pv)
server.addRecord('db', db)
server.addRecord('aux', var)

# pv_ch = pva.Channel('pv')

# print('---')
print(pv)
num = 0

while True:
    num += 1
    
    if num > 4:
        num = 0
    
    x_array[1] = num
    y_array[0] = num
    
    pv.set(x_array)
    db.setScalarArray('array', y_array)

    print(pv)
    print(db)
    print("---------------- \n")
    sleep(0.5)
    
    