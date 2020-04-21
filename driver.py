import time
import Node1
import Node2
import Node3
import Node4
import Node5
import Node6

node_mapping = {"Node1": Node1, "Node2": Node2, "Node3": Node3, "Node4": Node4, "Node5": Node5, "Node6": Node6}
counter = 0
total_nodes = 6

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
            with open("FIFO_test.csv", "r") as inp:
                for line in inp:
                    [sender, receiver, message] = line.split(",")
                    # print(sender,receiver,message)
                    node_mapping[sender].send(receiver,"1 " + sender + " " + message.rstrip(),"FIFO")
                    # time.sleep(2)
                # line  = inp.readline()
                # [sender, receiver, message] = line.split(",")
                # Node2.send(receiver,message,"FIFO")

        elif choice == 2:
            with open("FIFO_test.csv", "r") as inp:
                for line in inp:
                    [sender, receiver, message] = line.split(",")
                    node_mapping[sender].send(receiver,"1 " + sender+ " " + message.rstrip(),"Arbitrary")
                    # time.sleep(2)

        elif choice == 3:
        	Node1.clr_counter()
        	with open("ME_Test.csv", "r") as inp:
        		for Node in inp:
        			node_mapping[Node.rstrip()].critical_section("FIFO")

        	while(Node1.get_counter() < 6):
        		continue

        	Node1.mode = "Arbitrary"
        	Node2.mode = "Arbitrary"
        	Node3.mode = "Arbitrary"
        	Node4.mode = "Arbitrary"
        	Node5.mode = "Arbitrary"
        	Node6.mode = "Arbitrary"

        	Node1.clr_counter()
        	with open("ME_Test.csv", "r") as inp:
        		for Node in inp:
        			node_mapping[Node.rstrip()].critical_section("Arbitrary")

        	while(Node1.get_counter() < 6):
        		continue
            # while(counter)
        	# with open("ME_Test.csv", "r") as inp:
         #        for Node in inp:
         #            node_mapping[Node.rstrip()].critical_section("Arbitrary")

        else:
            with open("ME_Test.csv", "r") as inp:
                for Node in inp:
                    
                    # print(sender,receiver,message)
                    # print(Node.rstrip())
                    node_mapping[Node.rstrip()].critical_section("Arbitrary")
                    # time.sleep(2)''

            