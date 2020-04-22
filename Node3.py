import socket       # For TCP connections
from _thread import start_new_thread
import threading    # For handling communication with multiple nodes
from concurrent.futures import ThreadPoolExecutor
import random
import time
from queue import PriorityQueue
import driver

node_to_port = {"Node1": 9001, "Node2": 9002, "Node3": 9003, "Node4": 9004, "Node5": 9005, "Node6": 9006, "Node7": 9007, }
# node_to_port = {"Node1": 8001, "Node2": 8002, "Node3": 8003, "Node4": 8004, "Node5": 8005, "Node6": 8006, "Node7": 8007, }
ip_addr = "127.0.0.1"

# out_lock = threading.Lock()

Request_Queue = PriorityQueue()
Recv_Counter = 0
Clock = 0
Total_Nodes = 6

mode = "FIFO"

def node_recv(conn,rip,rport):
    global Clock
    global Recv_Counter
    ack = "received"

    data = conn.recv(1024).decode()
    TimeStamp, Id, Type_of_Message = data.split(' ')

    Clock = max(Clock, int(TimeStamp))
    Clock += 1

    if(Type_of_Message == 'Request'):
        Request_Queue.put((int(TimeStamp), Id))
        Clock += 1
        msg = str(Clock) + " Node3 Reply"
        send(Id, msg, mode) # get mode
    elif(Type_of_Message == 'Reply'):
        Recv_Counter += 1
    elif(Type_of_Message == 'Release'):
        Request_Queue.get()
    else:
        print("Received message:", Type_of_Message, "from address",rip,":",rport)
        driver.Increment_Counter()
        # print(driver.counter)

    conn.close()
    return data

def recv():
    global Clock

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip_addr,node_to_port["Node3"]))
    sock.listen()

    while (True):
        conn,(rip,rport)  = sock.accept()
        Clock += 1
        start_new_thread(node_recv, (conn,rip,rport))
    
    sock.close()

def node_send(node, msg):
    port = node_to_port[node]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip_addr,port))

    if mode == "Arbitrary":
        delay = random.randrange(10)
        if delay:
            time.sleep(delay)
            # print("Introducing delay of ", delay, " seconds")

    sock.sendall(msg.encode())
    sock.close()


t1 = start_new_thread(recv,())

def send(node, msg, mode_recv):
    global mode
    mode = mode_recv
    if mode == "Arbitrary":
        start_new_thread(node_send, (node,msg))
    else:
        node_send(node,msg)

def critical_section(mode_recv):
    global mode
    mode = mode_recv
    start_new_thread(cs,())

def get_counter():
    return driver.counter

def clr_counter():
    return driver.Clear_Counter()

def cs():
    global Recv_Counter
    global Clock

    Clock = 0
    Recv_Counter = 0

    # time.sleep(random.randrange(10))
    # Broadcasting Request

    Clock += 1
    Request_Queue.put((Clock, "Node3"))
    msg = str(Clock) + " Node3 Request"
    time.sleep(1) 
    for Id in range(Total_Nodes):
        Node = "Node" + str(Id + 1)
        if(Node != "Node3"):
            send(Node, msg, mode)


    # Wait for Critical Section

    Req_Top = None
    Req_Top = Request_Queue.get()
    Request_Queue.put(Req_Top)
    # print(Req_Top)
    Counter = Recv_Counter

    while(Req_Top[1] != "Node3" or Counter < Total_Nodes - 1):
        time.sleep(1)
        Req_Top = Request_Queue.get()
        Request_Queue.put(Req_Top)
        Counter = Recv_Counter
        # print(Req_Top, Counter)
    
    # Critical Section

    Recv_Counter -= Total_Nodes - 1
    print("Executing critical section of Node3")
    time.sleep(15)
    print("Exiting critical section of Node3")

    # Broadcasting Release

    Request_Queue.get()
    Clock += 1
    msg = str(Clock) + " Node3 Release"
    
    for Id in range(Total_Nodes):
        Node = "Node" + str(Id + 1)
        if(Node != "Node3"):
            send(Node, msg, mode)

    driver.Increment_Counter()
    # driver.counter = 10
    # print(driver.counter)