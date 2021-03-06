from kivy.config import Config

Config.set('graphics', 'height', '700')
Config.set('graphics', 'width', '1120')
Config.write()

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, ObjectProperty, NumericProperty, StringProperty, BooleanProperty, DictProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.stacklayout import StackLayout
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
import sqlite3

db = sqlite3.connect('KyraDB.db')
curs = db.cursor()
items = []

class Boundary(Widget):
    room = BooleanProperty(False)
    solid = BooleanProperty(False)
    event = ObjectProperty()
    
    def __init__(self, pos, size, event = None, startLocation = None, **kwargs):
        super(Boundary, self).__init__(**kwargs)
        self.size_hint = (None,None)
        self.pos = pos
        self.size = size
        self.event = event
        self.startLocation = startLocation
        
        if event == None:
            self.solid = True
        
        #print "pos {} size {} event {}".format(self.pos, self.size, self.event)

class Body(Widget):
    def __init__(self, **kwargs):
        super(Body, self).__init__(**kwargs)
        self.makeCollisionPoints(self.pos, self.size)
    
    def makeCollisionPoints(self, pos, size):
        x,y = pos
        h,w = size
        
        #print 'Body x {} y {} h {} w {}'.format(x,y,h,w)
        self.collisionPoints = []
    
class Info(TextInput):
    pass
    
class WSprite(Widget): # CURRENTLY REDUNDANT
    pos = ListProperty()
    def __init__(self, tex, **kwargs):
        super(WSprite, self).__init__(**kwargs)
        self.tex = tex
        self.rect = Rectangle(texture = self.tex,
                              size = self.size,
                              pos = self.pos)
        with self.canvas:
            self.rect
    
    def on_pos(self, instance, value):
        print 'moved'

class Inventory(Widget):
    def __init__(self,slot, **kwargs):
        super(Inventory, self).__init__(**kwargs)
        self.size_hint = (None,None)
        self.size = (55,57)
        
class AGSprite(Image):
    player = BooleanProperty(False)
    solid = BooleanProperty(False)
    enemy = BooleanProperty(False)
    town = BooleanProperty(False)
    boundary = BooleanProperty(False)
    
    def __init__(self,**kwargs):
        super(AGSprite, self).__init__(**kwargs)
        self.size_hint=(None,None)
        self.allow_stretch = True
    
    def on_start(self):
        print 'i started' 

class AGPlayer(AGSprite):
    def __init__(self,**kwargs):
        super(AGPlayer, self).__init__(**kwargs)
        self.zone = Widget(pos = self.pos, size = (self.width,self.height/2))
    
    def on_pos(self, instance, value):
        self.zone.pos = self.pos

class Item(AGSprite):
    def __init__(self,name,**kwargs):
        super(Item, self).__init__(**kwargs)
        self.size = (48,48)
        self.name = name
            
