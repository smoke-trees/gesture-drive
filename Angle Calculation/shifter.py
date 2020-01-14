import socket


### SERVER CODE
host = "127.0.0.1"
port = 20000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
print("Socket binded to post", port)
s.listen(5)
print("Socket is listening")

# If multiple listeners, add while True:
c, addr = s.accept()
print('Connected to :', addr[0], ':', addr[1])
while True:
    try:
        data = c.recv(1024)
        print(c.getpeername(), ': ', str(data)[2:-1])
        gesture = data.decode()
        # print(type(data))
        #print(type(int(data.decode())))
        print(gesture)
        #print(angle)
    except ConnectionResetError:
        print("Closing connection at shifter")
        s.close()
        break
    except ValueError:
        print("shifter here")
        continue
    #start_new_thread(threaded, (c,))


