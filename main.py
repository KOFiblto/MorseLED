from machine import Pin
import time
from morse import morse_code
from morseSender import MorseSender

led = Pin(18, Pin.OUT)
speed = 0.01


# Main
# ms = MorseSender(18, speed)
# ms.transmitText("Hallo Welt")


class data:
    def __init__(self, message):
        self.message = message

    def __or__(self, other):
        other.connect(self)
        return other

class translate:
    def __init__(self, type):
        self.__type = type
    
    def connect(self, other):
        self.partner = other

    def translate(self, letter):
        return letter.upper()

    def __or__(self, other):
        other.connect(self)
        for letter in self.partner.message:
            other.write(self.translate(letter))

class stream:
    def __init__(self, type):
        self.__type = type
        self.__message = None
    
    def connect(self, other):
        self.partner = other

    def write(self, letter):
        print(letter)

data("HalloWelt") | translate("Morse") | stream("stdout")








