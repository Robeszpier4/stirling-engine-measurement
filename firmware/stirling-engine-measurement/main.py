from machine import ADC, Pin
import time

# samples for 20 ms, returns the average of the samples
def readNTC(NTCadc):
    startUs = time.ticks_us()
    numOfSamples = 0
    ADCsum = 0

    while time.ticks_us() - startUs < 20000:
        ADCsum += NTCadc.read_u16()
        numOfSamples += 1

    return ADCsum / numOfSamples

def optoInterruptHandler():
    print()

NTC1 = ADC(Pin(26))
NTC2 = ADC(Pin(27))
NTC3 = ADC(Pin(28))

userLed1 = Pin(6, Pin.OUT)
userLed2 = Pin(10, Pin.OUT)


while True:
    NTC1_ADCval = readNTC(NTC1)
    NTC1_ADCvalMs = time.ticks_ms()

    NTC2_ADCval = readNTC(NTC2)
    NTC2_ADCvalMs = time.ticks_ms()

    NTC3_ADCval = readNTC(NTC3)
    NTC3_ADCvalMs = time.ticks_ms()