class KYRScreenManager(ScreenManager):
    touchLocation = ListProperty()
    playerLocation = ListProperty()
    playerDestination = ListProperty()
    velocity = NumericProperty(200)
    sprites = ListProperty()
    collision = BooleanProperty(False)
    destination = ListProperty()
    boundary = ObjectProperty()
    music = ObjectProperty(None)
    selected = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(KYRScreenManager, self).__init__(**kwargs)
        #self.anim = Animation()
        self.loadAssets()
        self.buildRooms()
        
        self.buildLocationEvents()
        self.transition=WipeTransition()    
        self.init() 
        
        Clock.schedule_interval(self.updatePlayerLocation, (1/60))
    
    def init(self):
        self.loadSprites(self.room1)
        self.switch_to(self.room1)
        self.room1.isCurrent = True
        
    def buildRooms(self):
        self.room1 = KYRScreen(name='room1', bg = 'assets/art/room01.png', music = self.silent)
        self.room2 = KYRScreen(name='room2', bg = 'assets/art/room02.png', music = self.the_forest)
        self.room3 = KYRScreen(name='room3', bg = 'assets/art/room03.png', music = self.the_forest)
        self.room4 = KYRScreen(name='room4', bg = 'assets/art/room04.png', music = self.the_forest)
        self.room5 = KYRScreen(name='room5', bg = 'assets/art/room05.png', music = self.the_forest)
        self.room6 = KYRScreen(name='room6', bg = 'assets/art/room06-1.png', music = self.brynn_temple)
        self.room7 = KYRScreen(name='room7', bg = 'assets/art/room07.png', music = self.the_forest)
        self.room8 = KYRScreen(name='room8', bg = 'assets/art/room08.png', music = self.the_forest)
        self.room9 = KYRScreen(name='room9', bg = 'assets/art/room09.png',
                               fg = 'assets/art/room09-stone.png', music = self.pool_of_sorrow)
        self.room11 = KYRScreen(name='room11', bg = 'assets/art/room11.png', music = self.the_forest)
        self.room12 = KYRScreen(name='room12', bg = 'assets/art/room12.png', music = self.the_forest)
        self.room13 = KYRScreen(name='room13', bg = 'assets/art/room13.png', music = self.the_forest)
        self.room14 = KYRScreen(name='room14', bg = 'assets/art/room14.png', music = self.the_forest)
        self.room16 = KYRScreen(name='room16', bg = 'assets/art/room16.png', music = self.the_forest)
        self.room17 = KYRScreen(name='room17', bg = 'assets/art/room17.png', music = self.the_forest)
        self.room18 = KYRScreen(name='room18', bg = 'assets/art/room18.png', music = self.the_forest)
        self.room19 = KYRScreen(name='room19', bg = 'assets/art/room19.png', music = self.silent) 
         
    def loadAssets(self):
        self.the_forest = SoundLoader.load('assets/music/The_Forest.ogg')
        self.pool_of_sorrow = SoundLoader.load('assets/music/Pool_Of_Sorrow.ogg')
        self.brynn_temple = SoundLoader.load('assets/music/Brynn_Temple.ogg')
        self.healing_the_willow = SoundLoader.load('assets/music/Healing_the_Willow.ogg')
        self.silent = SoundLoader.load('assets/music/silent.ogg')
        
    def toggleMusic(self):
        try:
            music = self.current_screen.music
            if self.music == music:
                pass
            else:
                if self.music != None:
                    self.music.stop()
                self.music = music
                print("Sound found at %s" % self.music.source)
                print("Sound is %.3f seconds" % self.music.length)
                self.music.loop = True
                self.music.play()
        
        except Exception as e:
            print "toggleMusic exception: ",e
            
    def buildLocationEvents(self):
        # Boundary(pos, size, event, start location) rooms
        # Boundary(pos, size, solid = True) walls
        w = self.width
        h = self.height
        
        # treehouse
        self.room1.boundaries = [Boundary((500,0), (w,32), self.room7, (650,105)),
                                 Boundary((0,200), (w,150)),
                                 Boundary((w-100,0), (50,h)),
                                 Boundary((0,0), (200,h)),
                                 Boundary((0,0), (500,64)),
                                 Boundary((603, 160),(400,100))
                                 ]
        # treehouse base
        self.room2.boundaries = [Boundary((0,h-32), (w,32), self.room7, (500,120)),
                                 Boundary((w-32,0), (32,w), self.room8, (100,70)),
                                 Boundary((0,0), (32,h), self.room3, (800,70))]
        # wilted tree
        self.room3.boundaries = [Boundary((w-32,0), (32,h), self.room2, (100,70)),
                                 Boundary((0,0), (32,h), self.room4, (900,70))]
        # rock cliff below temple
        self.room4.boundaries = [Boundary((450,h-32), (200,32), self.room5, (500,70)),
                                 Boundary((w-32,0), (32,h), self.room3, (70,70))]
        # temple entrance
        self.room5.boundaries = [Boundary((0,0), (w,32), self.room4, (450,h-200)),
                                 Boundary((550,200), (50,100), self.room6, (700,100))]
        # temple
        self.room6.boundaries = [Boundary((w-32,0), (32,h), self.room5, (w-420,70))]
        
        # treehouse doorway
        self.room7.boundaries = [Boundary((0,h-100), (w,32), self.room1, (500,70)),
                                 Boundary((0,50), (w, 32), self.room2, (500,120))]
        # woods 1
        self.room8.boundaries = [Boundary((0,0), (32,h), self.room7, (w-100,70)),
                                 Boundary((w-32,0), (32,h), self.room9, (70,70))]
        # pool of tears
        self.room9.boundaries = [Boundary((w-32,0), (32,h), self.room11, (200,70)),
                                 Boundary((0,0), (32,h), self.room8, (800,70))]
        # woods 2
        self.room11.boundaries = [Boundary((0,0), (32,h), self.room9, (800,70)),
                                  Boundary((0,0), (w,32), self.room17, (500,200)),
                                  Boundary((0,h-32), (w,32), self.room12, (500, 70))]
        # woods 3
        self.room12.boundaries = [Boundary((0,0), (32,h), self.room13, (800,70)),
                                  Boundary((0,0), (w,32), self.room11, (500,200)),
                                  Boundary((w-32,0), (32,h), self.room14, (70,70))]
        # woods 4
        self.room13.boundaries = [Boundary((w-32,0), (32,h), self.room12, (70,70))]
        
        # crystal altar
        self.room14.boundaries = [Boundary((0,0), (32,h), self.room12, (800,100)),
                                  Boundary((w-32,0), (32,h), self.room16, (100,100))]
        # sea cliff
        self.room16.boundaries = [Boundary((0,0), (32,h), self.room14, (800,100))]
        
        # woods 5
        self.room17.boundaries = [Boundary((500,h-32), (w-500,32), self.room11, (500,100)),
                                  Boundary((100,0), (w-100,32), self.room18, (700,200))]
        # cave entrance
        self.room18.boundaries  = [Boundary((600,h-32), (w-600,32), self.room17, (600,100)),
                                   Boundary((100,100), (50,200), self.room19, (800,70))]
        # bridge cave
        self.room19.boundaries = [Boundary((w-32,0), (32,300), self.room18, (300,70))]
    
    def updatePlayerLocation(self, dt):
        self.playerLocation = self.current_screen.player.pos
    
    def on_playerLocation(self, instance, value):
        """
            check for boundary collisions as player moves
        """
        #print "on_playerLocation: ",value
        self.evaluateCollision(value)
    
    def evaluateCollision(self, destination):
        player = self.current_screen.player
        boundaries = self.current_screen.boundaries

        for boundary in boundaries:
            if player.zone.collide_widget(boundary):
                #print 'collision!'
                self.boundary = boundary
                self.destination = destination
                self.didCollision(boundary, destination)
            '''
            else:
                try:
                    print "no collisions"
                    if self.anim.have_properties_to_animate(player):
                        print 'props ',self.anim.animated_properties
                        self.anim.start(player)
                except:
                    pass
            '''

    def didCollision(self, boundary, destination):
        player = self.current_screen.player
        if boundary.solid:
            self.solidCollision(boundary, destination)
        else:
            self.anim.stop(player)
            self.changeRoom(boundary.event, boundary.startLocation)
            
    def solidCollision(self, boundary, destination):
        player = self.current_screen.player
        #print 'solid collision'
        #print "boundary height: {}, width: {}".format(boundary.height, boundary.width)
        #print "boundary x: {}, y: {}".format(boundary.x, boundary.y)
        #print "player x: {}, y: {}".format(player.x, player.y)
        
        x = destination[0]
        y = destination[1]
        start = player.pos
        
        if player.x > (boundary.width + boundary.x - 5): # player is right of boundary
            txt= "right of boundary"
            player.x = (boundary.width + boundary.x)
            self.anim.stop_property(player, 'center_x')
            
        elif player.x < (boundary.x + 5): # player is left of boundary
            txt= "left of boundary"
            player.x = (boundary.x - player.width)
            self.anim.stop_property(player, 'center_x')
            
        if player.y > (boundary.height + boundary.y - 5): # player is above boundary
            txt= "above boundary"
            player.y = (boundary.height + boundary.y)
            self.anim.stop_property(player, 'y')
            
        elif player.y < (boundary.y + 5): # player is below boundary
            txt= "below boundary"
            player.y = (boundary.y - player.height/2)
            self.anim.stop_property(player, 'y')
        
        #print txt
        
    # REDUNDANT    
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
        self.loadSprites(room)
        self.switch_to(room)
        self.current_screen.isCurrent = True
        self.parent.screen = room
        self.toggleMusic()
    
    def on_touchLocation(self, instance, value):
        #print 'value: ',value
        if self.selected is None:
            self.movePlayer(instance, value)
      
    def movePlayer(self, instance, value):
        self.playerLocation = self.current_screen.player.pos
        self.playerDestination = value
        player = self.current_screen.player
        xTouch,yTouch = value[0],value[1]
        xPlayer = self.playerLocation[0]
        yPlayer = self.playerLocation[1]
        
        start = (xPlayer,yPlayer)
        end = (xTouch,yTouch)
        self.animateSprite(start, end, player)
    
    def loadSprites(self, room):
        print "loadSprites, room: ",room.name
        room = room.name
        print '{} sprites'.format(room)
        
    def animateSprite(self, start, end, sprite):
        try: self.anim.stop(sprite)
        except: pass
        
        distance = Vector(start).distance(end)
        duration = distance / self.velocity
        
        self.anim = Animation(center_x=end[0], y=end[1], d=duration)
        self.anim.start(sprite)
            
