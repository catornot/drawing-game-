import socket
import threading
from _thread import start_new_thread
import sys
import pickle , time

import pygame
import random
from PIL import Image
from server_functions import *
from PSI import *

global breakall,kick
breakall=False
kick=False

def Thread_client(conn, playernum):  #clinet manager
	global chosen
	conn.send(pickle.dumps(['',False,False,started,False,None,False]))
	Protocol = PIS(conn)
	bytesBuffer=2048
	vote=''
	while True:

		try:
			data_recv = pickle.loads(conn.recv(bytesBuffer))#was 2048
			
			if type(data_recv) == list:
				print('received from:',playernum,' ;',data_recv)
				hold_drawer_state=playersData[playernum][1]
				hold_draw_state=playersData[playernum][4]
				hold_voter_state=playersData[playernum][2]
				hold_voter_darwer_state=playersData[playernum][6]
				playersData[playernum] = data_recv
				playersData[playernum][1]=hold_drawer_state
				playersData[playernum][4]=hold_draw_state
				playersData[playernum][3] = started
				playersData[playernum][6]=hold_voter_darwer_state
				playersData[playernum][2]=hold_voter_state

				if not data_recv or breakall or kick:
					print('Disconnected')
					break

				if data_recv[5]!=None and data_recv[5]!='' and playersData[playernum][1] and playersData[playernum][4] and playersData[playernum][6]:
					if len(votes)-1 >= int(data_recv[5]):
						print(chosen)
						chosen=int(data_recv[5])
						print(chosen)
						playersData[playernum][6]=False
						data_recv[5]=None

				elif data_recv[5]==None and data_recv[5]==''and playersData[playernum][1] and playersData[playernum][4] and playersData[playernum][6]:
					pass

				elif data_recv[5]!=None and data_recv[5]!=''and not playersData[playernum][1] and data_recv[2]:
					votes.append(data_recv[5])
					vote=data_recv[5]
					playersData[playernum][2]=False


				elif len(playersData) > 1 and not playersData[playernum][1]: 
					for name in playersData.keys():
						if playersData[name][4]:
							playersData[playernum][2]=True
							if data_recv[5]!=None:
								playersData[playernum][5]=None

				if vote in votes:
					playersData[playernum][2]=False

				conn.sendall(pickle.dumps(playersData[playernum]))
					
			else:
				bytesBuffer,state,sent=Protocol.run(data_recv)
				conn.sendall(pickle.dumps(sent))
				playersData[playernum][4]=state
				print(playersData[playernum][4])


		except:
			break
	try:
		conn.sendall(pickle.dumps(None))
	except:
		pass
	print('lost connection')
	playersData.pop(playernum)
	conn.close()

playersData = {}

currentPlayer = 0

started=False

next_p = 0

global votes #must be rest1
chosen=''
votes= []

def server_thread():
	server = "192.168.0.189"
	# server = socket.gethostbyname(socket.gethostname())
	print("host local ip :",server)
	port = 5555

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		s.bind((server, port))
	except socket.error as e:
		print(str(e))

	s.listen(4)
	print('waiting for connection, server started')


	while True:
		conn, addr = s.accept()
		print("connected to :", addr)

		if breakall:
			server.shutdown(socket.SHUT_RDWR)

		global currentPlayer,playersData,started,next_p,chosen

		start_new_thread(Thread_client, (conn,currentPlayer))

		playersData[currentPlayer] = ['',False,False,started,False,None,False]

		time.sleep(0.5)

		currentPlayer = currentPlayer + 1

def assingner():
	global chosen, votes, started, next_p , kick
	if len(playersData) > 1: #assings the role drawer to the right player try at least it dosen't work >:( wasn't :)
		there_is=False
		for name in playersData.keys():
			if playersData[name][1]:
				there_is=True

		print('next_p : ',next_p,'len(playersData): ',len(playersData))
		if not there_is and started and next_p == len(playersData):
			started=False
			chosen=''
			votes= []
			next_p=0
			kick=True
			time.sleep(1)
			kick=False
		if len(list(playersData.keys())) > next_p:
				next_key=list(playersData.keys())[next_p]
				if not there_is and started and next_p != 0:
					playersData[next_key][1]=True
					if chosen!='' and votes!=[]: # don't jugde me this is here to debug if this gets in the end product that means I didn't remove 
						chosen=''
					chosen=''
					votes= []

				elif next_p == 0 and started:
					playersData[next_key][1]=True
					if chosen!='' and votes!=[]:
						chosen=''
					chosen=''
					votes= []
		else:
			started=False
			chosen=''
			votes= []
			next_p=0
			kick=True
			time.sleep(1)
			kick=False

