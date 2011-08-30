import clutter
import pango
import random
import time
import math
import glob

from twisted.internet import task, reactor

from ikcam import stage
from ikcam.gfx import dialogs, default
from banjo.style import Style
from banjo.grid import Grid

import ikcam.gfx.default, ikcam.gfx.util


class Stage (stage.IkCamStage):

    grid = None
    pix = 8. # pixelscale

    a = None
    b = None

    actors = None
    looper = None

    # initial scrolling speed
    initialSpeed = 10

    # determines the smoothness
    tickspeed = 0.02

    
    inputReaderMap = {'A3T6PWW3': 'DOWN',
                      'A3T6PX0O': 'LEFT',
                      'A3T6PWJD': 'UP',
                      'A3T6PX1I': 'RIGHT'}

    start = [0.1, 0.25]
    gametime = 0

    bannergroup = None

    def enter_start(self, s):
        self.set_color(clutter.color_from_string("#000000"))
        if self.a and self.a.original:
            self.a.original.destroy()
            self.a.ship.destroy()
        if self.b and self.b.original:
            self.b.original.destroy()
            self.b.ship.destroy()
        self.a = Avatar(None, None)
        self.b = Avatar(None, None)
 
        self.avatarADisplay.changeAvatar(self.a)
        self.avatarBDisplay.changeAvatar(self.b)

        if self.bannergroup:
            self.bannergroup.destroy()

        self.r = clutter.Rectangle(clutter.color_from_string("#ff0000"))
        self.add(self.r)
        self.r.set_size(10,10)
        self.r.show()

        self.levels = [{'speed': 10, 'enemies': 0},
                       {'speed': 25, 'enemies': 1, 'enemyclass': Simple1},
                       {'speed': 30, 'enemies': 0},
                       {'speed': 30, 'enemies': 1, 'enemyclass': Simple1},
                       {'speed': 50, 'enemies': 2, 'enemyclass': Simple2},
                       {'speed': 70, 'enemies': 3, 'enemyclass': Simple3},
                       {'speed': 100, 'enemies': 2, 'enemyclass': BigBoss}
                       ]
        self.levelUpAfter = 20 # in seconds
        if self.plugin.service.debug:
            self.levelUpAfter = 2

        self.currentLevel = 1
        self.actors = []


    def gotPicture(self, item):
        pass


    def addActor(self, actor):
        actor.set_position(self.width-200,random.random()*self.height)
        actor.angle = random.random()*360.
        self.add(actor)
        actor.show()
        self.actors.append(actor)


    def enter_gameover(self, s):
        for a in self.actors:
            print "doei"
            a.destroy()

        self.setNotifyText("GAME OVER!")
        reactor.callLater(5, self.setNotifyText, "Your banner will be knit!")
        reactor.callLater(17, self.setNotifyText, "Ask the instructor!")


    def loadKnitting(self, png):
        bannergroup = clutter.Group()

        banner = clutter.texture_new_from_file(png)
        banner.set_filter_quality(clutter.TEXTURE_QUALITY_LOW)
        banner.set_rotation(clutter.Z_AXIS, 90.0, banner.get_width()/2, banner.get_height()/2, 0)
        
        bannerrect = clutter.Rectangle(clutter.color_from_string("White"))
        bannerrect.set_size(*banner.get_size())
        
        bannergroup.add(bannerrect)
        bannergroup.add(banner)
        
        self.add(bannergroup)
        bannergroup.show_all()
        return bannergroup


    def showBanner(self, png):
        self.bannergroup = self.loadKnitting(png)
        self.bannergroup.set_position(-self.bannergroup.get_width(), self.height/2-self.bannergroup.get_height()/2)

        p = clutter.Path()
        p.add_move_to(-self.bannergroup.get_width(), self.height/2-self.bannergroup.get_height()/2)
        p.add_rel_line_to(self.width+self.bannergroup.get_width(), 0)

        timeline = clutter.Timeline(20000)
        alpha = clutter.Alpha(timeline, clutter.LINEAR)
        self.r_behaviour = clutter.BehaviourPath(alpha, p)
        self.r_behaviour.apply(self.bannergroup)
        timeline.start()


    def enter_wait1(self, s):
        self.setNotifyText("Place your tags!")
        self.bgscroller.start()
        self.stage.set_key_focus(self.stage)


    def enter_wait2(self, s):
        self.setNotifyText("Find an opponent!")
        participant = self.plugin.participants[self.plugin.tags[0]]
        self.a = Avatar(participant['the_name'].split(" ")[0], participant['avatar'])
        self.add(self.a.original)
        self.add(self.a.ship)
        self.avatarADisplay.changeAvatar(self.a)
        self.avatarADisplay.setpos()

        self.a.ship.set_rotation(clutter.Z_AXIS, 90.0, 8*self.pix, 8*self.pix, 0)
        self.a.ship.set_position(self.start[0]*self.width, self.start[1]*self.height)
        self.a.appear()


    def enter_getready(self, s):
        self.setNotifyText("Get ready!")
        participant = self.plugin.participants[self.plugin.tags[1]]
        self.b = Avatar(participant['the_name'].split(" ")[0], participant['avatar'])
        self.add(self.b.original)
        self.add(self.b.ship)
        self.avatarBDisplay.changeAvatar(self.b)
        self.avatarBDisplay.setpos(right=True)

        self.b.ship.set_rotation(clutter.Z_AXIS, 90.0, 8*self.pix, 8*self.pix, 0)
        self.b.ship.set_position(self.start[0]*self.width, self.height-self.start[1]*self.height)
        self.b.appear()


    def enter_c3(self, s):
        self.setNotifyText(" 3 ", 400)

    def enter_c2(self, s):
        self.setNotifyText(" 2 ", 400)

    def enter_c1(self, s):
        self.setNotifyText(" 1 ", 400)

    def enter_playing(self, s):
        self.bgscroller.setSpeed(self.initialSpeed)
        self.setNotifyText("Go!!", 300)
        self.a.respawn()
        self.b.respawn()
        self.timePlayed = 0
        reactor.callLater(3, self.setNotifyText, False)


    def gameTick(self):

        if self.plugin.state != "playing":
            return

        self.timePlayed += self.tickspeed

        if self.timePlayed > self.currentLevel * self.levelUpAfter and self.currentLevel < len(self.levels):
            self.currentLevel += 1
            level = self.levels[self.currentLevel-1]
            # set level variables
            print "levelup !!"
            self.bgscroller.setSpeed(level['speed'])

            if 'enemies' in level:
                for r in range(level['enemies']):
                    self.addActor(level['enemyclass'](self))

            if random.random() > .3:
                self.addActor(InvincibleBonus(self))
            if random.random() > .3:
                self.addActor(InvincibleBonus(self))


        # process all the actors
        for a in self.actors:
            a.tick()

        # animate the scroller
        self.bgscroller.tick()

        # move the characters
        self.a.ship.set_position(self.a.ship.get_x()+self.pix*self.a.dx*self.tickspeed,
                                  self.a.ship.get_y()+self.pix*self.a.dy*self.tickspeed)
        self.b.ship.set_position(self.b.ship.get_x()+self.pix*self.b.dx*self.tickspeed,
                                  self.b.ship.get_y()+self.pix*self.b.dy*self.tickspeed)

        # perform colosion detection
        if self.checkCollide(self.a):
            self.avatarADisplay.update()
        if self.checkCollide(self.b):
            self.avatarBDisplay.update()

        if self.a.lives == 0 or self.b.lives == 0:
            if self.a.lives == 0:
                self.plugin.winner = self.plugin.tags[1]
                self.plugin.loser = self.plugin.tags[0]
            else:
                self.plugin.winner = self.plugin.tags[0]
                self.plugin.loser = self.plugin.tags[1]
            self.plugin.setState("gameover")


    def checkCollide(self, avatar):
        if avatar.invincible:
            return

        x, y = avatar.ship.get_position()
        x += avatar.ship.get_width()/2
        y += avatar.ship.get_height()/2

        collision = False
        if x < 0 or x >= self.width:
            collision = True
        if y < 0 or y >= self.height:
            collision = True

        if not collision:
            x, y = self.world2game(x, y)
            collision = self.bgscroller.check(-x, y)
            
            # for tx in range(avatar.silhouette.get_cols()):
            #     for ty in range(avatar.silhouette.get_rows()):
            #         if avatar.silhouette.get(tx, ty):
            #             collision = self.bgscroller.check(-x-ty+8, y+tx-12)
            #             #collision = self.bgscroller.check(-x - ty, y + tx)
            #             if collision:
            #                 break

        if not collision:
            # check actors
            x, y = avatar.ship.get_position()
            x = int(x/80)
            y = int(y/80)
            for a in self.actors:
                ax, ay = a.get_position()
                ax = int(ax/80)
                ay = int(ay/80)
                if ax == x and ay == y:
                    die = a.collide(avatar)
                    if die:
                        collision = True
                    if collision:
                        break


        if collision:
            # EXPLODE!!! 
            y = self.start[1]*self.height
            if avatar == self.b:
                y = self.height - y
            avatar.ship.set_position(self.start[0]*self.width, y)
            avatar.respawn()
            avatar.lives -= 1
            return True
        return False


    def keypress(self, x, e):
        # x, y = self.world2game(*self.box.get_position())
        if self.plugin.state != "management":
            return
        sym = e.get_key_symbol()
        from gtk import keysyms
        if sym == keysyms.Up:
            # print!
            return
        if sym == keysyms.Down:
            # cancel
            self.plugin.setState("start")
            return
        if sym == keysyms.Left:
            # previuos knitting
            self.currentKnitting = (self.currentKnitting + self.currentKnitting - 1) % len(self.bitmaps)
        if sym == keysyms.Right:
            self.currentKnitting = (self.currentKnitting + 1) % len(self.bitmaps)

        self.showKnitting(self.bitmaps[self.currentKnitting])
        pass


    def setStage(self, stage):

        # starting the tick
        if self.looper:
            self.looper.stop()
        self.looper = task.LoopingCall(self.gameTick)
        self.looper.start(self.tickspeed)

        self.stage = stage
        self.stage.set_anchor_point(self.stage.get_width()/2, self.stage.get_height()/2)
        self.stage.set_scale(0.97, 0.97)

        self.connect("key-press-event", self.keypress)

        self.bgscroller = SideScroller("gamedata/background_1_favorite.png", self.initialSpeed, self.tickspeed)
        self.bgscroller.set_position(10,0)
        self.bgscroller.set_rotation(clutter.Z_AXIS, 90.0, 0, 0, 0)

        self.add(self.bgscroller)

        self.fadeRect = clutter.Rectangle(clutter.color_from_string("#ffffff"))
        self.fadeRect.show()
        self.add(self.fadeRect)

        self.a = Avatar("Player1", "gamedata/dino_top1.png")
        self.avatarADisplay = AvatarDisplay(self.a)
        self.add(self.avatarADisplay)
        self.avatarADisplay.set_rotation(clutter.Z_AXIS, 90.0, 0, 0, 0)

        self.b = Avatar("Player2", "gamedata/dino_top1.png")
        self.avatarBDisplay = AvatarDisplay(self.b)
        self.add(self.avatarBDisplay)
        self.avatarBDisplay.set_rotation(clutter.Z_AXIS, 90.0, 0, 0, 0)

        self.tagtext = ikcam.gfx.default.ShadowedText("TAG", 100, "#00ff00")
        self.tagtext.hide()
        self.add(self.tagtext)

        self.tagArect = clutter.Clone(self.tagtext)
        self.tagArect.set_rotation(clutter.Z_AXIS, 90.0, 0.0, self.tagtext.get_height(), 0.0)
        self.tagArect.show()
        self.add(self.tagArect)

        self.tagBrect = clutter.Clone(self.tagtext)
        self.tagBrect.set_rotation(clutter.Z_AXIS, 90.0, 0.0, self.tagtext.get_height(), 0.0)
        self.tagBrect.show()
        self.add(self.tagBrect)




    def world2game(self, x, y):
        return x/self.pix, y/self.pix


    def game2world(self, x, y):
        return x*self.pix, y*self.pix


    def setSize(self, width, height):
        self.width = width
        self.height = height
        self.stage.set_size(width, height)
        self.reposition()


    def tagAdded(self, e):

        tag = "urn:rfid:" + e.data

        if self.plugin.state != "playing":
            self.tagArect.show()
            self.tagBrect.show()


        direction = self.inputReaderMap[e.service.serial]
        #print "direction", e.service.serial, direction

        if self.plugin.state == "management":
            self.plugin.delayTimeOut()
            self.handleManagementTag(tag, direction)

        if self.plugin.state != "playing":
            return


        if len(self.plugin.tags) and tag == self.plugin.tags[0]:
            self.tagArect.show()
            avatar = self.a
        elif len(self.plugin.tags)>1 and tag == self.plugin.tags[1]:
            self.tagBrect.show()
            avatar = self.b
        else:
            return
        avatar.setDirection(direction)


    def tagRemoved(self, e):
        if self.plugin.state != "playing":
            self.tagArect.hide()
            self.tagBrect.hide()
            return

        tag = "urn:rfid:" + e.data
        if len(self.plugin.tags) and tag == self.plugin.tags[0]:
            self.tagArect.hide()
            avatar = self.a
        elif len(self.plugin.tags)>1 and tag == self.plugin.tags[1]:
            self.tagBrect.hide()
            avatar = self.b
        else:
            return
        avatar.setDirection(None)


    def reposition(self):
        if self.notify_text:
            if self.notify_coordinates_set==False:
                self.notify_text.set_position(0, self.height/2. - self.notify_text.get_height()/2.)

        self.fadeRect.lower_bottom()
        self.fadeRect.set_position(0,0)
        self.fadeRect.set_size(self.width, self.height)
        self.fadeRect.set_opacity(180)
        # if self.camera_texture:
        #     sc = max(float(self.height)/self.camera_texture.get_height(), float(self.width)/self.camera_texture.get_width())
        #     self.camera_texture.lower_bottom()
        #     self.camera_texture.set_scale(sc, sc)
        #     self.camera_texture.set_position(self.width/2, self.height/2)

        # how big is 1 pixel?
        self.pix = self.height / float(self.bgscroller.w)
        self.bgscroller.set_scale(self.pix, self.pix)
        #self.bgscroller.set_position(400,100)

        self.avatarADisplay.set_position(self.width, 20)
        self.avatarBDisplay.set_position(self.width, self.height-20)
        self.avatarADisplay.setpos(right=False)
        self.avatarBDisplay.setpos(right=True)

        self.tagArect.set_position(30, -20)
        self.tagBrect.set_position(30, self.height - self.tagBrect.get_width()-100)



    def setNotifyText(self, message, size=100, color="#00ff00", x=0, y=0, blinkspeed=500):
        """
        Set a notification text. Rotated to fit the screen.
        """
        if self.notify_text:
            self.stage.remove(self.notify_text)
            self.notify_text = None
        if not message:
            return

        if x!=0 or y!=0:
            self.notify_coordinates_set = True

        self.notify_text = ikcam.gfx.default.ShadowedText(message, size, color, x=x, y=y)
        self.notify_text.set_rotation(clutter.Z_AXIS, 90.0, self.notify_text.get_width()/2, self.notify_text.get_height()/2, 0)
        self.notify_text.show_all()
        self.stage.add(self.notify_text)

        self.b_behaviour = BehaviourBlink(blinkspeed)
        self.b_behaviour.apply(self.notify_text)

        self.reposition()


    def message(self, message):
        self.setNotifyText(self, message, size=100, color="#ff9900", x=0, y=0, blinkspeed=50)


    def setError(self, text):

        def rmerr():
            self.stage.remove(self.error_text)
            self.error_text = None
            self.error_call = None

        if self.error_call:
            self.error_call.cancel()
            self.error_call = None
        if self.error_text:
            rmerr()
        
        self.error_text = default.ShadowedText(text, 70, "#FFFF00")
        self.error_text.set_position(self.width/2., self.height/2.)
        self.error_text.set_rotation(clutter.Z_AXIS, 90.0, self.error_text.get_width()/2, self.error_text.get_height()/2, 0)
        self.error_text.show_all()
        self.stage.add(self.error_text)

        self.error_call = reactor.callLater(4, rmerr)


    def enter_management(self, s):
        self.setNotifyText("left  = prev\nright = next\n\ndown  = cancel\nup    = print!")
        self.bitmaps = glob.glob("/home/mediamatic/work/banjo/output/*.bmp")
        self.managementState = "start"
        self.knitting = None
        self.currentKnitting = 0
        if not len(self.bitmaps):
            self.plugin.error("No results waiting to knitted!")
            self.plugin.setState("start")
            return
        self.showKnitting(self.bitmaps[self.currentKnitting])


    def showKnitting(self, bmp):
        png = bmp.replace(".bmp", ".png")
        if self.knitting:
            self.knitting.destroy()
        self.knitting = self.loadKnitting(png)
        self.knitting.set_position(self.width/2-self.knitting.get_width()/2., self.height/2-self.knitting.get_height()/2)


    def exit_management(self, s):
        if self.knitting:
            self.knitting.destroy()


    def handleManagementTag(self, tag, direction):
        if self.managementState == "start":
            self.managementState = "choose"
            return

        if self.managementState == "choose":
            if direction == 'RIGHT':
                self.currentKnitting += 1
                if self.currentKnitting >= len(self.bitmaps): self.currentKnitting = 0
                print self.bitmaps
                print self.currentKnitting
                self.showKnitting(self.bitmaps[self.currentKnitting])
                return
            if direction == 'LEFT':
                self.currentKnitting -= 1
                if self.currentKnitting < 0: self.currentKnitting = len(self.bitmaps)-1
                print self.bitmaps
                print self.currentKnitting
                self.showKnitting(self.bitmaps[self.currentKnitting])
                return
            if direction == 'DOWN':
                self.plugin.setState("start")
            if direction == 'UP':
                self.plugin.setState("management_print")


    def enter_management_print(self, s):
        target = self.bitmaps[self.currentKnitting]
        self.showKnitting(target)
        self.setNotifyText("\nProgramming the knitting\nmachine! This takes up to\n45 seconds. Please wait.")


    def exit_management_print(self, s):
        self.knitting.destroy()


    def enter_management_printed(self, s):
        self.setNotifyText("The operator can now start knitting!!")





