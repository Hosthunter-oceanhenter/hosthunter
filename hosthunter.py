#!/usr/bin/env python3
import socket
import threading
from queue import Queue

print("""
================================
  𝙃𝙤𝙨𝙩𝙝𝙪𝙣𝙩𝙚𝙧 
        Host Scanner
================================
""")

input_file = input("Input file  : ")
output_file = input("Output file : ")
threads = int(input("Threads     : "))

ports = [80, 443]
queue = Queue()
lock = threading.Lock()

def scan(host):
    try:
        ip = socket.gethostbyname(host)
    except:
        return

    for port in ports:
        s = socket.socket()
        s.settimeout(2)
        try:
            s.connect((ip, port))
            status = "open"
        except:
            status = "closed"
        s.close()

        with lock:
            result = f"{status:<12}{ip:<16}{host:<14}{port}"
            print(result)
            with open(output_file, "a") as f:
                f.write(result + "\n")

def worker():
    while not queue.empty():
        host = queue.get()
        print(f"processing   {host}")
        scan(host)
        queue.task_done()

with open(input_file, "r") as f:
    for line in f:
        queue.put(line.strip())

print(f"\n{'status':<12}{'ip':<16}{'domain':<14}port")

for _ in range(threads):
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()

queue.join()
print("\nScan completed ✅")