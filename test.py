import socket

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
print(f"Local IP: {local_ip}")