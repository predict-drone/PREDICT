import serial
import time
# ============================= Variables ==================================
message = [];
temp = [];
start = False
start_i = 1
start_check = False
start_lim = ['.','F','P','G','A','1'];
start_lim_n = len(start_lim)

end_lim = ['!'];
end_lim_n = len(end_lim)

dummy = False
i = 0
# ============================= Functions ==================================
# Function to convert
def listToString(s):

    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele

    # return string
    return str1

# ============================= MAIN ==================================
print('Hello world!')
ser = serial.Serial(port = "/dev/ttyUSB1", baudrate=9600, bytesize=8, timeout=0.2, stopbits=serial.STOPBITS_ONE)
while 1:
    print("Message nr",i)
    message_to_board = 'Hello Patmos!\n\r'
    ser.write(message_to_board.encode('utf-8'))
    i+=1
    time.sleep(1)

i = 0
while 1:
    print("Ready")
    data = ser.read(10)                        #read byte from serial device
    try:
        #data = data.decode('utf-8')              #decode message
        print(data)

        data = (data+"\x00").decode('utf-16-le')              #decode message

        print(data)
        print("\n")
        if (data==".")and(not start):
            start = True
            print("Appending\n")

        if (data =="!") and (start_check):
            print("--> Message: <--")
            print(listToString(message))
            # Analyse message here:
            print("\n--> End of message nr.",i,"<--")
            # Send message at the end:
            print("--> Sending a message <--")
            message_to_board = 'Hello Patmos!\n\r'
            ser.write(message_to_board.encode('utf-8'))
            message_to_board=''
            message.clear()
            temp.clear()
            start_check = False
            start = False
            dummy = False
            i+=1

        if start_check:
            message.append(data)
            #print(listToString(message))
            if (not dummy):
                print("Saving message.")
                dummy = True

        if start:
            temp.append(data)
            start_i+=1
            #check beginning
            if (len(temp)==start_lim_n)and(not start_check):
                start_check = (temp == start_lim)
                print(temp)
                print("Found start")
                print("Start check ",start_check)
                start = False
                temp.clear()

        time.sleep(.200)

    except:
        time.sleep(1)