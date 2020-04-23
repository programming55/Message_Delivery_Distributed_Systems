import socket       # For TCP connections
from _thread import start_new_thread
import threading    # For handling communication with multiple nodes
from concurrent.futures import ThreadPoolExecutor
import random
import time
from queue import PriorityQueue

class Node:
	def __init__(self, total_nodes, IP, node_to_port_dic, current_node, driver_object):
		self.ip_addr = IP
		self.node_to_port = node_to_port_dic
		self.Total_Nodes = total_nodes
		self.Request_Queue = PriorityQueue()
		self.Recv_Counter = 0
		self.Clock = 0
		self.mode = "FIFO"
		self.MSG_ID = 0
		self.msg_resend_counter = {}
		self.resend_messages = {}
		self.ack_expected = {}
		self.curr_node = current_node
		self.driver = driver_object

	def start(self):
		t1 = start_new_thread(self.recv,()) # Receiving service is running in background
		# print(self.curr_node, " is up")

	def clear_ack(self):
		self.msg_resend_counter = {}
		self.resend_messages = {}
		self.ack_expected ={}
		self.MSG_ID = 0

	def ack_timer(self, Message_ID, msg):
	    start = time.time()
	    seconds = 100
	    elapsed = 0
	    while elapsed < seconds:
	        elapsed = time.time() - start
	        time.sleep(2)

	    if int(Message_ID) in self.ack_expected and self.ack_expected[int(Message_ID)]:
	        if int(Message_ID) in self.ack_expected and len(self.ack_expected[int(Message_ID)]) == 0:
	            del self.ack_expected[int(Message_ID)]
	        else:
	            if Message_ID not in self.msg_resend_counter:
	                self.msg_resend_counter[Message_ID] = 1
	            else:
	                self.msg_resend_counter[Message_ID] += 1

	            if self.msg_resend_counter[Message_ID] > 3:
	                for node in self.ack_expected[int(Message_ID)]:
	                    if node not in self.resend_messages:
	                        self.resend_messages[node] = [msg]
	                    else:
	                        self.resend_messages[node].append(msg)
	            else:
	                    for node in self.ack_expected[int(Message_ID)]:
	                        self.send(node, msg, self.mode)
	                    start_new_thread(self.ack_timer, (Message_ID, msg))

	def node_recv(self, conn, rip, rport):
	    ack = "received"
	    data = conn.recv(1024).decode()

	    TimeStamp, Id, Message_ID, Type_of_Message  = data.split(' ')

	    self.Clock = max(self.Clock, int(TimeStamp))
	    self.Clock += 1

	    if(Type_of_Message == 'Request'):
	        self.Request_Queue.put((int(TimeStamp), Id))
	        self.Clock += 1
	        msg = str(self.Clock) + " " + self.curr_node + " " + str(Message_ID) + " Reply" 
	        self.send(Id, msg, self.mode)
	        if int(Message_ID) in self.ack_expected:
	            self.ack_expected[int(Message_ID)].append(Id)
	        else:
	            self.ack_expected[int(Message_ID)] = [Id]
	        start_new_thread(self.ack_timer, (int(Message_ID), msg))

	    elif(Type_of_Message == 'Reply'):
	        self.Recv_Counter += 1
	        self.Clock += 1
	        msg = str(self.Clock) + " " + self.curr_node + " " + str(Message_ID) + " ACK_Reply"
	        self.send(Id, msg, self.mode)

	    elif(Type_of_Message == 'Release'):
	        self.Clock += 1
	        msg = str(self.Clock) + " " + self.curr_node + " " + str(Message_ID) + " ACK_Release"
	        self.send(Id, msg, self.mode)
	        self.Request_Queue.get()

	    elif "ACK" in Type_of_Message:
	        if int(Message_ID) in self.ack_expected and  Id in self.ack_expected[int(Message_ID)]:
	            self.ack_expected[int(Message_ID)].remove(Id)

	    else:
	    	self.driver.Execution_List.append(self.curr_node + str(": Received message: " + Type_of_Message + " from address " + str(rip) + " : " + str(rport)) + "\n")
	    	self.Clock += 1
	    	msg = str(self.Clock) + " " + self.curr_node + " " + str(Message_ID) + " ACK_Other"
	    	self.send(Id, msg, self.mode)
	    	self.driver.counter += 1

	    conn.close()
	    return data

	def recv(self): # To receive message in background using thraad
	    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    sock.bind((self.ip_addr,self.node_to_port[self.curr_node]))
	    sock.listen()

	    while (True):
	        conn,(rip,rport)  = sock.accept()
	        self.Clock += 1
	        start_new_thread(self.node_recv, (conn,rip,rport)) # Accepting multiple request in parallel using thread
	    
	    sock.close()


	def node_send(self, node, msg):
	    port = self.node_to_port[node]
	    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    sock.connect((self.ip_addr,port))

	    if self.mode == "Arbitrary": # For arbitrart channel, introducing random delay in each message send to make messages out of order
	        delay = random.randrange(5)
	        if delay:
	            time.sleep(delay)

	    sock.sendall(msg.encode())

	    TimeStamp, Id, Message_ID, Type_of_Message = msg.split(' ')
	    if Type_of_Message not in ['Request', 'Reply', 'Release']:
	        if int (Message_ID) in self.ack_expected:
	            self.ack_expected[int(Message_ID)].append(node)
	        else:
	            self.ack_expected[int(Message_ID)] = [node]

	    sock.close()

	def send(self, node, msg, mode_recv): # send message which internally use node_send function
	    self.mode = mode_recv
	    if self.mode == "Arbitrary": # Use of thread to send all arbitrart message in parallel with random delay to introduce out of order receiving
	        start_new_thread(self.node_send, (node,msg))
	    else:
	        self.node_send(node,msg)

	def critical_section(self, mode_recv): # Call when process need critical section. Every cs execution will run in parallel.
	    self.mode = mode_recv
	    start_new_thread(self.cs,())

	def get_counter(self): # send counter value
		return self.driver.counter

	def clr_counter(self): # clear counter value
		self.driver.counter = 0

	def cs(self):
   		self.Clock = 0
   		self.Recv_Counter = 0

   		# Broadcasting Request

   		self.Clock += 1
   		
   		self.Request_Queue.put((self.Clock, self.curr_node))
   		self.driver.Request_Clock_Queue.put((self.Clock, self.curr_node))
   		self.driver.Request_Clock_List.append((self.Clock, self.curr_node))

   		time.sleep(3)

   		self.MSG_ID += 1
   		msg = str(self.Clock) + " " + self.curr_node + " " + str(self.MSG_ID) + " Request"

   		if(self.curr_node == "Node1" and self.mode == "Arbitrary"): # This is introduct to make special case where Lmaport fail in Arbitrary channel.
   			time.sleep(5)

   		for Id in range(self.Total_Nodes):
   			Node = "Node" + str(Id + 1)
   			if(Node != self.curr_node):
   				self.send(Node, msg, self.mode)

   		#Wait for Critical Section

   		Req_Top = None
   		Req_Top = self.Request_Queue.get()
   		self.Request_Queue.put(Req_Top)
   		Counter = self.Recv_Counter

   		while(Req_Top[1] != self.curr_node or Counter < self.Total_Nodes - 1):
   			time.sleep(1)
   			Req_Top =self. Request_Queue.get()
   			self.Request_Queue.put(Req_Top)
   			Counter = self.Recv_Counter

   		self.Recv_Counter -= self.Total_Nodes - 1
   		# Critical Section Entry

   		self.driver.Execution_List.append("Executing critical section of "+ self.curr_node)
   		time.sleep(10)
   		self.driver.Execution_List.append("Exiting critical section of "+ self.curr_node)

   		# Critical Section Exit

   		# Broadcasting Release

   		if not self.Request_Queue.empty():
   			self.Request_Queue.get()
   		self.Clock += 1
   		self.MSG_ID += 1

   		msg = str(self.Clock) + " " + self.curr_node + " " + str(self.MSG_ID) + " Release"
   		if int(self.MSG_ID) not in self.ack_expected:
   			self.ack_expected[int(self.MSG_ID)] = []

   		for Id in range(self.Total_Nodes):
   			Node = "Node" + str(Id + 1)
   			if(Node != self.curr_node):
   				self.send(Node, msg, self.mode)
   				self.ack_expected[int(self.MSG_ID)].append(Node)

   		start_new_thread(self.ack_timer, (self.MSG_ID, msg))
   		self.driver.counter += 1