class Avatar(object):

    def __init__(self, name, imagefile=None, cellsize=2):
        self.dx = 0
        self.dy = 0
        self.original = None
        self.ship = None
        self.imagefile = None
        self.speed = 0 # game units per second

        if imagefile:
            self.original = clutter.Group()
            im = clutter.texture_new_from_file(imagefile)
            im.set_filter_quality(clutter.TEXTURE_QUALITY_LOW)
            g = Grid.from_file(imagefile, cellsize)
            g.invert()
            self.silhouette = Grid.as_silhouette(g)
            fn = "/tmp/sil%d.png" % time.time()
            self.silhouette.to_file(fn, cellsize, fg=(255,255,255,255), bg=(0,0,0,0))
            re = clutter.texture_new_from_file(fn)
            re.set_filter_quality(clutter.TEXTURE_QUALITY_LOW)
            re.show()
            w = im.get_width()
            im.set_size(w*4, w*4)
            #re = clutter.Rectangle(clutter.color_from_string("#ffffff"))
            re.set_size(im.get_width(), im.get_height())
            self.original.add(re)
            self.original.add(im)
            self.original.set_opacity(0)
            self.original.show()
            self.ship = clutter.Clone(self.original)
            self.imagefile = imagefile

            speedfact = self.silhouette.count_pixels()/float(16*16)
            self.speed = 15 + (1-speedfact) * 10 # max speed = 25


        self.invincible = False
        self.respawnInvincibleTime = 1
        self.name = name
        self.lives = 5
        self.isHit = False


    def respawn(self):
        self.setInvincible(self.respawnInvincibleTime)


    def setInvincible(self, t):
        self.invincible = True
        self.b = BehaviourBlink(200, t, blinkdrop=255)
        self.b.apply(self.ship)
        def vincible():
            self.invincible = False
        reactor.callLater(t, vincible)


    def setDirection(self, dir):
        self.dx = 0
        self.dy = 0
        if dir == 'UP':
            self.dx = 1
        if dir == 'DOWN':
            self.dx = -1
        if dir == 'LEFT':
            self.dy = -1
        if dir == 'RIGHT':
            self.dy = 1

        self.dx *= self.speed
        self.dy *= self.speed


    def appear(self):
        self.ship.set_opacity(255)
        self.ship.show()



