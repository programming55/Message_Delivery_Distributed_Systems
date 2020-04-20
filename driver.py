import time
import Node1
import Node2

node_mapping = {"Node1": Node1, "Node2": Node2}


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
                    node_mapping[sender].send(receiver,message,"FIFO")
                    time.sleep(2)
                # line  = inp.readline()
                # [sender, receiver, message] = line.split(",")
                # Node2.send(receiver,message,"FIFO")