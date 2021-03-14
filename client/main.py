from kivy.app import App
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock

from random import random
from PIL import Image
from network import Network
from time import sleep

from kivy.core.window import Window
from kivy.graphics import (Color,Ellipse,Rectangle,Line)

class WindowManager(ScreenManager):
    pass

class Painterwidget(Screen): #painter screen that you draw on. can't remenber how the code works it was a long time since checked
    def __init__(self,**kwargs): #if it works it works
        super().__init__(**kwargs)
        self.candraw = False
        self.color1chosen = False
        self.color2chosen = False
        self.color = (255,0,0,1)
        self.last_x = 0
        self.last_y = 0

    def on_touch_move(self,touch):
        if Window.size[1] - Window.size[1]  * 0.8  < touch.y and self.candraw:
            if self.last_y == 0 and self.last_x == 0:
                self.canvas.add(Color(self.color[0],self.color[1],self.color[2],1))
                with self.canvas:
                    Line(points=(touch.x,touch.y,touch.x,touch.y))
                self.last_x,self.last_y = touch.x,touch.y
            else:
                self.canvas.add(Color(self.color[0],self.color[1],self.color[2],1))
                with self.canvas:
                    Line(points=(self.last_x,self.last_y,touch.x,touch.y),width=2)
                self.last_x,self.last_y = touch.x,touch.y

    def on_touch_up(self,touch):
        self.last_x,self.last_y = 0,0

    def erasor(self):
        with self.canvas:
            Color(1,1,1,1)
            Rectangle(pos=(0,Window.size[1] - Window.size[1] * 0.8),size=(Window.size[0],Window.size[1] - Window.size[1] * 0.2))

    def color1(self):
        if not self.color1chosen:
            self.color1chosen = True
            self.color11 = (random(),random(),random())
        self.color = self.color11
        self.candraw = True

    def color2(self):
        if not self.color2chosen:
            self.color2chosen = True
            self.color22 = (random(),random(),random())
        self.color = self.color22
        self.candraw = True

    def submit(self):
        self.color1chosen = False
        self.color2chosen = False
        self.size= (Window.size[0],Window.size[1])
        self.export_to_png('image.png')

        img = Image.open('image.png')

        crop_img = img.crop((0,0, img.width, img.height * 0.8))
        crop_img.save("image.png")
        crop_img = crop_img.convert('RGB')
        crop_img.save("image.jpg",quality=75)
        global clocked
        Clock.unschedule(clocked)        
        clocked = Clock.schedule_interval(pis,0.5)
        

        with self.canvas:
            Color(1,1,1,1)
            Rectangle(pos=(0,Window.size[1] - Window.size[1] * 0.8),size=(Window.size[0],Window.size[1] - Window.size[1] * 0.2))

        sm.current = "wait"

class WaitingMenu(Screen):
    pass

class VoteMenu(Screen):
    vote = ObjectProperty(None)

    def VoteBtn(self):
        global data_recv
        data_recv[5]=self.vote.text
        self.vote.text=''

class ChooseMenu(Screen):

    def CBtn1(self):
        global data_recv
        data_recv[5]=1-1
    def CBtn2(self):
        global data_recv
        data_recv[5]=2-1
    def CBtn3(self):
        global data_recv
        data_recv[5]=3-1
    def CBtn4(self):
        global data_recv
        data_recv[5]=4-1
    def CBtn5(self):
        global data_recv
        data_recv[5]=5-1
    def CBtn6(self):
        global data_recv
        data_recv[5]=6-1       


class MainMenu(Screen):
    ipnum = ObjectProperty(None)
    nickname = ObjectProperty(None)

    def ConnectBtn(self):
        try:
            print(self.ipnum.text,self.nickname.text)
            global Net,data_recv,clocked
            if self.ipnum.text=='' or self.ipnum.text==None or self.ipnum.text.lower()=='pc':
                adr='192.168.0.189' #could change this is just for easier access
            else:
                adr=self.ipnum.text
            print(adr)
            Net = Network(adr)
            Net.getData()
            data_recv = Net.send([self.nickname.text,False,False,False,False,None,False])
            clocked = Clock.schedule_interval(rs,0.5)
            sleep(0.3)
            sm.current = "wait"
        except:
            pass

Net=''
data_recv=''
clocked=''

#protocol image send
def pis(dt):
    global clocked
    sm.current = "wait"
    data_recv=Net.send('PSI')
    data_recv=Net.send('PSI')
    if data_recv=='continue':
        myfile = open("image.jpg", 'rb')
        bytess = myfile.read()
        print(type(bytess))
        size = len(bytess)
        myfile.close()
        data_recv=Net.send(int(size))
        if data_recv=='GOT':
            data_recv=Net.send(bytess)
            if data_recv=='GOT':
                Clock.unschedule(clocked)        
                clocked = Clock.schedule_interval(rs,0.5)


def rs(dt): #manage connection
    global data_recv,clocked
    try:
        data_recv=Net.send(data_recv)
    except:
        Clock.unschedule(clocked)
        sm.current = "mainmenu"
    if data_recv==None:
        print("connection lost")
        Clock.unschedule(clocked)
        sm.current = "mainmenu"
    else:
        # print(data_recv)
        if data_recv[1] and data_recv[4] and not data_recv[6]:
            sm.current = "wait"

        elif data_recv[1] and not sm.current=="painter" and not data_recv[6] and not data_recv[4]:
            sm.current = "painter"

        elif sm.current == "painter" and data_recv[1] and not data_recv[6] and data_recv[4]: #check this if something goes wrong
            sm.current = "wait"

        elif sm.current == "wait" and not data_recv[1] and data_recv[2]:
            sm.current = "vote"

        elif sm.current == "vote" and not data_recv[1] and not data_recv[2]:
            sm.current = "wait"

        elif sm.current == "wait" and data_recv[6] and data_recv[1] and data_recv[4]:
            sm.current = "c"

        elif sm.current == "c" and not data_recv[6] and data_recv[1] and data_recv[4]:
            sm.current = "wait"


Builder.load_file("draw2.kv")
sm = WindowManager()

screens = [MainMenu(name="mainmenu"),Painterwidget(name="painter"),WaitingMenu(name="wait"),VoteMenu(name='vote'),ChooseMenu(name='c')]
for screen in screens:
    sm.add_widget(screen)

sm.current = "mainmenu"
       
class draw_2App(App):
    def build(self):
        return sm
        
        

if __name__ == "__main__":
    draw_2App().run()