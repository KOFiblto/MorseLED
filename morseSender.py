import time
from machine import Pin
from morse import morse_code

class MorseSender:
    def __init__(self, pinNumber, speed):
        self.pin = Pin(pinNumber, Pin.OUT)
        self.speed = speed
        
        #Functions
        self.blink = lambda duration: (self.pin .on(), time.sleep(duration), self.pin .off(), time.sleep(duration))
        self.short_blink = lambda: (self.blink(self.speed), print(".", end=""))
        self.long_blink = lambda: (self.blink(self.speed * 3), print("-", end=""))
        self.zeichen_delay = lambda: time.sleep(self.speed)
        self.letter_delay = lambda: time.sleep(self.speed * 3)
        self.space_delay = lambda: (self.pin .off(), time.sleep(self.speed * 7), print(" ", end=""))
        
        self.blinker = {'.': self.short_blink, '-': self.long_blink, '/': self.space_delay}

    #Blink a single Letter
    def transmitLetter(self, letter):
        letter = letter.upper()
        if letter in morse_code:
            print(letter, end= "")
            print(": ", end="")
            for i in morse_code[letter]:
                self.blinker[i]()
                    
                self.zeichen_delay()
            self.letter_delay()
            
    #Blink a whole Text
    def transmitText(self, text):
        for letter in text:
            self.transmitLetter(letter)
            print()
    
