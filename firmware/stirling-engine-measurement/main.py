from machine import ADC, Pin
import time
import math

# convert temperature from ADC
def convertTemperature(ADCvalue, R0, beta, rReference, T0):
    rNTC = (rReference) / ((65535/ADCvalue) - 1)

    temperature = 1 / ((1 / T0) + (1 / beta) * math.log(rNTC / R0))

    return temperature

# samples for 20 ms, returns the average of the samples
def readNTC(NTCadc):
    startMs = time.ticks_ms()
    numOfSamples = 0
    ADCsum = 0

    while time.ticks_diff(time.ticks_ms(), startMs) < 20:
        ADCsum += NTCadc.read_u16()
        numOfSamples += 1

    avgADC = ADCsum / numOfSamples

    return convertTemperature(avgADC, 10000, 3380, 3900, 298.15)

def optoInterruptHandler(pin):
    global firstInterruptReceived, lastInterruptMS, freqPacket

    if firstInterruptReceived == True:
        currentTimeMS = time.ticks_ms()

        if time.ticks_diff(currentTimeMS, lastInterruptMS) > 20:
            freq = 1 / (time.ticks_diff(currentTimeMS, lastInterruptMS) / 1000) # calculating freq (1 / sec)
    
            freqTimestamp = (currentTimeMS + lastInterruptMS) / 2 # timestamp for the freq, avg of the last and the current time
    
            lastInterruptMS = currentTimeMS
    
            freqPacket[0] = freqTimestamp
            freqPacket[1] = freq

            userLed1.toggle()
    else:
        lastInterruptMS = time.ticks_ms()
        firstInterruptReceived = True

        userLed1.toggle()
            

NTC1 = ADC(Pin(26))
NTC2 = ADC(Pin(27))
NTC3 = ADC(Pin(28))

userLed1 = Pin(4, Pin.OUT)
userLed2 = Pin(7, Pin.OUT)

firstInterruptReceived = False
lastInterruptMS = 0
freqPacket = [-1.0, -1.0] # timeMS, freq

opto = Pin(15, Pin.IN)
opto.irq(trigger=Pin.IRQ_RISING, handler=optoInterruptHandler)

while True:
    # measuring temperature
    userLed2.value(1)

    NTC1_temp = readNTC(NTC1)
    NTC1_tempMs = time.ticks_ms() - 10

    NTC2_temp = readNTC(NTC2)
    NTC2_tempMs = time.ticks_ms() - 10

    NTC3_temp = readNTC(NTC3)
    NTC3_tempMs = time.ticks_ms() - 10

    userLed2.value(0)

    print(f"start|{NTC1_temp}#{NTC1_tempMs}|{NTC2_temp}#{NTC2_tempMs}|{NTC3_temp}#{NTC3_tempMs}|{freqPacket[1]}#{freqPacket[0]}|stop")

    time.sleep_ms(1000)