class KYRScreen(Screen):
    
    spriteList = ListProperty()
    locationEvent = DictProperty() # all location-based events for the room, including room changes
    player = ObjectProperty()
    playerBoundary = ObjectProperty()
    isCurrent = BooleanProperty(False)
    playerLocation = ListProperty((500,70))
    bg =  StringProperty()
    fg = StringProperty(None)
    music = ObjectProperty(None)
    #startLocations = DictProperty()
    boundaries = ListProperty()
    items = ListProperty()
    
    def __init__(self, **kwargs):
        super(KYRScreen, self).__init__(**kwargs)
        self.field = FloatLayout()

    def on_isCurrent(self, instance, value):
        if value:
            self.turnOn()
        else:
            self.turnOff()

    def turnOn(self):
        print 'turning on {}'.format(self)
        self.buildPlayer(self.playerLocation)
        self.buildBoundaries()
        self.loadBackground()
        if self.fg != None:
            self.loadForeground()
        self.loadWidgets()
    
    def turnOff(self):
        print 'turning off {}'.format(self)
        #self.parent.playerLocation = self.playerLocation
        self.unloadWidgets()
    
    def buildBoundaries(self):
        for boundary in self.boundaries:
            self.field.add_widget(boundary)
            print 'building boundary: ', boundary
          
    def loadBackground(self):
        print 'loading bg', self.bg
        bg = CImage.load(self.bg, keep_data=True).texture
        with self.field.canvas.before:
            Rectangle(texture = bg, pos=(0,0), size=(1068,450))
    
    def loadForeground(self):
        print 'loading fg', self.fg
        fg = AGSprite(source=self.fg, pos=(0,0), size=(1068,450))
        self.field.add_widget(fg)
            
    def loadWidgets(self):
        self.add_widget(self.field)
        
    def unloadWidgets(self):
        '''
            removes all widgets to prevent conflicts when re-instantiating screen
        '''
        self.field.clear_widgets()
        self.remove_widget(self.field)      
                          
    def changePlayerImage(self, direction): # CURRENTLY REDUNDANT
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
        '''
            loads player sprite onto screen
        '''
        self.player = AGPlayer(source = 'assets/art/brandon-right.zip', size=(96,192))
        #self.player.anim_delay = (-1)
        self.player.pos = playerLocation
        self.field.add_widget(self.player)   
    
    def loadSprites(self): # REDUNDANT
        # look in sprite list for sprite in specific room, return sprite list for room
        directory = {'room number': 'sprite list'}    
        sprites = directory['room number']
        return sprites
       
    def buildSprites(self, sprites): # REDUNDANT
        for sprite in sprites:
            self.field.add_widget(sprite)
            self.spriteList.append(sprite)