def pygame_start():
	print('turn off firewall!')
	pygame.init()
	screen=pygame.display.set_mode((1200,800))
	# infoObject = pygame.display.Info()
	# screen = pygame.display.set_mode((infoObject.current_w-360, infoObject.current_h-200),pygame.FULLSCREEN)
	pygame.display.set_caption('draw2! server')
	font = pygame.font.SysFont("Arial", 24)

	GREEN=(0,255,0)
	GRAY=(192,192,192)

	keep_going= True
	did=False
	timer= pygame.time.Clock()
	global currentPlayer,playersData,started,chosen,next_p

	while keep_going:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				keep_going= False
				time.sleep(1)

		
		there_is=False
		for name in playersData.keys():
			if playersData[name][1]:
				there_is=True

		there_is2=False
		for name in playersData.keys():
			if playersData[name][4]:
				there_is2=True

		there_is3=False
		for name in playersData.keys():
			if playersData[name][6]:
				there_is3=True

		if not started:
			to_run=start_menu(GREEN,GRAY,screen,font,playersData)
			started=to_run.run() #runs the right screen sceen
			assingner() #assignes drawer role to the right player
			did=False
		elif started and there_is and not there_is2:
			to_run=waiting_for(screen,font,playersData)
			to_run.run() #runs the right screen sceen
			did=False
		elif started and there_is and there_is2 and not there_is3 and type(chosen)!= int:
			to_run=ShowImageAndVotes(screen,font,playersData,votes)
			DoVote=to_run.run() #runs the right screen sceen
			for name in playersData.keys():
				if playersData[name][1]:
					playersData[name][6]=DoVote

		elif started and there_is and there_is2 and there_is3 and type(chosen)!= int:
			to_run=ShowImageAndPossibilitys(screen,font,playersData,votes)
			to_run.run() #runs the right screen sceen

		elif started and there_is and there_is2 and there_is3 and type(chosen)!= int:
			to_run=ShowImageAndPossibilitys(screen,font,playersData,votes)
			to_run.run() #runs the right screen sceen

		elif type(chosen)== int: #why it doesn't work I am out will continue tomorrow on 11/25/20 ok it does but what about assingner()?
			to_run=EndVotes(screen,font,playersData,votes,chosen)
			next_2=to_run.run()
			if next_2:
				hold_name=None
				for name in playersData.keys():
					if playersData[name][1]:
						hold_name=name

				if hold_name!=None and not did:
					playersData[hold_name][6]=False
					playersData[hold_name][4]=False
					playersData[hold_name][1]=False
					myfile = open("image.jpg", 'rb')
					bytess = myfile.read()
					myfile.close()
					try:
						name=votes[int(chosen)]
						name=name.replace(" ", "_").replace("/", "").replace("\\", "")
						myfile = open("server_imgs/{0}.jpg".format(name.replace("?", "").replace(".", "").replace(",", "")), 'wb')
						myfile.write(bytess)
						myfile.close()
					except:
						pass
					next_p = next_p + 1
					assingner() #assignes drawer role to the right player
					did=True

				elif hold_name!=None and did:
					playersData[hold_name][6]=False
					playersData[hold_name][4]=False
					playersData[hold_name][1]=False
					myfile = open("image.jpg", 'rb')
					bytess = myfile.read()
					myfile.close()
					try:
						name=votes[int(chosen)]
						name=name.replace(" ", "_").replace("/", "").replace("\\", "")
						myfile = open("server_imgs/{0}.jpg".format(name.replace("?", "").replace(".", "").replace(",", "")), 'wb')
						myfile.write(bytess)
						myfile.close()
					except:
						pass
					assingner() #assignes drawer role to the right player
					did=True


		 
		pygame.display.update()
		time.sleep(0.4)
	global breakall
	breakall=True
	pygame.quit()
	sys.exit()

start_new_thread(server_thread,())
start_new_thread(pygame_start,())
while True:
	if breakall:
		break
	time.sleep(5)
sys.exit()