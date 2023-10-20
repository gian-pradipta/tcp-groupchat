import subprocess
import os

command = 'python server.py'
command2 =  "python -m pyftpdlib -w -i 192.168.1.7 -p 8000 -u hello -P 12345678"


p1 = subprocess.Popen(command)
p2 = subprocess.Popen(command2)

try:
    p1.wait()
    p2.wait()
except KeyboardInterrupt:
    try:
       p1.terminate()
       p2.terminate
    except OSError:
       pass
    p1.wait()
    p2.wait()