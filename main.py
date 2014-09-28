from kivy.config import Config

Config.set('graphics', 'height', '700')
Config.set('graphics', 'width', '1120')
Config.write()

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, ObjectProperty, NumericProperty, StringProperty, BooleanProperty, DictProperty, BoundedNumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.graphics import Color,Rectangle
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.core.image import Image as CImage
from kivy.animation import Animation
from kivy.vector import Vector

import time
import random

class Boundary(Widget):
    room = BooleanProperty(False)
    solid = BooleanProperty(False)
    def __init__(self, **kwargs):
        super(Boundary, self).__init__(**kwargs)

class WSprite(Widget): # CURRENTLY REDUNDANT
    pos = ListProperty()
    def __init__(self,tex, **kwargs):
        super(WSprite, self).__init__(**kwargs)
        self.tex = tex
        self.rect = Rectangle(texture = self.tex,
                              size = self.size,
                              pos = self.pos)
        with self.canvas:
            self.rect
    
    def on_pos(self, instance, value):
        print 'moved'
                   
class AGSprite(Image):
    player = BooleanProperty(False)
    solid = BooleanProperty(False)
    enemy = BooleanProperty(False)
    town = BooleanProperty(False)
    boundary = BooleanProperty(False)
    
    def __init__(self, size=(64,64),**kwargs):
        super(AGSprite, self).__init__(**kwargs)
        self.size_hint=(None,None)
        self.size = size
        self.allow_stretch = True
    
    def on_start(self):
        print 'i started' 

class AGPlayer(AGSprite):
    def __init__(self,**kwargs):
        super(AGPlayer, self).__init__(**kwargs)
        self.boundary = Widget(width = (self.width+8),height = (self.height+8), pos = self.pos)
            
