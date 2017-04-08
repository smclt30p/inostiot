import serial


def checksum(data):
    check = 0
    for i in range(0, 31):
        if (data[i]) % 2 == 0:
            check += 1
    return check

def make_packet(string):
    data = []
    for i in string:
        data.append(ord(i))
    for i in range(0, 31 - len(data)):
        data.append(0)
    data.append(checksum(data))
    return data

def get_data(incoming):
    data = []
    for i in incoming:
        if i == 0: # null terminated
            string = ""
            for i in data:
                string += i
            return string
        data.append(chr(i))

if __name__ == "__main__":

    ser = serial.Serial("/dev/ttyUSB0", timeout=5)

    syn = ser.read(32)

    if checksum(syn) != syn[-1]:
        print("Checksum invalid")

    if get_data(syn) != "SYN":
        print("SYN invalid")

    ser.write(make_packet("ACK"))
    ser.write(make_packet("SYN"))

    ack = ser.read(32)

    if checksum(ack) != ack[-1]:
        print("ACK checksum invalid!")

    if get_data(ack) != "ACK":
        print("ACK invalid")


