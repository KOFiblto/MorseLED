from machine import Pin
import time
from morse import morse_code

led = Pin(18, Pin.OUT)
speed = 1

class Morse_blinker:
    def __init__(self, pinNumber, speed):
        self.led = Pin(pinNumber, Pin.OUT)
        
        #Functions
        self.blink = lambda duration: (self.led.on(), time.sleep(duration), self.led.off(), time.sleep(duration))
        self.short_blink = lambda: (self.blink(self.led, self.speed), print(".", end=""))
        self.long_blink = lambda: (self.blink(self.led, self.speed * 3), print("-", end=""))
        self.zeichen_delay = lambda: time.sleep(self.speed)
        self.letter_delay = lambda: time.sleep(self.speed * 3)
        self.space_delay = lambda: (self.led.off(), time.sleep(self.speed * 7), print(" ", end=""))
        
        #
        self.blinker = {'.': self.short_blink, '-': self.long_blink, '/': self.space_delay}


    def blink_morse_letter(self, letter):
        letter = letter.upper()
        if letter in morse_code:
            print(letter, end= "")
            print(": ", end="")
            for i in morse_code[letter]:
                self.blinker[i]()
                    
                self.zeichen_delay()
            self.letter_delay()
    
        
        
    def blink_morse_text(self, text):
        for letter in text:
            self.blink_morse_letter(letter)
            print();
    
    


# Main
mb = Morse_blinker(18, speed)
mb.blink_morse_text("Hallo Welt")

