class KYRScreenManager(ScreenManager):
    touchLocation = ListProperty()
    playerLocation = ListProperty()
    playerDestination = ListProperty()
    velocity = NumericProperty(200)
    
    def __init__(self, **kwargs):
        super(KYRScreenManager, self).__init__(**kwargs)
        self.loadAssets()
        self.buildRooms()
        
        #self.add_widget(room1)
        #self.add_widget(room2)
        self.buildLocationEvent()
        self.transition=WipeTransition()
        
        self.switch_to(self.room1)
        self.room1.isCurrent = True    
        
        Clock.schedule_interval(self.updatePlayerLocation, 0.5)
    
    def buildRooms(self):
        self.room1 = KYRScreen(name='room1', bg = 'assets/art/room01.png', music = self.overworld)
        self.room2 = KYRScreen(name='room2', bg = 'assets/art/room02.png',)
        self.room3 = KYRScreen(name='room3', bg = 'assets/art/room03.png',)
        self.room4 = KYRScreen(name='room4', bg = 'assets/art/room04.png',)
        self.room5 = KYRScreen(name='room5', bg = 'assets/art/room05.png',)
        self.room6 = KYRScreen(name='room6', bg = 'assets/art/room06.png',)
        self.room7 = KYRScreen(name='room7', bg = 'assets/art/room07.png',)
        self.room8 = KYRScreen(name='room8', bg = 'assets/art/room08.png',)
        self.room9 = KYRScreen(name='room9', bg = 'assets/art/room09.png',)
        self.room10 = KYRScreen(name='room10', bg = 'assets/art/room10.png',)
        self.room11 = KYRScreen(name='room11', bg = 'assets/art/room11.png',)
        self.room12 = KYRScreen(name='room12', bg = 'assets/art/room12.png',)
        self.room13 = KYRScreen(name='room13', bg = 'assets/art/room13.png',)
        self.room14 = KYRScreen(name='room14', bg = 'assets/art/room14.png',)
        self.room15 = KYRScreen(name='room15', bg = 'assets/art/room15.png',)
        self.room16 = KYRScreen(name='room16', bg = 'assets/art/room16.png',)
        self.room17 = KYRScreen(name='room17', bg = 'assets/art/room17.png',)
        self.room18 = KYRScreen(name='room18', bg = 'assets/art/room18.png',)
        self.room19 = KYRScreen(name='room19', bg = 'assets/art/room19.png',) 
         
    def loadAssets(self):
        self.overworld = SoundLoader.load('assets/music/overworld.wav')
        
    def buildLocationEvent(self):
        # treehouse
        self.room1.locationEvent = dict(bottom = [self.room7, (650,115)])
        # treehouse base
        self.room2.locationEvent = dict(top = [self.room7, (500,120)], right = [], left = [])
        # treehouse doorway
        self.room7.locationEvent = dict(top = [self.room1, (500,70)], bottom = [self.room2, (500,120)])
        
    def updatePlayerLocation(self, dt):
        self.playerLocation = self.current_screen.player.pos
    
    def on_playerLocation(self, instance, value):
        # evaluate whether room has room connection at event location
        # evaulate boundary collision
        print "on_playerLocation: ",value
        self.evaluateBoundaryCollision(value)
        x = value[0]
        y = value[1]
        
        if y > 386:
            self.evaluateEvent('top')
        elif y < 64:
            self.evaluateEvent('bottom')
        elif x < 64:
            self.evaluateEvent('left')
        elif x > 960:
            self.evaluateEvent('right')
    
    def evaluateBoundaryCollision(self, position):
        pass
        
    def evaluateEvent(self, spot):
        locationEvent = self.current_screen.locationEvent
        if spot in locationEvent:
            room = locationEvent[spot][0]
            position = locationEvent[spot][1]
            self.changeRoom(room, position)
        
    def changeRoom(self, room, position):
        self.current_screen.isCurrent = False
        self.remove_widget(self.current_screen)
        room.playerLocation = position
        self.switch_to(room)
        self.current_screen.isCurrent = True
    
    def on_touchLocation(self, instance, value):
        #print 'value: ',value
        self.playerLocation = self.current_screen.player.pos
        self.playerDestination = value
        player = self.current_screen.player
        xTouch = value[0]
        yTouch = value[1]
        xPlayer = self.playerLocation[0]
        yPlayer = self.playerLocation[1]
        
        distance = Vector(xTouch, yTouch).distance((xPlayer,yPlayer))
        duration = distance / self.velocity
        
        anim = Animation(x=xTouch, y=yTouch, d=duration)
        anim.start(player)
            