class Manager(RelativeLayout):

    touchLocationScreen = ListProperty()
    touchLocationUI = ListProperty()
    infoText = StringProperty('adventure awaits!')
    screen = ObjectProperty()
    selected = BooleanProperty(False)
    selectedObj = ObjectProperty(None)
    items = ListProperty([]) # holds all on-screen items
    
    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self.buildUI()
        self.loadItemSheet()
        self.screen = self.screenManager.current_screen
        self.orientation = 'vertical'
    
    def loadItemSheet(self):
        self.itemSheet = CImage('assets/art/item_sheet.png').texture
    
    def on_screen(self, instance, value):
        '''
            on room change, inst. room items
            garbage collects all items not in inventory, and resets their spawn tag
        '''
        # cleanup
        db.execute('UPDATE Item SET Spawned = ? WHERE Inventory = ?', (False,False))
        db.commit()
        for i in self.items:
            self.remove_widget(i)
        self.items = []
        
        room = value.name
        print 'room changed to ',room
        self.retrieveItems(room)
        
    def retrieveItems(self,room):
        '''
            retrieve items from database relevant to new room
            ItemID=0, Holding=1, Room=2, X=3, Y=4, Inventory=5, Name=6, Spawned=7, Path=8
        '''
        i = db.execute('SELECT * FROM Item WHERE Room = ? OR Inventory = ?', (room,True))
        for e in i: 
            print e
            if e[7] and not e[5]:
                print '{} has spawned and is not an inventory item'.format(e[6])
            else:
                position = (e[3],e[4])
                print 'spawning {} at {}'.format(e[6],position)
                self.buildItem(position,e[6],e[8])
                
    def buildItem(self,position,item,path):
        '''
            populates screen with items for the room and inventory
            inventory slot positions: 1:(336.5,85.5), 2:(406.5,85.5), 3:(476.5,85.5), 
            4:(546.5,85.5), 5:(616.5,85.5), 6:(336.5,13.5), 7:(406.5,13.5), 8:(476.5,13.5), 
            9:(546.5,13.5), 0:(616.5,13.5),
        '''
        x,y,h,w = path.split(',')
        x,y,h,w = int(x),int(y),int(h),int(w)
        tex = self.itemSheet.get_region(x,y,h,w)
        i = Item(texture = tex, pos = position, name = item)
        
        self.add_widget(i)
        self.items.append(i)
        db.execute('UPDATE Item SET Spawned = 1 WHERE Name = ? ',(item,))
    
    def moveItem(self,item,inv=False):
        '''
            moves item to inventory or ground, and labels such in DB
        '''
        self.selected = False
        r = self.screen.name
        x = item.x
        y = item.y
        n = item.name
        print 'moving {} to {}'.format(n,(x,y))
        if inv:
            curs.execute('UPDATE Item SET Inventory=?, Room=?, X=?, Y=? WHERE Name = ? ',(True,None,x,y,n))
        else:
            curs.execute('UPDATE Item SET Inventory=?, Room=?, X=?, Y=? WHERE Name = ? ',(False,r,x,y,n))
        db.commit()
        
    def on_touch_down(self, value):
        '''
            looks for an item being selected, or moves player
        '''
        #print('value.pos: {} value.spos: {}'.format(value.pos, value.spos))
        x = int(value.pos[0])
        y = int(value.pos[1])
        
        # look for an item
        for i in self.items:
            if i.collide_point(x,y):
                self.selectedObj = i
                self.infoText = '{} picked up'.format(i.name)
                self.selected = True
                break
            else:
                self.selected = False
        
        # if no item selected, move player
        if not self.selected:
            localScreen = self.screenManager.to_local(x, y, True)
            if localScreen[0] < 0 or localScreen[1] < 0:
                pass # only update touchLocation for the screen when on screen
            else:
                self.touchLocationScreen = localScreen
                self.touchLocationUI = (x,y)
            
            self.infoText = str(localScreen)
            print '{}'.format(localScreen)
            
    def on_touch_up(self, value):
        '''
            moves items, and checks if item is in inventory nodes
        '''
        x = int(value.pos[0])
        y = int(value.pos[1])
        if self.selected is True:
            if self.inventory.collide_point(x, y):
                for node in self.nodes:
                    if node.collide_point(x,y):
                        self.selectedObj.center = node.center
                        self.moveItem(self.selectedObj, inv=True)
                        block = False
                        break
                    else: block = True
                if block: # blocked item placement 
                    self.selectedObj.center = (520,280)
                    self.moveItem(self.selectedObj)
            elif self.screenManager.collide_point(x, y):
                self.moveItem(self.selectedObj)
            else: # blocked item placement
                self.selectedObj.center = (520,280)
                self.moveItem(self.selectedObj)
                pass
            
            self.infoText = '{} placed.'.format(self.selectedObj.name)
            
    def on_touch_move(self, value):
        '''
            used for dragging items on screen
        '''
        x = value.pos[0]
        y = value.pos[1]
        
        if self.selected:
            self.selectedObj.center = (x,y)
            #print 'x,y ',x,y
            #print 'object center: ',self.selectedObj.center    
               
    def on_touchLocationScreen(self, instance, value):
        '''
            take touch input on the manager and send to screen manager for handling
        '''
        self.screenManager.touchLocation = self.touchLocationScreen
    
    def eventCompleted(self): #REDUNDANT
        pass
        
    def update(self, dt): #REDUNDANT
        #self.infoScreen.text = self.infoScreenText
        pass
        
    def on_infoText(self, instance, value): 
        #print value
        self.info.text = self.infoText
    
    def buildInventory(self):
        n1 = Inventory(text='I1', slot=1)
        n2 = Inventory(text='I2', slot=2)
        n3 = Inventory(text='I3', slot=3)
        n4 = Inventory(text='I4', slot=4)
        n5 = Inventory(text='I5', slot=5)
        n6 = Inventory(text='I6', slot=6)
        n7 = Inventory(text='I7', slot=7)
        n8 = Inventory(text='I8', slot=8)
        n9 = Inventory(text='I9', slot=9)
        n0 = Inventory(text='I0', slot=0)
        self.inventory.add_widget(n1)
        self.inventory.add_widget(n2)
        self.inventory.add_widget(n3)
        self.inventory.add_widget(n4)
        self.inventory.add_widget(n5)
        self.inventory.add_widget(n6)
        self.inventory.add_widget(n7)
        self.inventory.add_widget(n8)
        self.inventory.add_widget(n9)
        self.inventory.add_widget(n0)
        self.nodes = [n1,n2,n3,n4,n5,n6,n7,n8,n9,n0]
        
    def buildUI(self):
        bottomBox = RelativeLayout() # 1024,188
        self.screenManager = KYRScreenManager(size=(1068,450), size_hint=(None,None), pos=(25,224))
        self.info = Info(text=self.infoText, multiline=True,
                        readonly=True, size=(1064,30), size_hint=(None,None), pos=(25,167))
        btnMenu = Button(text='menu', size=(196,120), size_hint=(None,None), pos=(28,16), opacity = .5)
        self.inventory = GridLayout(orientation='vertical',cols=5,pos=(333,-562),spacing=15)
        
        bottomBox.add_widget(self.info)
        bottomBox.add_widget(btnMenu)
        self.add_widget(self.inventory)
        self.add_widget(self.screenManager)
        self.add_widget(bottomBox)
        self.buildInventory() 
        
class GameApp(App):
    
    def build(self):
        return Manager()

if __name__ == "__main__":
    GameApp().run()
    
'''
Created on Sep 17, 2014

@author: Joshua Cox
'''