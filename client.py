import socket
import threading
import time
import os
from ftplib import FTP
# Choosing Nickname
server = input("Server asal: ")
nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server, 55555))

# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break

# Upload File to server
def upload_file(filename) :
    ftp = FTP()
    ftp.connect(server, 8000)
    ftp.login("hello", "12345678")
    try:
        with open(filename, 'rb') as file:
            ftp.storbinary(f'STOR {filename}', file)
    except:
        print("Upload Error")
    ftp.quit()

def download_file(filename):
    ftp = FTP()
    ftp.connect(server, 8000)
    ftp.login("hello", "12345678")
    try:
        with open(filename, 'wb') as file:
            ftp.retrbinary(f'RETR {filename}', file.write)
    except:
        print("download error")
    ftp.quit()
# Sending Messages To Server
def show_dir ():
    files_and_directories = os.listdir('.')
    list_files = '\n'.join(files_and_directories)
    client.send(list_files.encode('utf-8'))
    print(list_files)
def write(pesan):
    # while True:
    message = '>> {}: {}'.format(nickname, pesan)
    client.send(message.encode('utf-8'))

def send() :
    while True:
        pesan = input()
        write(pesan)
        message_split = pesan.split(";")
        if message_split[0] == '!upload':
            upload_file(message_split[-1])
        if message_split[0] == '!download':
            download_file(message_split[-1])
        if message_split[0] == '!dir':
            show_dir()
# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=send)
write_thread.start()