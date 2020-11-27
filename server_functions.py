import pygame

class start_menu():
	def __init__(self,GREEN,GRAY,screen,font,PlayersData):
		self.GREEN=GREEN
		self.GRAY=GRAY
		self.screen=screen
		self.font=font
		self.PlayersData=PlayersData

	def run(self):
		self.draw()
		if pygame.key.get_pressed()[pygame.K_SPACE] and len(self.PlayersData) > 1:
			return True
		else:
			return False
	def draw(self):
		self.screen.fill(self.GREEN) #bckground
		pygame.draw.rect(self.screen,self.GRAY,(self.screen.get_width()*0.2,self.screen.get_height()*0.7,self.screen.get_width()*0.6,100)) #drawing the start button
		text=self.font.render('Press \'SPACE\' to start',True,(0,0,0))
		text_rect=text.get_rect()
		text_rect.centerx = self.screen.get_rect().centerx
		text_rect.y = self.screen.get_height()*0.7
		self.screen.blit(text,text_rect)
		if len(self.PlayersData) > 0: #cheking if there are players connected
			num=0
			for name in self.PlayersData.keys(): #drawing players names
				text=self.font.render(str(self.PlayersData[name][0]),True,(0,0,0))
				text_rect=text.get_rect()
				text_rect.centerx = self.screen.get_rect().centerx
				text_rect.y = self.screen.get_height()*(num/10)
				self.screen.blit(text,text_rect)
				num +=1

	def collides(self,rect1, rect2):
		r1x = rect1[0][0]
		r1y = rect1[0][1]
		r2x = rect2[0][0]
		r2y = rect2[0][1]
		r1w = rect1[1][0]
		r1h = rect1[1][1]
		r2w = rect2[1][0]
		r2h = rect2[1][1]

		if (r1x < r2x + r2w and r1x + r1w > r2x and r1y < r2y + r2h and r1y + r1h > r2y):
			return True
		else:
			return False

class waiting_for():
	def __init__(self,screen,font,PlayersData):
		self.screen=screen
		self.font=font
		self.PlayersData=PlayersData
		self.BLUE=(0,255*0.3,255)

	def run(self):
		self.draw()

	def draw(self):
		self.screen.fill(self.BLUE)
		if len(self.PlayersData) > 0: #cheking if there are players connected
			found=False
			for name in self.PlayersData.keys(): #finding the drawer
				if self.PlayersData[name][1]:
					nick=self.PlayersData[name][0]
					found=True
				elif not found:
					nick='None'

		else:
			nick = 'None'
		text=self.font.render('waiting for '+nick,True,(0,0,0))
		text_rect=text.get_rect()
		text_rect.centerx = self.screen.get_rect().centerx
		text_rect.y = self.screen.get_height()*0.7
		self.screen.blit(text,text_rect)

class ShowImageAndVotes():
	def __init__(self,screen,font,PlayersData,votes):
		self.screen=screen
		self.font=font
		self.PlayersData=PlayersData
		self.votes=votes
		img = pygame.image.load('server_imgs\\img.jpg')
		self.img=pygame.transform.scale(img, (self.screen.get_width(),self.screen.get_height()))

	def run(self):
		self.draw()
		if pygame.key.get_pressed()[pygame.K_SPACE] and len(self.votes) == len(self.PlayersData) - 1:
			return True
		else:
			return False

	def draw(self):
		self.screen.blit(self.img,(0,0))

		if len(self.votes) == len(self.PlayersData) - 1:
			text=self.font.render('Press \'SPACE\' to continue',True,(0,0,0))
			text_rect=text.get_rect()
			text_rect.centerx = self.screen.get_rect().centerx
			text_rect.y = self.screen.get_height()*0.8
			self.screen.blit(text,text_rect)

		num=0
		for vote in self.votes: #drawing players votes
			text=self.font.render(vote,True,(0,0,0))
			text_rect=text.get_rect()
			text_rect.centerx = self.screen.get_rect().centerx
			text_rect.y = self.screen.get_height()*(num/10)
			self.screen.blit(text,text_rect)
			num +=1

class ShowImageAndPossibilitys():
	def __init__(self,screen,font,PlayersData,votes):
		self.screen=screen
		self.font=font
		self.PlayersData=PlayersData
		self.votes=votes
		img = pygame.image.load('server_imgs\\img.jpg')
		self.img=pygame.transform.scale(img, (self.screen.get_width(),self.screen.get_height()))

	def run(self):
		self.draw()

	def draw(self):
		self.screen.blit(self.img,(0,0))
		num=0
		for vote in self.votes: #drawing players votes
			text=self.font.render(str(num+1)+" : "+vote,True,(0,0,0))
			text_rect=text.get_rect()
			text_rect.centerx = self.screen.get_rect().centerx
			text_rect.y = (self.screen.get_height())*(num/10)
			self.screen.blit(text,text_rect)
			num +=1

		text=self.font.render('what is this',True,(0,0,0)) #drawing 'what is this'
		text_rect=text.get_rect()
		text_rect.centerx = self.screen.get_rect().centerx
		text_rect.y = self.screen.get_height()*0.8
		self.screen.blit(text,text_rect)

class EndVotes():
	def __init__(self,screen,font,PlayersData,votes,chosen):
		self.screen=screen
		self.font=font
		self.PlayersData=PlayersData
		self.votes=votes
		self.chosen=chosen
		img = pygame.image.load('server_imgs\\img.jpg')
		self.img=pygame.transform.scale(img, (self.screen.get_width(),self.screen.get_height()))

	def run(self):
		self.draw()

		if pygame.key.get_pressed()[pygame.K_SPACE]:
			return True
		else:
			return False

	def draw(self):
		self.screen.blit(self.img,(0,0))

		text=self.font.render('this is a ' + self.votes[self.chosen],True,(0,0,0)) #drawing 'this is...'
		text_rect=text.get_rect()
		text_rect.centerx = self.screen.get_rect().centerx
		text_rect.centery = self.screen.get_rect().centery
		self.screen.blit(text,text_rect)