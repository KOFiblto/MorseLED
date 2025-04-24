import pipe

pipe.Pipe("Hallo") | pipe.to_morse | pipe.LedOut() | pipe.LdrIn() | pipe.from_morse | pipe.LedOut()

