import pipe

pipe.Pipe("Hallo") | pipe.to_morse | pipe.StdOut() | pipe.StdIn() | pipe.from_morse | pipe.StdOut()

