import pipe

pipe.Pipe("Hallo") | pipe.to_morse | pipe.StdOut() | pipe.StdIn() | pipe.from_morse | pipe.LedOut()


"""


            pipe.Pipe("Hallo")        |           pipe.to_morse          |  pipe.StdOut()  |  pipe.StdIn()  |  pipe.from_morse  |  pipe.LedOut()
REIN:             ["Hallo"]               ["H"]["A"]["L"]["L"]["L"]["o"]       [".--."]         ["."]["-"]          [".--."]         ["Hallo"]
RAUS: ["H"]["A"]["L"]["L"]["L"]["o"]                  [".--."]                ["."]["-"]         [".--."]          ["Hallo"]
""" 
