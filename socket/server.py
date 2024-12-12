import socket
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = 'localhost'
port = 1234
server_socket.bind((host,port))
server_socket.listen(1)

conn,addr = server_socket.accept()
print('This guy connected -> '+str(addr))

while 1:
	message = conn.recv(1024).decode();
	print('some one send a message : ' + message)
	arr = message.split()
	response = ""
	if len(arr)>0 and arr[0]=="factorial":
		fact = 1
		num = int(arr[1])
		for i in range(1,num+1):
			fact = fact*i
		response = response + f' The factorial is {fact} '
	elif len(arr)>0 and arr[0] == "isPrime":
		flag = True
		num = int(arr[1])
		for i in range(2,num):
			if(num%i == 0):
				flag = False
		if flag:
			response += f'{num} is Prime'
		else:
			response += f'{num} is notPrime'
	else:
		response = 'Invalid query'
	conn.send(response.encode())
