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

class WSprite(Widget):
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
        
class KYRScreenManager(ScreenManager):
    touchLocation = ListProperty()
    playerLocation = ListProperty()
    velocity = NumericProperty(200)
    
    def __init__(self, **kwargs):
        super(KYRScreenManager, self).__init__(**kwargs)
        self.loadAssets()
        self.room1 = KYRScreen(name='room1',
                               bg = 'assets/art/room1.png',
                               music = self.overworld,
                               startLocations = dict(top = (512, 96),
                                                     bottom = (512, 416),
                                                     left = (928, 256),
                                                     right = (96, 256)
                                )) # inverse directions, based on direction you enter from
        self.room2 = KYRScreen(name='room2',
                               bg = 'assets/art/room2.png',
                               startLocations = dict(top = (512, 96),
                                                     bottom = (512, 416),
                                                     left = (928, 256),
                                                     right = (96, 256)
                                ))
        
        #self.add_widget(room1)
        #self.add_widget(room2)
        self.buildLocationEvent()
        self.transition=WipeTransition()
        
        self.switch_to(self.room1)
        self.room1.isCurrent = True    
        
        Clock.schedule_interval(self.updatePlayerLocation, 0.5)
    
    def loadAssets(self):
        self.overworld = SoundLoader.load('assets/sound/overworld.wav')
        
    def buildLocationEvent(self):
        # location directions are inverted
        self.room1.locationEvent = dict(top = self.room2)
        self.room2.locationEvent = dict(bottom = self.room1)
        
    def updatePlayerLocation(self, dt):
        self.playerLocation = self.current_screen.player.pos
    
    def on_playerLocation(self, instance, value):
        # evaluate whether room has room connection at event location
        print "on_playerLocation: ",value
        x = value[0]
        y = value[1]
        
        if y > 448:
            self.evaluateEvent('bottom')
        elif y < 64:
            self.evaluateEvent('top')
        elif x < 64:
            self.evaluateEvent('right')
        elif x > 960:
            self.evaluateEvent('left')
        
    def evaluateEvent(self, spot):
        locationEvent = self.current_screen.locationEvent
        if spot in locationEvent:
            self.parent.infoText = locationEvent[spot].name
            room = locationEvent[spot]
            self.changeRoom(room, spot)
        
    def changeRoom(self, room, spot):
        self.current_screen.isCurrent = False
        self.remove_widget(self.current_screen)
        room.direction = spot
        self.switch_to(room)
        self.current_screen.isCurrent = True
    
    def adjustPlayerLocation(self, room, spot): 
        if spot == 'top':
            room.playerLocation = (512, 96)
        elif spot == 'bottom':
            room.playerLocation = (512, 416)
        elif spot == 'right':
            room.playerLocation = (928, 256)
        elif spot == 'left':
            room.playerLocation = (96, 256)
    
    def on_touchLocation(self, instance, value):
        #print 'value: ',value
        self.playerLocation = self.current_screen.player.pos
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
    isCurrent = BooleanProperty(False)
    playerLocation = ListProperty((200,200))
    bg =  StringProperty()
    music = ObjectProperty()
    startLocations = DictProperty()
    direction = StringProperty('top')
    
    def __init__(self, **kwargs):
        super(KYRScreen, self).__init__(**kwargs)
        self.field = RelativeLayout()
        
        #sprites = self.loadSprites()
        #self.buildSprites(sprites)
    
    def on_isCurrent(self, instance, value):
        if value:
            self.turnOn()
        else:
            self.turnOff()

    def turnOn(self):
        print 'turning on {}'.format(self)
        self.getStartLocation()
        self.buildPlayer(self.playerLocation)
        self.loadBackground()
        self.loadWidgets()
        self.toggleMusic('on')
    
    def turnOff(self):
        print 'turning off {}'.format(self)
        self.parent.playerLocation = self.playerLocation
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
        self.player = AGSprite(source = 'assets/art/brandon-right.zip', size=(96,192))
        #self.player.anim_delay = (-1)
        self.player.pos = playerLocation
        self.field.add_widget(self.player)   
    
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
TODO
boundaries: standardized collision objects to prevent player movement

zone of detection: zone around player widget to detect boundaries ahead of collision, zone will dictate player 
                    movement around boundaries
player widget sizing: player widget should be half length of canvas, allowing upper sprite to overlap objects
                        before collisions occur, preventing head-bumping boundaries
'''
    
'''
Created on Sep 17, 2014

@author: Joshua Cox
'''