class AvatarDisplay(clutter.Group):
    __gobject_type = "SideScroller"

    def __init__(self, avatar):
        clutter.Group.__init__(self)
        self.name = None
        self.lives = None
        self.livecount = None
        self.image = None
        self.rect = None
        self.changeAvatar(avatar)

    def changeAvatar(self, avatar):
        self.avatar = avatar
        if self.name:
            self.name.destroy()
        self.name = clutter.Text("Ernest 100px", "", clutter.color_from_string("White"))
        self.add(self.name)

        if self.lives:
            self.lives.destroy()
        self.lives = clutter.Text("Ernest 50px", "Lives:", clutter.color_from_string("White"))
        self.lives.set_position(0, 90)
        self.add(self.lives)

        if self.livecount:
            self.livecount.destroy()
        self.livecount = clutter.Text("Ernest 120px", "", clutter.color_from_string("Green"))
        self.livecount.set_position(0, 100)
        self.add(self.livecount)

        if self.image:
            self.image.destroy()
        if self.rect:
            self.rect.destroy()

        self.image = None
        if self.avatar.imagefile:
            self.image = clutter.Clone(self.avatar.original)
            self.add(self.image)
            h = self.name.get_height()
            self.image.set_size(h,h)

        self.show_all()
        self.update()


    def setLives(self, lives):
        if lives > 3:
            color = "Green"
        else:
            color = "Red"
        s = "*" * lives
        self.livecount.set_text(s)
        self.livecount.set_color(clutter.color_from_string(color))
        self.lives.set_text("Lives: %d" % lives)


    def update(self):
        self.setLives(self.avatar.lives)

        if self.avatar.name is None:
            self.name.set_text("-swipe-")
            self.b = BehaviourBlink(200) # forever
        else:
            self.name.set_text(self.avatar.name)
            self.b = BehaviourBlink(100, 1.5)

        self.b.apply(self.name)
        if self.image:
            self.b.apply(self.image)


    def setpos(self, right=False):
        if self.image:
            w = self.image.get_width()
            p = 0.2*w
        else:
            w = 0
            p = 0
        if right:
            self.name.set_x(-self.name.get_width()-p-w)
            if self.image:
                self.image.set_x(-w)
            self.lives.set_x(-self.lives.get_width())
            self.livecount.set_x(-self.livecount.get_width())
        else:
            self.name.set_x(p+w)


