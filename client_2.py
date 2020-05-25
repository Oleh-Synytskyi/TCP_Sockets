import socket
import threading
import sys
import os
from tkinter import *
import time

msg = '1234'
host = port = message = '---'

def sendMessage(host, port, message, time_out=0.05):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
    except:
        print("Could not make a connection to the server")
        sys.exit(0)
    sock.sendall(str.encode(message))
    global msg
    msg = sock.recv(1024)
    msg = str(msg)

    msg = msg[22:]
    print(msg)
    time.sleep(3)
    print('Client close')
    sock.close()
    return

def insertText():
    s = "  we are here"
    print(msg)
    text.insert(1.0, msg)
    return

def getButton_3(event):
    print("Button_3")

    #f1 = 'localhost'
    #f2 = 5555
    #f3 = 'client_2 says hello there'
    #f4 = 'client_2'
    #f5 = 'client_1'
    f1 = field_1.get()
    f2 = field_2.get()
    f3 = field_3.get()
    f4 = field_4.get()
    f5 = field_5.get()
    print("Host: ", f1)
    print("Port: ", f2)
    print("My name: ", f4)
    print("Adressee name: ", f5)
    print("Message: ", f3)
    if f1 != '' and f2 != '' and f3 != '':
        print("Усі поля заповнено.")
        host = f1
        #host = 'localhost'
        port = int(f2)
        #port = 5555
        myname = f4
        #myname = 'client_1'
        message = f4 + '/'+ f5 + '/' + f3 + '!'
        adress = f5
        #paket = myname + '/' + adress + '/'
        print("Message: ", message)
        sendMessage(host, port,  message)

def getButton_NEW(event):
    print("Button_NEW")
    #f1 = field_1.get()
    f1 = 'localhost'
    f2 = 5555
    f3 = 'client_2 says hello there'
    f4 = 'client_2'
    f5 = '_new'
    #f2 = field_2.get()
    #f3 = field_3.get()
    #f4 = field_4.get()
    #f5 = field_5.get()
    print("Host: ", f1)
    print("Port: ", f2)
    print("My name: ", f4)
    print("Adressee name: ", f5)
    print("Message: ", f3)
    if f1 != '' and f2 != '' and f3 != '':
        print("Усі поля заповнено.")
        #host = f1
        host = 'localhost'
        #port = int(f2)
        port = 8800
        myname = f4
        #myname = 'client_1'
        message = f4 + '/'+ f5 + '/' + f3 + '!'
        #adress = f5
        #paket = myname + '/' + adress + '/'
        print("Message: ", message)
        sendMessage(host, port,  message)
    #else:
    #print("Недостатньо даних.")


def getButton_ALL(event):
    print("Button_ALL")
    #f1 = field_1.get()
    f1 = 'localhost'
    f2 = 8800
    f3 = 'client_2 says hello there'
    f4 = 'client_2'
    f5 = '_all'
    #f2 = field_2.get()
    #f3 = field_3.get()
    #f4 = field_4.get()
    #f5 = field_5.get()
    print("Host: ", f1)
    print("Port: ", f2)
    print("My name: ", f4)
    print("Adressee name: ", f5)
    print("Message: ", f3)
    if f1 != '' and f2 != '' and f3 != '':
        print("Усі поля заповнено.")
        #host = f1
        host = 'localhost'
        #port = int(f2)
        port = 8800
        myname = f4
        #myname = 'client_1'
        message = f4 + '/'+ f5 + '/' + f3 + '!'
        #adress = f5
        #paket = myname + '/' + adress + '/'
        print("Message: ", message)
        sendMessage(host, port,  message)
    #else:
    #print("Недостатньо даних.")


#Wait for incoming data from server
#.decode is used to turn the message in bytes to a string
def receive(socket, signal):
    while signal:
        try:
            data = socket.recv(32)
            print(str(data.decode("utf-8")))
        except:
            print("You have been disconnected from the server")
            signal = False
            break

root = Tk()



#Get host and port
#host = input("Host: ")
#port = int(input("Port: "))
l1 = Label(text="Введіть адресу хоста", font=("Comic Sans MS", 10, "bold"))
l2 = Label(text="Введіть номер порта", font=("Comic Sans MS", 10, "bold"))
l3 = Label(text="Введіть своє повідомлення ", font=("Comic Sans MS", 10, "bold"))
l4 = Label(text="Введіть своє ім'я ", font=("Comic Sans MS", 10, "bold"))
l5 = Label(text="Введіть  ім'я адресата", font=("Comic Sans MS", 10, "bold"))
l6 = Label(text="Повідомлення для мене", font=("Comic Sans MS", 10, "bold"))

l1.config(bd=5, bg='#6BB5E7')
l2.config(bd=5, bg='#6BB5E7')
l3.config(bd=5, bg='#6BB5E7')
l4.config(bd=5, bg='#6BB5E7')
l5.config(bd=5, bg='#6BB5E7')
l6.config(bd=5, bg='#6BB5E7')


button_3 = Button(text="Надіслати")
button_3['bg'] = '#6BB5E7'
button_3['fg'] = '#000000'
field_1 = Entry(width=30)
field_2 = Entry(width=30)
field_3= Entry(width=30)
field_4= Entry(width=30)
field_5= Entry(width=30)

frame = Frame()
frame.pack()
button_NEW = Button(frame, text="NEW")
button_NEW['bg'] = '#6BB5E7'
button_NEW['fg'] = '#000000'

button_ALL = Button(frame, text="ALL")
button_ALL['bg'] = '#6BB5E7'
button_ALL['fg'] = '#000000'

button_3.bind('<Button-1>', getButton_3)
button_NEW.bind('<Button-1>', getButton_NEW)
button_ALL.bind('<Button-1>', getButton_ALL)

b_insert = Button(frame, text="GET", command=insertText)
b_insert['bg'] = '#6BB5E7'
b_insert['fg'] = '#000000'
b_insert.pack(side=RIGHT)

l1.pack(side = TOP)
field_1.pack()

l2.pack()
field_2.pack()

l4.pack()
field_4.pack()

l6.pack()

text = Text(width=35, height=10)
text.pack()

#frame = Frame()
#frame.pack()

label = Label()
label.pack(side = BOTTOM)



l5.pack()
field_5.pack()
#frame.pack()
l3.pack()
field_3.pack()
button_NEW.pack(side=LEFT)

button_ALL.pack(side=RIGHT)
button_3.pack()
root.mainloop()