
from machine import ADC
from machine import Pin


class Relay():

    def __init__(self, pin):
        self.relaypin = Pin(pin, Pin.OUT)
        self.last_status = 1

    def set_state(self, state):
        self.relaypin.value(state)
        self.last_status = state