class SideScroller (clutter.Group):
    __gobject_type = "SideScroller"

    def __init__(self, file, pixels_per_second=200, tickspeed=0.05):
        clutter.Group.__init__(self)
        self.image = clutter.texture_new_from_file(file)
        self.image.set_filter_quality(clutter.TEXTURE_QUALITY_LOW)
        self.image.hide()
        self.textures = [clutter.Clone(self.image),
                         clutter.Clone(self.image)]
        self.add(self.image)

        self.grid = Grid.from_file(file)

        self.h = self.image.get_height()
        self.w = self.image.get_width()

        self.add(self.textures[0])
        self.add(self.textures[1])

        self.pixels_per_second = pixels_per_second
        self.tickspeed = tickspeed

        self.currentheight = int(random.random()*self.h)

        self.running = True


    def setSpeed(self, pixels_per_second):
        self.pixels_per_second = pixels_per_second


    def start(self):
        self.running = True
        self.textures[0].show()
        self.textures[1].show()
        self.textures[0].set_y(self.currentheight-self.h)
        self.textures[1].set_y(self.currentheight-self.h*2)


    def stop(self):
        self.running = False
        self.currentheight = self.h/2
        self.textures[0].set_y(self.currentheight-self.h)
        self.textures[1].set_y(self.currentheight-self.h*2)


    def tick(self):
        if not self.running:
            return
        self.textures[0].set_y(self.currentheight-self.h)
        self.textures[1].set_y(self.currentheight-self.h*2)
        self.currentheight += self.pixels_per_second/(1/self.tickspeed)

        if self.currentheight > self.h:
            # swap the textures
            self.currentheight = 0
            self.textures = [self.textures[1], self.textures[0]]
            print "*****"


    def check(self, ox, oy):
        # ox = 0
        # oy = 0
        x = oy
        y = ox-self.currentheight
        if y < 0:
            y += self.grid.get_rows()
        return self.grid.get(int(x), int(y))




