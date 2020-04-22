import time
import Node1
import Node2
import Node3
import Node4
import Node5
import Node6
from queue import PriorityQueue

node_mapping = {"Node1": Node1, "Node2": Node2, "Node3": Node3, "Node4": Node4, "Node5": Node5, "Node6": Node6}
counter = 0
total_nodes = 6
Request_Clock_Queue = PriorityQueue()
Request_Clock_List = []
Execution_List = []
Mututal_Exclusion_Result_File = "Mutual_Execlusion_Result"

def Write_In_Mututal_Exclusion_Result_File(Mode):
	File = open(Mututal_Exclusion_Result_File,'w')
	
	File.write("Using " + Mode + " order of channel")
	File.write("Processes Requests with Timestamp and process (Tsi,i)")

	for Tsi_id in Request_Clock_List:
		File.write(Tsi_id)

	File.write("\nCorrect Order of processes to execute critical section is:")
	while(Request_Clock_Queue.qsize()):
		File.write(Request_Clock_Queue.get()[1])

	File.write("\nActual Order of processes to execute critical section is:")
	for Process in Execution_List:
		File.write(Process)

	File.close()
# # def Print_Queue():
# 	print(Request_Clock_Queue.qsize())

# def Print_Request_Clock_List():
# 	print(Request_Clock_List)

# def Print_Execution_List():
# 	print(Execution_List)

def Push_Request_Clock_Queue(tuple):
	global Request_Clock_Queue
	Request_Clock_Queue.put(tuple)

def Append_Request_Clock_List(tuple):
	global Request_Clock_List
	Request_Clock_List.append(tuple)

def Append_Execution_List(Process):
	global Append_Execution_List
	Execution_List.append(Process)

def Increment_Counter():
	global counter
	counter += 1

def Clear_Counter():
	global counter
	counter = 0

if __name__ == "__main__":
    while (True):
        print("Press 1 to simulate FIFO message delivery guarantee")
        print("Press 2 to simulate Arbitrary message delivery guarantee")
        print("Press 3 to measure impact on Lamport's Mutual Exclusion Algorithm")
        print("Press 4 to measure impact on Ricarta-Agrawal's Mutual Exclusion Algorithm")
        print("Press 5 to quit simulation")
        choice = int(input())

        if choice == 5:
            print("Exiting Simulation...")
            break

        elif choice == 1:
            Total_Send_Recv = 0
            Node1.clr_counter()
            with open("FIFO_test.csv", "r") as inp:
                for line in inp:
                    [sender, receiver, message] = line.split(",")
                    # print(sender,receiver,message)
                    node_mapping[sender].send(receiver,"1 " + sender + " " + message.rstrip(),"FIFO")
                    Total_Send_Recv += 1
            
            # print(Total_Send_Recv)
            while(Node1.get_counter() < Total_Send_Recv):
            	continue
                    # time.sleep(2)

                # line  = inp.readline()
                # [sender, receiver, message] = line.split(",")
                # Node2.send(receiver,message,"FIFO")

        elif choice == 2:
            Total_Send_Recv = 0
            Node1.clr_counter()
            with open("FIFO_test.csv", "r") as inp:
                for line in inp:
                    [sender, receiver, message] = line.split(",")
                    node_mapping[sender].send(receiver,"1 " + sender+ " " + message.rstrip(),"Arbitrary")
                    Total_Send_Recv += 1
            
            while(Node1.get_counter() < Total_Send_Recv):
            	continue
                    # time.sleep(2)

        elif choice == 3:
        	Total_Send_Recv = 0
        	Node1.clr_counter()
        	with open("ME_Test.csv", "r") as inp:
        		for Node in inp:
        			node_mapping[Node.rstrip()].critical_section("FIFO")
        			Total_Send_Recv += 1


        	while(Node1.get_counter() < Total_Send_Recv):
        		continue

        	Node6.Write_Mutual_Exclusion_Result_In_File()
        	# Node1.Node_Print_Queue_Size()
        	# Node1.Node_Print_Request_Clock_List()
        	# Node1.Node_Print_Execution_List()
        	# print(Request_Clock_List)
        	# print(Execution_List)

        	Total_Send_Recv = 0
        	Node6.clr_counter()

        	with open("ME_Test.csv", "r") as inp:
        		for Node in inp:
        			node_mapping[Node.rstrip()].critical_section("Arbitrary")
        			Total_Send_Recv += 1

        	while(Node6.get_counter() < Total_Send_Recv):
        		time.sleep(2)
        		continue

        	Node6.Write_Mutual_Exclusion_Result_In_File()
        else:
            print("Exiting Simulation...")
            break

            