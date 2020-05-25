import socket, select
import datetime

MAX_CONNECTIONS = 10   # стільки дескрипторів одночасно можуть бути відкриті
INPUTS = list()        #  Список дескрипторів для отримання даних по дескрипторам.
OUTPUTS = list()       #  Список дескрипторів для відправки даних по дескрипторам.
EXCEPTIONS = list()

messageForSocket = {}  #  port:message

list_sender = ['Відправник :']
list_recepient = ['Адресат :']
list_message = ['Повідомлення :']
list_time = ['Час :']
list_mark = ['Статус :']
list_of_lists = [list_sender, list_recepient, list_message, list_time]

server_host = 'localhost'
server_port = '8800'
serverAddress = (server_host, int(server_port))



def handling_OutputEvents(writeList):
    # Подія виникає, коли в буфері на запис звільняється місце.
    for client in writeList:
        try:
            IP, port = getClientIP(client)
            answer = messageForSocket[port]
            answer = bytes(answer, encoding='UTF-8')
            sent = client.send(answer)

            print("Відправлено відповідь.")
            deleteClientConnection(client)
        except OSError:
            printLog(unitName, NumLine(), '###  Error: handling_OutputEvents  ###')
            deleteClientConnection(client)

def getClientIP(client):
    s = str(client)
    s = s.split("'")
    IP, port = ' ', ' '
    if len(s) == 5:
        IP = s[3]
        port = s[4][2:-2]
    return IP, port


def deleteClientConnection(client):
    """ Очистка ресурсів сокета """

    IP, port = getClientIP(client)
    if client in OUTPUTS:
        if port in messageForSocket:
            del messageForSocket[port]
        OUTPUTS.remove(client)
    if client in INPUTS:
        INPUTS.remove(client)
    print('connection:  ' + str(IP) + ' ' + str(port) + '  closed')
    print("---------------------------=====-----------------")

    client.close()

def getClientHTTP(client):
    requestData = ""
    IP, port = getClientIP(client)
    if IP == ' ' or port == ' ':
        return "deleted_client_connection"
    print('connection:  ' + str(IP) + ' ' + str(port))
    try:
        requestData = client.recv(1024)
        print()
        print(requestData)
        if requestData:
            if client not in OUTPUTS:
                OUTPUTS.append(client)  # запись дескриптора сокета в список возврата
        else:
            deleteClientConnection(client)
            requestData = "deleted_client_connection"
        #----
    except ConnectionResetError:
        print('closed by remote host')
        deleteClientConnection(client)
        requestData = "  ConnectionResetError "
    return requestData

def appendTime():
    time_now = datetime.datetime.now()
    time_now = str(time_now)
    x = time_now.find('.')
    time_now = time_now[0:x]
    list_time.append(time_now)

def appendMessage(msg, i):
    compare = 1
    list_mark[i] = "old"
    msg = msg + '\n Time: ' + list_time[i] + \
          '/From user: ' + list_sender[i] + \
          '/for user: ' + list_recepient[i] + \
          '/message: ' + list_message[i]
    return compare, msg


def createMessage(sender, recepient):
    msg = ''
    compare = 0
    for i in range(0, len(list_recepient)):
        if list_recepient[i] == sender:
            if recepient == "_new":
                if list_mark[i] == "New":
                    compare, msg = appendMessage(msg, i)
            else:
                compare, msg = appendMessage(msg, i)
    return compare, msg


def getRequest(client):
    # Переривання на наповнення вхідного буфера.
    requestData = getClientHTTP(client)
    requestData = str(requestData)
    requestData = requestData[2:-2]
    requestData = requestData.split('/')
    #print(":", requestData)
    return requestData



    ##################################################################################
def WriteInList(list_of_lists, requestData):
    list_sender, list_recepient, list_message, list_time = list_of_lists
    appendTime()
    list_mark.append("New")
    list_sender.append(requestData[0])
    list_recepient.append(requestData[1])
    list_message.append(requestData[2])

    list_of_lists = [list_sender, list_recepient, list_message, list_time]
    return list_of_lists

def handling_InputEvents(readList, serverSocket, list_of_lists):
    requestData = ''
    for client in readList:
        IP, port = getClientIP(client)
        if client is serverSocket:
            # Подія від серверного сокета - нове підключеня
            connection, client_address = client.accept()
            connection.setblocking(0)
            INPUTS.append(connection)
        else:
            # parsing:
            requestData = getRequest(client)
            sender = requestData[0]
            recepient = requestData[1]
            #------------------------------------------------------------------
            # append lists:
            if (recepient != '_new') and (recepient != '_all'):
                list_of_lists = WriteInList(list_of_lists, requestData)
            #------------------------------------------------------------------
            # form back msg:
            compare, msg =  createMessage(sender, recepient)
            #------------------------------------------------------------------
            # 'send' msg:
            if compare == 0:
                messageForSocket[port] = 'No messages for you.'
            else:
                messageForSocket[port] = msg
            print("Повідомлення для відповіді сформовано :", messageForSocket[port])
            #------------------------------------------------------------------
            print()
            print(list_sender)
            print(list_recepient)
            print(list_message)
            print(list_time)
            print(list_mark)
            print()

    return list_of_lists

def createNonBlockingServerSocket(serverAddress):
    # Створення сокету, який працює без блокування основного потоку.
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setblocking(0)
    serverSocket.bind(serverAddress)      # Бінд сервера на потрібну адресу і порт
    serverSocket.listen(MAX_CONNECTIONS)  # Установка максимальної кількості конектів.
    return serverSocket

def runServer(serverAddress, list_of_lists):
    serverSocket = createNonBlockingServerSocket(serverAddress)
    INPUTS.append(serverSocket)
    #----------------------------------------------
    while True:
        readList, writeList, _ = select.select(INPUTS, OUTPUTS, [], 0)
        handling_OutputEvents(writeList)
        list_of_lists = handling_InputEvents(readList, serverSocket, list_of_lists)
    #----------------------------------------------
    print("Роботу сервера зупинено!")


if __name__ == '__main__':

    print("-----------------------------------------------")
    print("   Server address:   "+ server_host +':'+ server_port)
    #print("   Start path:       "+ serverPath))
    print("-- press ESC to stop ---------------------------")
    runServer(serverAddress, list_of_lists)
##########################################################