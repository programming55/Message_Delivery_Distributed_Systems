import socket       # For TCP connections
from _thread import start_new_thread
import threading    # For handling communication with multiple nodes
from concurrent.futures import ThreadPoolExecutor
import random
import time

node_to_port = {"Node1": 8001, "Node2": 8002, "Node3": 8003, "Node4": 8004, "Node5": 8005, "Node6": 8006, "Node7": 8007, }
ip_addr = "127.0.0.1"

data_received = []

out_lock = threading.Lock()

# send_args = []


def node_recv(conn,rip,rport):
    ack = "received"
    # while(True):
    #     data = conn.recv(1024)
    #     if not data:
    #         conn.sendall(ack.encode())
    #         break
    #     # data = reversed(data)
    data = conn.recv(1024)
    conn.sendall(ack.encode())
    out_lock.acquire()
    print("Received message:", data, "from address",rip,":",rport)
    out_lock.release()
    data_received.append(data)
    conn.close()

def recv():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip_addr,node_to_port["Node2"]))
    sock.listen()
    while (True):
        conn,(rip,rport)  = sock.accept()
        start_new_thread(node_recv, (conn,rip,rport))
    
    sock.close()


def node_send(node, msg, mode):
    # node = send_args[0]
    # msg = send_args[1]
    # mode = send_args[2]
    port = node_to_port[node]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip_addr,port))
    # if mode == "FIFO":
    #     sock.sendall(msg.encode())
    #     # while True:
    #     #     ack = sock.recv(1024)
    #     #     if not ack:
    #     #         break
    #     print("Acknowledgement received from",ip_addr,":",port)

    if mode == "Arbitrary":
        delay = random.randrange(10)
        if delay:
            time.sleep(delay)
            print("Introducing delay of ", delay, " seconds")

    sock.sendall(msg.encode())


t1 = threading.Thread(target=recv)
executor = ThreadPoolExecutor(100)

def send(node, msg, mode):
    # global send_args
    # send_args.append(node)
    # send_args.append(msg)
    # send_args.append(mode)
    # t2 = executor.submit(node_send,(node,msg,mode))
    node_send(node,msg,mode)

def critical_section():
    print("Executing critical section of Node 1")

if __name__ == "__main__":
    t1.start()
    t1.join()
