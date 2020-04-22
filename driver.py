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

Request_Clock_Queue = PriorityQueue() # To store critical section requests in correct order

Request_Clock_List = [] # To store critical section requests in actual order
Execution_List = [] # Execution order of critical section entry and exit record

Mututal_Exclusion_Result_File = "Mutual_Execlusion_Result"
FIFO_Result_File = "FIFO_Result"
Arbitrary_Result_File = "Arbitrary_Result"

if __name__ == "__main__":
    while (True):
        print("Press 1 to simulate FIFO message delivery guarantee")
        print("Press 2 to simulate Arbitrary message delivery guarantee")
        print("Press 3 to measure impact on Lamport's Mutual Exclusion Algorithm")
        print("Press 4 to quit simulation")
        choice = int(input())

        if choice == 4:
            print("Exiting Simulation...")
            break

        elif choice == 1: # To simulate FIFO message delivery
            Total_Send_Recv = 0
            Node5.clr_counter()

            with open("FIFO_test.csv", "r") as inp:
                id = 1
                for line in inp:
                    [sender, receiver, message] = line.split(",")
                    node_mapping[sender].send(receiver,"1 " + sender + " " + str(id) + " " + message.rstrip() , "FIFO")
                    id += 1
                    Total_Send_Recv += 1
            
            while(Node5.get_counter() < Total_Send_Recv):
            	time.sleep(2)
            	continue

            Node5.Write_Result_In_File("FIFO")

        elif choice == 2: # To simulate Arbitrary message delivery
            Total_Send_Recv = 0
            Node5.clr_counter()

            with open("FIFO_test.csv", "r") as inp:
                id = 1
                for line in inp:
                    [sender, receiver, message] = line.split(",")
                    node_mapping[sender].send(receiver,"1 " + sender + " " + str(id) + " " + message.rstrip() , "Arbitrary")
                    id += 1
                    Total_Send_Recv += 1
            
            while(Node5.get_counter() < Total_Send_Recv):
            	time.sleep(2)
            	continue

            Node5.Write_Result_In_File("Arbitrary")

        elif choice == 3:
        	Total_Send_Recv = 0 # To measure impact on Lamport's Mutual Exclusion Algorithm on FIFO channel
        	Node5.clr_counter()

        	with open("ME_Test.csv", "r") as inp:
        		for Node in inp:
        			node_mapping[Node.rstrip()].critical_section("FIFO")
        			Total_Send_Recv += 1


        	while(Node5.get_counter() < Total_Send_Recv):
        		time.sleep(2)
        		continue

        	Node1.Write_Mutual_Exclusion_Result_In_File()
        	
        	Total_Send_Recv = 0 # To measure impact on Lamport's Mutual Exclusion Algorithm on Arbitrary channel
        	Node1.clr_counter()

        	with open("ME_Test.csv", "r") as inp:
        		for Node in inp:
        			node_mapping[Node.rstrip()].critical_section("Arbitrary")
        			Total_Send_Recv += 1

        	while(Node1.get_counter() < Total_Send_Recv):
        		time.sleep(2)
        		continue

        	Node1.Write_Mutual_Exclusion_Result_In_File()

        else:
            print("Wrong Input...")