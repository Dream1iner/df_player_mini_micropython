# df player mini requrements:
# files should be named 001.mp3, 002.mp3 etc.
# sd card limit is 32 Gb
# you can create multiple folder and name them 01, 02 etc.
# in this case you need to modify next_track() functions
# in this example next_track() is only working in "root" folder - #1

from utime import sleep_ms, sleep
from machine import UART, Pin
from utime import sleep_ms, sleep

class DFPlayer():
    UART_BAUD_RATE=9600
    UART_BITS=8
    UART_PARITY=None
    UART_STOP=1
    
    START_BYTE = 0x7E
    VERSION_BYTE = 0xFF
    COMMAND_LENGTH = 0x06
    ACKNOWLEDGE = 0x01
    END_BYTE = 0xEF
    COMMAND_LATENCY =   500

    def __init__(self, uartInstance, txPin, rxPin, busyPin):
        self.playerBusy=Pin(busyPin, Pin.IN, Pin.PULL_UP)
        self.uart = UART(uartInstance, baudrate=self.UART_BAUD_RATE, tx=Pin(txPin), rx=Pin(rxPin), bits=self.UART_BITS, parity=self.UART_PARITY, stop=self.UART_STOP)
            

    def split(self, num):
        return num >> 8, num & 0xFF

    def sendcmd(self, command, parameter1, parameter2):
        checksum = -(self.VERSION_BYTE + self.COMMAND_LENGTH + command + self.ACKNOWLEDGE + parameter1 + parameter2)
        highByte, lowByte = self.split(checksum)
        toSend = bytes([b & 0xFF for b in [self.START_BYTE, self.VERSION_BYTE, self.COMMAND_LENGTH, command, self.ACKNOWLEDGE,parameter1, parameter2, highByte, lowByte, self.END_BYTE]])

        self.uart.write(toSend)
        sleep_ms(self.COMMAND_LATENCY)
        return self.uart.read()

    def queryBusy(self):
        return not self.playerBusy.value()
        
        # DFPlayer control commands
    def nextTrack(self):
        self.sendcmd(0x01, 0x00, 0x00)

    def prevTrack(self):
        self.sendcmd(0x02, 0x00, 0x00)

    def increaseVolume(self):
        self.sendcmd(0x04, 0x00, 0x00)

    def decreaseVolume(self):
        self.sendcmd(0x05, 0x00, 0x00)

    def setVolume(self, volume):
        # Volume can be between 0-30
        self.sendcmd(0x06, 0x00, volume)

    def setEQ(self, eq):
        #eq can be o-5
        #0=Normal
        #1=Pop
        #2=Rock
        #3=Jazz
        #4=Classic
        #5=Base

        self.sendcmd(0x07, 0x00, eq)

    def setPlaybackMode(self, mode):
        #Mode can be 0-3
        #0=Repeat
        #1=Folder Repeat
        #2=Single Repeat
        #3=Random
        self.sendcmd(0x08, 0x00, mode)
                                
    def setPlaybackSource(self, source):
        #Source can be 0-4
        #0=U
        #1=TF
        #2=AUX
        #3=SLEEP
        #4=FLASH
        self.sendcmd(0x09, 0x00, source)

    def standby(self):
        self.sendcmd(0x0A, 0x00, 0x00)

    def normalWorking(self):
        self.sendcmd(0x0B, 0x00, 0x00)

    def reset(self):
        self.sendcmd(0x0C, 0x00, 0x00)

    def resume(self):
        self.sendcmd(0x0D, 0x00, 0x00)

    def pause(self):
        self.sendcmd(0x0E, 0x00, 0x00)

    def playTrack(self, folder, file):
        self.sendcmd(0x0F, folder, file)
                 
    def playMP3(self, filenum):
        a = (filenum >> 8) & 0xff
        b = filenum & 0xff
        return self.sendcmd(0x12, a, b)#a, b)

    # Query System Parameters
    def init(self, params):
        self.sendcmd(0x3F, 0x00, params)

# Constants. Change these if DFPlayer is connected to other pins.
UART_INSTANCE=0
TX_PIN = 0
RX_PIN=1
BUSY_PIN=9
                          
# Create player instance
player = DFPlayer(UART_INSTANCE, TX_PIN, RX_PIN, BUSY_PIN)
    
# Default values
def_vol = 15
def_eq = 0 

# Iterate by track number
i = 1

def first_track():
    global i
    if player.queryBusy() is False:
        print('nothing playing, lets change that')
        player.playTrack(1,i)
        
        
def next_track():
    global i
    print('playing next song...')
    player.playTrack(1,i)
    
def pre_main():
    player.setVolume(def_vol)
    player.setEQ(def_vol)
    first_track()
    main_loop()


def main_loop():
    
    while True:
    
        if player.queryBusy() is False:
            global i
            i += 1
            print('next one...')
            next_track()
        elif player.queryBusy() is True:
            sleep_ms(100)
        
pre_main()
