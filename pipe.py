from morse import morse_code, morse_code_reverse
try:
    from machine import Pin
except ImportError:
    class Pin:
        OUT = None
        def __init__(self, pin_no, mode): pass
        def on(self): pass
        def off(self): pass


class Consumer:
    pass

class OutputStream(Consumer):
    def __call__(self, iterable):
        self._last_iterable = list(iterable)
        for val in self._last_iterable:
            self.write(val)
        self.flush()
        return self._last_iterable

    def write(self, val):
        raise Exception("Not implemented")

    def flush(self):
        raise Exception("Not implemented")
    
    def __gt__(self, other):
        if isinstance(other, InputStream):
            buffer = []

            class Collector(OutputStream):
                def write(self2, val):
                    buffer.append(val)
                def flush(self2):
                    pass

            collector = Collector()
            collector(self._last_iterable)

            morse_str = ''.join(buffer).strip()
            return Pipe(morse_str.split(' ')) | other

        raise Exception("Right-hand side must be an InputStream")

class InputStream(Consumer):
    def __call__(self, iterable):
        return iterable

class StdIn(InputStream):
    def __init__(self, iterable=None):
        self._buffer = list(iterable) if iterable is not None else []

    def __call__(self, iterable=None):
        if iterable is not None:
            self._buffer = list(iterable)
        return self._buffer

class StdOut(OutputStream):
    # ANSI code for blinking start and reset
    BLINK_ON = "\033[5m"
    BLINK_OFF = "\033[0m"

    def write(self, val):
        # wrap each printed character in blink on/off codes
        print(f"{self.BLINK_ON}{val}{self.BLINK_OFF}", end="")

    def flush(self):
        # print newline with blinking effect
        print(f"{self.BLINK_ON}\n{self.BLINK_OFF}", end="")

# New classes with identical functionality but hardware LED blink
class LedOut(OutputStream):
    """
    Acts like StdOut but also blinks an on-board LED on the ESP32 for each write/flush.
    """
    def __init__(self, pin_no=2):  # default to built-in LED pin
        self.led = Pin(pin_no, Pin.OUT)
        # reuse ANSI blink codes for console output
        self.BLINK_ON = StdOut.BLINK_ON
        self.BLINK_OFF = StdOut.BLINK_OFF

    def write(self, val):
        # hardware blink on
        self.led.on()
        # console blink output
        print(f"{self.BLINK_ON}{val}{self.BLINK_OFF}", end="")
        # hardware blink off
        self.led.off()

    def flush(self):
        # hardware blink on
        self.led.on()
        # console blink newline
        print(f"{self.BLINK_ON}\n{self.BLINK_OFF}", end="")
        # hardware blink off
        self.led.off()

class LdrIn(InputStream):
    """
    Identical to StdIn (named for LED driver input consistency).
    """
    def __init__(self, iterable=None):
        self._buffer = list(iterable) if iterable is not None else []

    def __call__(self, iterable=None):
        if iterable is not None:
            self._buffer = list(iterable)
        return self._buffer

class Pipe:
    def __init__(self, stream):
        if isinstance(stream, str):
            self.stream = list(stream)
        elif isinstance(stream, (list, tuple)):
            self.stream = list(stream)
        else:
            self.stream = [stream]

    def __or__(self, step):
        if isinstance(step, Consumer):
            result = step(self.stream)
            return Pipe(result)
        else:
            processed = [step(x) for x in self.stream]
            return Pipe(processed)
    
    def __call__(self, consumer):
        return consumer(self.stream)

def to_upper(c):
    return c.upper()

def to_lower(c):
    return c.lower()

def to_morse(c):
    return morse_code.get(c.upper(), '?') + ' '

def from_morse(c):
    return ''.join(morse_code_reverse.get(code, '?') for code in c.split())

def shift(n):
    def inner(c):
        return chr(ord(c) + n)
    return inner