class GameObject(clutter.Group):
    __gtype_name__ = "Floater"

    def __init__(self, stage, imgfile):
        clutter.Group.__init__(self)
        self.image = clutter.texture_new_from_file(imgfile)
        self.image.set_filter_quality(clutter.TEXTURE_QUALITY_LOW)
        self.image.set_scale(stage.pix, stage.pix)
        self.stage = stage
        self.image.show()
        self.add(self.image)

        self.b = BehaviourBlink(100, 1, blinkdrop=255)
        self.b.apply(self)

        w2, h2 = self.image.get_width()/2, self.get_height()/2
        self.set_anchor_point(w2, h2)

        self.speed = 10 # pixels/sec
        self.angle = 180.0
        self.bouncecount = 0
        self.maxbounce = None


    def tick(self):
        x = self.get_x()
        y = self.get_y()

        dx = self.speed * math.cos(self.angle/(180/math.pi))
        dy = self.speed * math.sin(self.angle/(180/math.pi))

        self.set_rotation(clutter.Z_AXIS, 180.0+self.angle, self.get_width()/2, self.get_height()/2, 0.0)

        if x + dx < 0:
            self.angle = math.atan2(dy, -dx) * (180/math.pi)
            self.bouncecount += 1
        if x + dx >= self.stage.width:
            self.angle = math.atan2(dy, -dx) * (180/math.pi)
            self.bouncecount += 1
        else:
            x += dx

        if y + dy < 0:
            self.angle = math.atan2(-dy, dx) * (180/math.pi)
            self.bouncecount += 1
        if y + dy >= self.stage.height:
            self.angle = math.atan2(-dy, dx) * (180/math.pi)
            self.bouncecount += 1
        else:
            y += dy

        if self.maxbounce is not None and self.bouncecount > self.maxbounce:
            self.remove()
        self.set_position(x, y)


    def remove(self):
        i = self.stage.actors.index(self)
        del self.stage.actors[i]
        self.destroy()


    def collide(self, avatar):
        print "collision of %s with %s" % (avatar.name, str(self))
        return True # die!



