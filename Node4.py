import socket       # For TCP connections
from _thread import start_new_thread
import threading    # For handling communication with multiple nodes
from concurrent.futures import ThreadPoolExecutor
import random
import time
from queue import PriorityQueue
import driver

node_to_port = {"Node1": 9001, "Node2": 9002, "Node3": 9003, "Node4": 9004, "Node5": 9005, "Node6": 9006, "Node7": 9007, }
ip_addr = "127.0.0.1"
Nodes = ["Node4", "Node2", "Node3", "Node4", "Node5", "Node6", "Node7"]
# out_lock = threading.Lock()


Request_Queue = PriorityQueue()
Recv_Counter = 0
Clock = 0
Total_Nodes = 6
mode = "FIFO"
MSG_ID = 0
ack_required = {}
ack_received = {}
msg_resend_counter = {}
resend_messages = {}

def ack_timer(Message_ID, msg):
    global  ack_required
    global msg_resend_counter
    global resend_messages

    start = time.time()
    seconds = 50
    elapsed = 0
    while elapsed < seconds:
        elapsed = time.time() - start
        time.sleep(2)

    if ack_required[Message_ID] == 0:
        del ack_required[Message_ID]
    else:
        if Message_ID not in msg_resend_counter:
            msg_resend_counter[Message_ID] = 1
        else:
            msg_resend_counter1[Message_ID] += 1

        if msg_resend_counter[Message_ID] > 3:
            for node in ack_received:
                if node not in resend_messages:
                    resend_messages[node] = [msg]
                else:
                    resend_messages[node].append(msg)
        else:
            start_new_thread(ack_timer, (Message_ID, msg))

def node_recv(conn,rip,rport):
    global Clock
    global Recv_Counter
    global ACK_Received
    global ack_required
    global ack_received
    global mode
    
    ack = "received"
    data = conn.recv(1024).decode()
    print(data)
    TimeStamp, Id, Message_ID, Type_of_Message  = data.split(' ')

    Clock = max(Clock, int(TimeStamp))
    Clock += 1

    if(Type_of_Message == 'Request'):
        Request_Queue.put((int(TimeStamp), Id))
        Clock += 1
        msg = str(Clock) + " Node4 " + str(Message_ID) + " Reply" 
        send(Id, msg, mode) # get mode
        ack_required[Message_ID] = 1
        start_new_thread(ack_timer, (Message_ID, msg))

    elif(Type_of_Message == 'Reply'):
        Recv_Counter += 1
        Clock += 1
        msg = str(Clock) + " Node4 " + str(Message_ID) + " ACK_Reply"
        send(Id, msg, mode)

    elif(Type_of_Message == 'Release'):
        Clock += 1
        msg = str(Clock) + " Node4 " + str(Message_ID) + " ACK_Release"
        send(Id, msg, mode)
        Request_Queue.get()

    elif "ACK" in Type_of_Message:
        print("ACK received from ", Id, "for message id ", Message_ID, " ACK_TYPE ", Type_of_Message)
        ack_required[Message_ID] -= 1
        if Message_ID in ack_received:
            ack_received[Message_ID].append(Id)
        else:
            ack_received[Message_ID] = [Id]

    else:
        print("Received message:", Type_of_Message, "from address",rip,":",rport)
        Clock += 1
        msg = str(Clock) + " Node4 " + str(Message_ID) + " ACK_Other"
        send(Id, msg, mode)
        driver.Increment_Counter()
        # print(driver.counter)


    conn.close()
    return data

def recv():
    global Clock

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip_addr,node_to_port["Node4"]))
    sock.listen()

    while (True):
        conn,(rip,rport)  = sock.accept()
        Clock += 1
        start_new_thread(node_recv, (conn,rip,rport))
    
    sock.close()

def node_send(node, msg):
    global ack_required

    port = node_to_port[node]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip_addr,port))
    if mode == "Arbitrary":
        delay = random.randrange(5)
        if delay:
            time.sleep(delay)
            # print("Introducing delay of ", delay, " seconds")
    sock.sendall(msg.encode())

    TimeStamp, Id, Message_ID, Type_of_Message = msg.split(' ')
    if Type_of_Message not in ['Request', 'Reply', 'Release']:
        ack_required[Message_ID] = 1

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

def Write_Mutual_Exclusion_Result_In_File():
    File = None
    if(mode == "Arbitrary"):
        File = open(driver.Mututal_Exclusion_Result_File,'a')
    else:
        File = open(driver.Mututal_Exclusion_Result_File,'w')
    
    File.write("Using " + mode + " order of channel\n")
    File.write("Processes Requests with Timestamp and process (Tsi,i)\n")

    for Tsi_id in driver.Request_Clock_List:
        File.write(str(Tsi_id) + '\n')

    driver.Request_Clock_List.clear()
    File.write("\nCorrect Order of processes to execute critical section is:\n")
    while(driver.Request_Clock_Queue.qsize()):
        File.write(str(driver.Request_Clock_Queue.get()[1]) + '\n')

    File.write("\nActual Order of processes to execute critical section is:\n")
    for Process in driver.Execution_List:
        File.write(str(Process) + '\n')

    driver.Execution_List.clear()
    File.write('\n\n')
    File.close()

def get_counter():
    return driver.counter

def clr_counter():
    return driver.Clear_Counter()

def cs():
    global Recv_Counter
    global Clock
    global MSG_ID
    global ack_required

    Clock = 0
    Recv_Counter = 0

    # time.sleep(random.randrange(10))
    # Broadcasting Request

    Clock += 1
    Request_Queue.put((Clock, "Node4"))
    driver.Append_Request_Clock_List((Clock, "Node4"))
    driver.Push_Request_Clock_Queue((Clock, "Node4"))
    MSG_ID += 1
    msg = str(Clock) + " Node4 " + str(MSG_ID) + " Request"
    if(mode == "Arbitrary"):
        time.sleep(5)

    for Id in range(Total_Nodes):
        Node = "Node" + str(Id + 1)
        if(Node != "Node4"):
            send(Node, msg, mode)


    # Wait for Critical Section

    Req_Top = None
    Req_Top = Request_Queue.get()
    Request_Queue.put(Req_Top)
    # print(Req_Top)
    Counter = Recv_Counter

    while(Req_Top[1] != "Node4" or Counter < Total_Nodes - 1):
        time.sleep(1)
        Req_Top = Request_Queue.get()
        Request_Queue.put(Req_Top)
        Counter = Recv_Counter
        # print(Req_Top, Counter)
    
    # Critical Section

    Recv_Counter -= Total_Nodes - 1
    driver.Append_Execution_List("Executing critical section of Node4")
    # print("Executing critical section of Node2")
    time.sleep(10)
    driver.Append_Execution_List("Exiting critical section of Node4")

    # Broadcasting Release

    Request_Queue.get()
    Clock += 1
    MSG_ID += 1
    msg = str(Clock) + " Node4 " + str(MSG_ID) + " Release"
    ack_required[MSG_ID] = Total_Nodes - 1
    start_new_thread(ack_timer, (Message_ID, msg))    
    for Id in range(Total_Nodes):
        Node = "Node" + str(Id + 1)
        if(Node != "Node4"):
            send(Node, msg, mode)

    driver.Increment_Counter()
    # driver.counter = 10
    # print(driver.counter)