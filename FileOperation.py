def Write_Mutual_Exclusion_Result_In_File(mode, obj): # write outout of mutual exclusion order in file
    File = None

    if(mode == "Arbitrary"):
        File = open(obj.Mututal_Exclusion_Result_File,'a')
    else:
        File = open(obj.Mututal_Exclusion_Result_File,'w')
    
    File.write("Using " + mode + " order of channel\n")
    File.write("Processes Requests with Timestamp and process (Tsi,i)\n")
    for Tsi_id in obj.Request_Clock_List:
        File.write(str(Tsi_id) + '\n')
    obj.Request_Clock_List.clear()


    File.write("\nCorrect Order of processes to execute critical section is:\n")
    while(obj.Request_Clock_Queue.qsize()):
        File.write(str(obj.Request_Clock_Queue.get()[1]) + '\n')


    File.write("\nActual Order of processes to execute critical section is:\n")
    for Process in obj.Execution_List:
        File.write(str(Process) + '\n')
    obj.Execution_List.clear()

    File.write('\n\n')

    File.close()

def Write_Result_In_File(mode_of_channel, obj): # write FiFO / Arbitrary message delivery guarantee result in file
    File = None

    if(mode_of_channel == "Arbitrary"):
        File = open(obj.Arbitrary_Result_File,'w')
    else:
        File = open(obj.FIFO_Result_File,'w')
    
    File.write("Order of message processed\n\n")

    for Message in obj.Execution_List:
        File.write(Message + '\n')

    obj.Execution_List.clear()
    File.write('\n\n')

    File.close()