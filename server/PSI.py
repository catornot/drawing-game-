import pickle
class PIS():
	def __init__(self,conn):
		self.conn=conn

	def run(self,msg):
		if type(msg) == str:
			if msg=='PSI':
				return 2048,False,'continue'
			else:
				return 2048,False,''
		elif type(msg)==int:
			return msg*2,False,'GOT'
		elif type(msg)==bytes:
			myfile = open("server_imgs/img.jpg", 'wb')
			myfile.write(msg)
			myfile.close()
			return 2048,True,'GOT'