# This tool is for educational purposes only.
# Only scan systems you have permission to test.
import sys
import socket
from concurrent.futures import ThreadPoolExecutor
import time

start_time = time.time()
found = False

if len(sys.argv) !=4 :
    print("Usage: python3 scanner.py <TARGET> <START_PORT> <END_PORT>")
    sys.exit()

target = sys.argv[1]

try:
    start_port = int(sys.argv[2])
    end_port = int(sys.argv[3])

except ValueError:
    print("Error : Ports must be numeric values")
    sys.exit()

if not(0<=start_port<=65535 and 0<=end_port<=65535):
    print("Error : Ports must be in range 0-65535")
    sys.exit()

if start_port>end_port:
    print("Error: START_PORT cannot be greater than END_PORT")
    sys.exit()

try :
    address = socket.gethostbyname(target)

except socket.gaierror:
    print("Error : Unable to resolve hostname")
    sys.exit()

print("="*70)
print("🔍 PORT SCANNER TOOL ".center(70))
print("="*70)

print(f"Target : {address}")
print(f"Port range : {start_port}-{end_port}")

def scan_port(port):
    global found
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((address,port))

    if result == 0:
        print("Port ",port," is open")
        found = True

    s.close()

with ThreadPoolExecutor(max_workers=200) as executor:
    list(executor.map(scan_port,range(start_port,end_port+1)))

end_time = time.time()

if not found:
    print("No open Ports found !!!")

print(f"Time elapsed : {end_time - start_time:.2f} seconds")