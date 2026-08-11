from machine import ADC, Pin
import time

# samples for 20 ms, returns the average of the samples
def readNTC(NTCadc):
    startMs = time.ticks_ms()
    numOfSamples = 0
    ADCsum = 0

    while time.ticks_diff(time.ticks_ms(), startMs) < 20:
        ADCsum += NTCadc.read_u16()
        numOfSamples += 1

    return ADCsum / numOfSamples

def optoInterruptHandler(pin):
    global optoEvents1, optoEventIDX1, optoEvents2, optoEventIDX2, optoActive, optoEventBufferOverflow

    eventTimestamp = time.ticks_ms()

    if optoActive == 1:
        if optoEventIDX1 < 100:
            optoEvents1[optoEventIDX1] = eventTimestamp
            optoEventIDX1 += 1
        else:
            optoEventBufferOverflow = True
    else:
        if optoEventIDX2 < 100:
            optoEvents2[optoEventIDX2] = eventTimestamp
            optoEventIDX2 += 1
        else:
            optoEventBufferOverflow = True
            


NTC1 = ADC(Pin(26))
NTC2 = ADC(Pin(27))
NTC3 = ADC(Pin(28))

userLed1 = Pin(6, Pin.OUT) # indicates the overflow of the opto event buffer
userLed2 = Pin(10, Pin.OUT)

# contains the timestamps of optoevents in ms, max 100 events, if there is no more space but event occured user LED 1 indictaes it
optoEvents1 = [0] * 100
optoEvents2 = [0] * 100
optoEventIDX1 = 0
optoEventIDX2 = 0
# contains the number of the opto buffer which is currently written by handler
optoActive = 1
optoEventBufferOverflow = False

opto = Pin(15, Pin.IN)
opto.irq(trigger=Pin.IRQ_RISING, handler=optoInterruptHandler)

startOfMainloopMS = time.ticks_ms()

while True:
    # measuring temperature, and logging it
    NTC1_ADCval = readNTC(NTC1)
    NTC1_ADCvalMs = time.ticks_ms() - startOfMainloopMS - 10

    NTC2_ADCval = readNTC(NTC2)
    NTC2_ADCvalMs = time.ticks_ms() - startOfMainloopMS - 10

    NTC3_ADCval = readNTC(NTC3)
    NTC3_ADCvalMs = time.ticks_ms() - startOfMainloopMS - 10

    print(f"temperature|{NTC1_ADCval}#{NTC1_ADCvalMs}|{NTC2_ADCval}#{NTC2_ADCvalMs}|{NTC3_ADCval}#{NTC3_ADCvalMs}|end")

    # logging all the opto event timestamps
    if optoEventBufferOverflow == False:
        if optoActive == 1:
            optoActive = 2

            print("opto|", end = "")

            for i in range(0, optoEventIDX1):
                print(f"{optoEvents1[i] - startOfMainloopMS}|", end = "")

            print("end")

            optoEventIDX1 = 0
        else:
            optoActive = 1

            print("opto|", end = "")

            for i in range(0, optoEventIDX2):
                print(f"{optoEvents2[i] - startOfMainloopMS}|", end = "")

            print("end")

            optoEventIDX2 = 0
    else:
        userLed1.value(1)

        while(1):
            print("error|Opto event buffer overflow!")
            time.sleep_ms(1000)

    time.sleep_ms(1000)