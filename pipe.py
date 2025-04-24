from morse import morse_code, morse_code_reverse

class Consumer:
    pass

class OutputStream(Consumer):
    def __call__(self, iterable):
        self._last_iterable = list(iterable)
        for val in self._last_iterable:
            self.write(val)
        self.flush()

    def write(self, val):
        raise Exception("Not implemented")

    def flush(self):
        raise Exception("Not implemented")
    
    def __gt__(self, other):
        if isinstance(other, InputStream):
            buffer = []

            # Unsichtbarer Datenfänger
            class Collector(OutputStream):
                def write(self2, val):
                    buffer.append(val)
                def flush(self2):
                    pass  # Unterdrücke Flush, da nur Pufferung benötigt wird

            # Trick: Führe die bisherige Pipeline aus, aber sammle die Ausgabe
            collector = Collector()
            collector(self._last_iterable)  # Verarbeite den gespeicherten Datenstrom

            # Morse-Code-Teile zu einem String zusammenfügen
            morse_str = ''.join(buffer).strip()

            # Weiterleitung an die nächste Pipeline (z. B. StdIn)
            return Pipe(morse_str.split(' ')) | other  # Pipe mit dem gesammelten Morse-String

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
        return iter(self._buffer)

class StdOut(OutputStream):
    def write(self, val):
        print(val, end="")

    def flush(self):
        print()

class Pipe:
    def __init__(self, stream):
        self.stream = stream if isinstance(stream, (list, tuple)) else [stream]

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