class KYRScreen(Screen):
    
    spriteList = ListProperty()
    locationEvent = DictProperty() # all location-based events for the room, including room changes
    player = ObjectProperty()
    playerBoundary = ObjectProperty()
    isCurrent = BooleanProperty(False)
    playerLocation = ListProperty((500,70))
    bg =  StringProperty()
    music = ObjectProperty()
    #startLocations = DictProperty()
    direction = StringProperty('top')
    
    def __init__(self, **kwargs):
        super(KYRScreen, self).__init__(**kwargs)
        self.field = RelativeLayout()
        '''
        # inverse directions, based on direction you enter from
        self.startLocations = dict(top = (512, 96),
                                   bottom = (512, 416),
                                   left = (928, 256),
                                   right = (96, 256))
        '''
        #sprites = self.loadSprites()
        #self.buildSprites(sprites)
    
    def on_isCurrent(self, instance, value):
        if value:
            self.turnOn()
        else:
            self.turnOff()

    def turnOn(self):
        print 'turning on {}'.format(self)
        #self.getStartLocation()
        self.buildPlayer(self.playerLocation)
        self.loadBackground()
        self.loadWidgets()
        self.toggleMusic('on')
    
    def turnOff(self):
        print 'turning off {}'.format(self)
        #self.parent.playerLocation = self.playerLocation
        self.unloadWidgets()
        self.toggleMusic('off')
    
    def getStartLocation(self):
        self.playerLocation = self.startLocations[self.direction]
          
    def loadBackground(self):
        print 'loading bg', self.bg
        tex = CImage.load(self.bg, keep_data=True).texture
        self.buildBackground(tex)
        
    def buildBackground(self, tex):
        with self.field.canvas.before:
            Rectangle(texture = tex, pos=(0,0), size=(1068,450))
    
    def loadWidgets(self):
        self.add_widget(self.field)
        
    def unloadWidgets(self):
        self.field.remove_widget(self.player)
        self.remove_widget(self.field)      
    
    def toggleMusic(self, value): 
        if value == 'on':
            if self.music:
                print("Sound found at %s" % self.music.source)
                print("Sound is %.3f seconds" % self.music.length)
                self.music.loop = True
                self.music.play()
        elif value == 'off':
            if self.music:
                self.music.stop()
                          
    def changePlayerImage(self, direction):
        if direction == 'up':
            self.player.source = 'assets/art/Clyde_up.zip'
        elif direction == 'down':
            self.player.source = 'assets/art/Clyde_down.zip'
        elif direction == 'left':
            self.player.source = 'assets/art/Clyde_left.zip'
        elif direction == 'right':
            self.player.source = 'assets/art/Clyde_right.zip'
             
    def on_transition_state(self, instance, value):   
        pass
        
    def buildPlayer(self, playerLocation):
        self.player = AGPlayer(source = 'assets/art/brandon-right.zip', size=(96,192))
        self.playerBoundary = Widget(size=(104,200))
        #self.player.anim_delay = (-1)
        self.player.pos = playerLocation
        self.playerBoundary.center = self.player.center
        self.field.add_widget(self.player)   
        self.field.add_widget(self.playerBoundary)
    
    def loadSprites(self):
        # look in sprite list for sprite in specific room, return sprite list for room
        directory = {'room number': 'sprite list'}    
        sprites = directory['room number']
        return sprites
       
    def buildSprites(self, sprites):
        for sprite in sprites:
            self.field.add_widget(sprite)
            self.spriteList.append(sprite)
    
    def checkCollision(self):
        pass
        
    def didCollision(self):
        pass

class Manager(RelativeLayout):

    touchLocationScreen = ListProperty()
    touchLocationUI = ListProperty()
    infoText = StringProperty('adventure awaits!\n')
    
    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self.buildUI()
        self.orientation = 'vertical'
        
    def on_touch_down(self, value):
        #print('value.pos: {} value.spos: {}'.format(value.pos, value.spos))
        x = value.pos[0]
        y = value.pos[1]
        localScreen = self.screenManager.to_local(x, y, True)
        if localScreen[0] < 0 or localScreen[1] < 0:
            pass # only update touchLocation for the screen when on screen
        else:
            self.touchLocationScreen = localScreen
            self.touchLocationUI = (x,y)
        
        self.infoText = str(localScreen)
           
    def on_touchLocationScreen(self, instance, value):
        # take touch input on the screenmanager and send to SM for handling
        self.screenManager.touchLocation = self.touchLocationScreen
    
    def eventCompleted(self):
        pass
        
    def update(self, dt):
        #self.infoScreen.text = self.infoScreenText
        pass
        
    def on_infoText(self, instance, value): 
        print value
        self.info.text = self.infoText
        
    def buildUI(self):
        bottomBox = RelativeLayout() # 1024,188
        self.screenManager = KYRScreenManager(size=(1068,450), size_hint=(None,None), pos=(25,224))
        self.info = TextInput(text=self.infoText, multiline=True, readonly=True, size=(1014,30), size_hint=(None,None), pos=(6,152))
        btnMenu = Button(text='menu', size=(196,120), size_hint=(None,None), pos=(28,16), opacity = .5)
        
        bottomBox.add_widget(self.info)
        bottomBox.add_widget(btnMenu)
        
        self.add_widget(self.screenManager)
        self.add_widget(bottomBox)
        
class GameApp(App):
    
    def build(self):
        return Manager()

if __name__ == "__main__":
    GameApp().run()
    
'''
Created on Sep 17, 2014

@author: Joshua Cox
'''