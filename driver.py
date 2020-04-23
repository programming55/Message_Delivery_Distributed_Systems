import time
from queue import PriorityQueue
import FileOperation
import Node


class CommonLists:
    def __init__(self):
        self.counter = 0
        self.total_nodes = 6
        self.node_to_port = {"Node1": 8001, "Node2": 8002, "Node3": 8003, "Node4": 8004, "Node5": 8005, "Node6": 8006, "Node7": 7007, }
        self.Request_Clock_Queue = PriorityQueue() # To store critical section requests in correct order
        self.Request_Clock_List = [] # To store critical section requests in actual order
        self.Execution_List = [] # Execution order of critical section entry and exit record
        self.Mututal_Exclusion_Result_File = "Mutual_Execlusion_Result.txt"
        self.FIFO_Result_File = "FIFO_Result.txt"
        self.Arbitrary_Result_File = "Arbitrary_Result.txt"

driver_obj = CommonLists()

def start_nodes():
    Node1 = Node.Node(driver_obj.total_nodes, "127.0.0.1", driver_obj.node_to_port, "Node1", driver_obj)
    Node2 = Node.Node(driver_obj.total_nodes, "127.0.0.1", driver_obj.node_to_port, "Node2", driver_obj)
    Node3 = Node.Node(driver_obj.total_nodes, "127.0.0.1", driver_obj.node_to_port, "Node3", driver_obj)
    Node4 = Node.Node(driver_obj.total_nodes, "127.0.0.1", driver_obj.node_to_port, "Node4", driver_obj)
    Node5 = Node.Node(driver_obj.total_nodes, "127.0.0.1", driver_obj.node_to_port, "Node5", driver_obj)
    Node6 = Node.Node(driver_obj.total_nodes, "127.0.0.1", driver_obj.node_to_port, "Node6", driver_obj)
    return Node1, Node2, Node3, Node4, Node5, Node6

if __name__ == "__main__":
    Node1, Node2, Node3, Node4, Node5, Node6 = start_nodes()
    Node1.start()
    Node2.start()
    Node3.start()
    Node4.start()
    Node5.start()
    Node6.start()

    node_mapping = {"Node1": Node1, "Node2": Node2, "Node3": Node3, "Node4": Node4, "Node5": Node5, "Node6": Node6}
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
            Node1.clear_ack()
            Node2.clear_ack()
            Node3.clear_ack()
            Node4.clear_ack()
            Node5.clear_ack()
            Node6.clear_ack()
            Total_Send_Recv = 0
            Node5.clr_counter()

            with open("Channel_test.csv", "r") as inp:
                id = 1
                for line in inp:
                    [sender, receiver, message] = line.split(",")
                    node_mapping[sender].send(receiver,"1 " + sender + " " + str(id) + " " + message.rstrip() , "FIFO")
                    id += 1
                    Total_Send_Recv += 1
            
            while(Node5.get_counter() < Total_Send_Recv):
                time.sleep(2)
                continue

            FileOperation.Write_Result_In_File("FIFO", driver_obj)

        elif choice == 2: # To simulate Arbitrary message delivery
            Node1.clear_ack()
            Node2.clear_ack()
            Node3.clear_ack()
            Node4.clear_ack()
            Node5.clear_ack()
            Node6.clear_ack()

            Total_Send_Recv = 0
            Node5.clr_counter()

            with open("Channel_test.csv", "r") as inp:
                id = 1
                for line in inp:
                    [sender, receiver, message] = line.split(",")
                    node_mapping[sender].send(receiver,"1 " + sender + " " + str(id) + " " + message.rstrip() , "Arbitrary")
                    id += 1
                    Total_Send_Recv += 1
            
            while(Node5.get_counter() < Total_Send_Recv):
                time.sleep(2)
                continue

            FileOperation.Write_Result_In_File("Arbitrary", driver_obj)

        elif choice == 3:
            Node1.clear_ack()
            Node2.clear_ack()
            Node3.clear_ack()
            Node4.clear_ack()
            Node5.clear_ack()
            Node6.clear_ack()
            Total_Send_Recv = 0 # To measure impact on Lamport's Mutual Exclusion Algorithm on FIFO channel
            Node5.clr_counter()

            with open("ME_Test.csv", "r") as inp:
                for Node in inp:
                    node_mapping[Node.rstrip()].critical_section("FIFO")
                    Total_Send_Recv += 1


            while(Node5.get_counter() < Total_Send_Recv):
                time.sleep(2)
                continue

            FileOperation.Write_Mutual_Exclusion_Result_In_File("FIFO", driver_obj)
            Node1.clear_ack()
            Node2.clear_ack()
            Node3.clear_ack()
            Node4.clear_ack()
            Node5.clear_ack()
            Node6.clear_ack()

            Total_Send_Recv = 0 # To measure impact on Lamport's Mutual Exclusion Algorithm on Arbitrary channel
            Node1.clr_counter()


            with open("ME_Test.csv", "r") as inp:
                for Node in inp:
                    node_mapping[Node.rstrip()].critical_section("Arbitrary")
                    Total_Send_Recv += 1

            while(Node1.get_counter() < Total_Send_Recv):
                time.sleep(2)
                continue

            FileOperation.Write_Mutual_Exclusion_Result_In_File("Arbitrary", driver_obj)

        else:
            print("Wrong Input...")