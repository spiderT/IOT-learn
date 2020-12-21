
from machine import ADC
from machine import Pin


class LightSensor():

    def __init__(self, pin):
        self.light = ADC(Pin(pin))

    def value(self):
        value = self.light.read()
        print("Light ADC value:", value)
        return int(value/4095*6000)
