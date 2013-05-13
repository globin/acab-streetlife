import serialinterface
import time
import Queue
import threading
import thread

serials = [ 
    "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A400fvDr-if00-port0",
    "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A400fvDs-if00-port0",
#    "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A400fvDu-if00-port0",
#    "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A10044Xp-if00-port0",
    "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A400fvDt-if00-port0",
    "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A400fvDq-if00-port0",
    ]

#serials = [ 
#    "/dev/null",
#    "/dev/null",
#    "/dev/null",
#    "/dev/null",
#    "/dev/null",
#    "/dev/null",
#    ]

#              0   1     2     3     4     5     6     7     8     9     10    11    12    13    14    15
lamps =  [[ 0x30, 0x47, 0x11, 0x46, 0x29, 0x56 ],
          [ 0x35, 0x6e, 0x22, 0x52, 0x15, 0x10 ],
          [ 0x1c, 0x31, 0x16, 0x5e, 0x43, 0x3d ],
          [ 0x42, 0x72, 0x18, 0x1f, 0x5a, 0x19 ],
          [ 0x2d, 0x21, 0x2e, 0x2a, 0x4a, 0x37 ],
          [ 0x6f, 0x5d, 0x70, 0x4f, 0x6d, 0x60 ],
          [ 0x40, 0x23, 0x6c, 0x27, 0x1a, 0x1e ],
          [ 0x68, 0x62, 0x4c, 0x57, 0x3c, 0x50 ]]

interfaces = [0,1,2,3]
logical_interfaces = [0,0,3,3,1,1,2,2]
updatelock = threading.RLock()
updatequeues = []
updatecounter = 0

def interfaceHandler(queue, serial, updatequeue):
    global updatecounter
    while 1:
        msg = queue.get();
        if msg[4] == 'U':
            with updatelock:
                updatecounter += 1
                if updatecounter == len(interfaces):
                    updatecounter = 0
                    [q.put(0) for q in updatequeues]
            updatequeue.get()
        serial.write(msg)
        time.sleep(0.001)

def createBridge(dev):
    serial = serialinterface.SerialInterface(dev,115200,1)
    queue = Queue.Queue(100)
    updatequeue = Queue.Queue(1)
    updatequeues.append(updatequeue)
    return (queue, serial, updatequeue)

bridges = map(createBridge,serials)
for bridge in bridges:
    bridge[1].write('\\F')
    thread.start_new_thread(interfaceHandler,bridge)

buffered = False

def send(x,y,r,g,b,t):
    ms = int(t*1000)
    if x == 100 and y == 100:
        if ms == 0:
            for i in interfaces:
                sendSetColor(0,r,g,b,i)
        else:
            for i in interfaces:
                sendMSFade(0,r,g,b,ms,i)
        return
    if x == 100:
        if ms == 0:
            sendSetColor(0,r,g,b,y)
        else:
            sendMSFade(0,r,g,b,ms,y)
        return

    lamp = lamps[y][x]

    if ms == 0:
        sendSetColor(lamp,r,g,b,logical_interfaces[y])
    else:
        sendMSFade(lamp,r,g,b,ms,logical_interfaces[y])

def high(x):
    return (x>>8)&0xff;

def low(x):
    return x&0xff;

def sendSetColor(lamp,r,g,b,interface):
    global buffered
    if buffered:
        cmd = "%cP%c%c%c"%(chr(lamp),chr(r),chr(g),chr(b))
    else:
        cmd = "%cC%c%c%c"%(chr(lamp),chr(r),chr(g),chr(b))
    write(cmd,interface);

def sendMSFade(lamp,r,g,b,ms,interface):
    global buffered
    if buffered:
        cmd = "%cc%c%c%c%c%c"%(chr(lamp),chr(r),chr(g),chr(b),chr(high(ms)),chr(low(ms)))
    else:
        cmd = "%cM%c%c%c%c%c"%(chr(lamp),chr(r),chr(g),chr(b),chr(high(ms)),chr(low(ms)))
    write(cmd,interface);

def sendSpeedFade(x,y,r,g,b,speed,interface):
    global buffered
    lamp = lamps[y][x]
    if buffered:
        cmd = "%ca%c%c%c%c%c"%(chr(lamp),chr(r),chr(g),chr(b),chr(high(speed)),chr(low(speed)))
    else:
        cmd = "%cF%c%c%c%c%c"%(chr(lamp),chr(r),chr(g),chr(b),chr(high(speed)),chr(low(speed)))

    write(cmd,interfaces[y]);

def sendUpdate(mode):
    global buffered
    if mode and not buffered:
        buffered = True
        for i in interfaces:
            sendMSFade(0,0,0,0,1500,interfaces[i])
    buffered = mode
    if buffered:
        cmd = "%cU"%chr(0)
        for i in interfaces:
            write(cmd, interfaces[i])

fullmessage = [False for i in interfaces]

def write(msg, interface):
    msg = "\x5c\x30%s\x5c\x31"%(msg.replace("\\","\\\\"))
    msg = msg.replace("\\","\\\\")

    if not bridges[interface][0].full():
        if fullmessage[interface]:
            print 'reactivating bridge'
            fullmessage[interface] = False
        bridges[interface][0].put(msg)
    else:
        if fullmessage[interface] == False:
            print 'ignoring', msg, 'queue for bridge is full'
            fullmessage[interface] = True