class Simple1(GameObject):
    def __init__(self, stage):
        GameObject.__init__(self, stage, "gamedata/dino_top5.png")
        self.speed = 4
        self.maxbounce = 3


class Simple2(GameObject):
    def __init__(self, stage):
        GameObject.__init__(self, stage, "gamedata/dino_top3.png")
        self.speed = 3
        self.maxbounce = 5


class Simple3(GameObject):
    def __init__(self, stage):
        GameObject.__init__(self, stage, "gamedata/dino_top4.png")
        self.speed = 5
        self.maxbounce = 5


class BigBoss(GameObject):
    def __init__(self, stage):
        GameObject.__init__(self, stage, "gamedata/dino3.png")
        self.speed = 3


class InvincibleBonus(GameObject):
    def __init__(self, stage):
        GameObject.__init__(self, stage, "gamedata/banjo2.png")
        self.speed = 5
        self.maxbounce = 5

    def collide(self, avatar):
        avatar.setInvincible(20)
        self.remove()
        return False




class BehaviourBlink(clutter.Behaviour):
    __gtype_name__ = 'BehaviourBlink'

    def __init__(self, speed=50, secs=None, blinkdrop=128):
        clutter.Behaviour.__init__(self)
        if not secs:
            time = int(100 * speed)
        else:
            time = int(1000 * secs)
        n = 2 * time / speed
        timeline = clutter.Timeline(time)
        alpha = clutter.Alpha(timeline, clutter.LINEAR)
        self.blinkdrop = blinkdrop
        self.set_alpha(alpha)
        self.n = n
        if secs is None: # looping
            timeline.set_loop(True)
        else:
            def appear(t):
                for a in self.get_actors():
                    a.set_opacity(255)
            timeline.connect("completed", appear)
        timeline.start()


    def do_alpha_notify(self, alpha_value):
        opacity = int(alpha_value*self.n)%2 * self.blinkdrop
        for actor in self.get_actors():
            actor.set_opacity(opacity+(255-self.blinkdrop))

