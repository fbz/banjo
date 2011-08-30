import random
import clutter

from ikcam import stage
from ikcam.gfx import dialogs, default
from banjo.style import Style
from banjo.grid import Grid


class Stage (stage.IkCamStage):

    grid = None


    def enter_start(self, s):
        self.set_color(clutter.color_from_string("#000000"))
        self.setNotifyText("Place your tag to edit your avatar!!")
        for a in self.actors:
            a.show()


    def exit_start(self, s):
        for a in self.actors:
            a.hide()


    def enter_loading(self, s):
        self.setNotifyText("Loading your avatar...")


    def enter_saving(self, s):
        self.setNotifyText("Saving...")


    def addActor(self, actor):
        actor.set_position(self.width-200,random.random()*self.height)
        actor.angle = random.random()*360.
        self.add(actor)
        actor.show()
        self.actors.append(actor)


    def setNotifyText(self, message, size=100, color="#ffffff", x=0, y=0, blinkspeed=500):
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

        self.notify_text = default.ShadowedText(message, size, color, x=x, y=y)
        self.stage.add(self.notify_text)

        self.reposition()


    def enter_editing(self, s):
        self.set_color(clutter.color_from_string("#666666"))

        self.grid = PixelGrid(self.plugin.spriteGrid, 40)
        self.grid.changedHandler = self.plugin.delayTimeOut
        
        self.add(self.grid)

        self.stage.show_all()

        self.setNotifyText(self.plugin.user['the_name']+"'s avatar")

        self.buttons = []
        def verify():
            if self.plugin.validSprite():
                self.plugin.saveAndStop()
            else:
                self.plugin.error("Your avatar is too small.")
 
        self.buttons.append(dialogs.RoundedButton(self, "done!", 50, 100, verify))

        self.buttons.append(dialogs.RoundedButton(self, "invert", 50, 200, lambda : self.grid.invert()))
        self.buttons.append(dialogs.RoundedButton(self, "clear", 50, 300, lambda : self.grid.clear()))
        self.buttons.append(dialogs.RoundedButton(self, "cancel", 50, 400, lambda : self.plugin.setState("start"), color=Style.button_color_secondary))

        [self.add(b) for b in self.buttons]
        self.reposition()


    def exit_editing(self, s):
        self.grid.destroy()
        [b.destroy() for b in self.buttons]


    def setStage(self, stage):
        self.actors = []
        self.stage = stage


    def setSize(self, width, height):
        self.width = width
        self.height = height
        self.stage.set_size(width, height)
        self.reposition()


    def tagAdded(self, e):
        pass

    def tagRemoved(self, e):
        pass


    def reposition(self):
        if self.grid:
            self.grid.set_x(self.stage.get_width()/2-self.grid.get_width()/2)
            self.grid.set_y(45)
        if self.notify_text:
            if self.notify_coordinates_set==False:
                self.notify_text.set_position(self.width/2. - self.notify_text.get_width()/2., self.height * 0.85)



class PixelGrid (clutter.Group):

    __gobject_type = "PixelGrid"

    def __init__(self, grid, size):
        clutter.Group.__init__(self)
        self.size = size
        self.boxes = []
        self.grid = grid

        self.mini = MiniSprite(Grid.as_silhouette(grid), size)
        self.mini.show()
        self.add(self.mini)

        self.rect = clutter.Rectangle()
        self.rect.set_color(clutter.color_from_string("#ffffff"))
        self.rect.set_opacity(50)
        self.rect.set_position(0,0)
        self.rect.set_size(self.grid.get_cols()*size, self.grid.get_rows()*size)
        self.rect.show()
        self.add(self.rect)

        w, h = self.grid.get_size()

        self.set_reactive(True)
        self.connect("button-press-event", self.pressed)
        self.connect("button-release-event", self.released)
        self.connect("motion-event", self.moved)

        self.changedHandler = None

        def makegetter(x, y):
            def cb():
                return self.grid.get(x, y)
            return cb

        def maketoggler(x, y):
            def cb():
                return self.grid.toggle(x, y)
            return cb

        for x in range(w):
            self.boxes.append([])
            for y in range(h):
                t = Toggler(size-2, maketoggler(x, y), makegetter(x, y))
                t.set_position(x*size+1, y*size+1)
                t.active = True
                self.add(t)
                self.boxes[x].append(t)
        self.painting = False
        self.paintWhat = False
        self.show_all()


    def changed(self):
        if callable(self.changedHandler):
            self.changedHandler()


    def clear(self):
        self.changed()
        self.grid.clear()
        self.repaint()


    def invert(self):
        self.changed()
        self.grid.invert()
        self.repaint()


    def repaint(self):
        self.mini.grid = Grid.as_silhouette(self.grid)
        self.mini.repaint()
        for l in self.boxes:
            for b in l:
                b.paint()
    

    def getpos(self, event):
        x = int( (event.x-self.get_x())/self.size)
        y = int( (event.y-self.get_y())/self.size)
        return x, y


    def pressed(self, actor, event):
        self.changed()
        x, y =  self.getpos(event)
        self.grid.toggle(x, y)
        self.boxes[x][y].paint()
        self.mini.grid = Grid.as_silhouette(self.grid)
        self.painting = True
        self.paintWhat = self.grid.get(x, y)


    def released(self, actor, event):
        self.changed()
        self.painting = False
        self.mini.grid = Grid.as_silhouette(self.grid)
        self.mini.repaint()


    def moved(self, actor, event):
        self.changed()
        if not self.painting:
            return
        x, y =  self.getpos(event)
        if self.grid.get(x, y) == self.paintWhat:
            return
        self.grid.set(x, y, self.paintWhat)
        self.boxes[x][y].paint()



class Toggler (clutter.Group):

    active = False

    def __init__(self, size, toggler, getter):
        clutter.Group.__init__(self)
        self.toggler = toggler
        self.getter = getter
        self.size = size
        self.rect = clutter.Rectangle()
        self.rect.set_size(size, size)
        self.rect.set_color(clutter.color_from_string("#000000"))
        self.add(self.rect)
        self.active = True
        self.paint()


    def paint(self):
        # if self.getter():
        #     self.rect.set_opacity(255)
        # else:
        #     self.rect.set_opacity(0)
        # return
        timeline = clutter.Timeline(200)
        alpha = clutter.Alpha(timeline, clutter.LINEAR)
        if self.getter():
            self.b = clutter.BehaviourOpacity(0,255,alpha)
        else:
            self.b = clutter.BehaviourOpacity(255,0,alpha)
        self.b.apply(self.rect)
        timeline.start()


class MiniSprite (clutter.CairoTexture):
    """
    A non-interactive sprite, based on a grid.
    """

    def __init__(self, grid, cellsize=1):
        clutter.CairoTexture.__init__(self, grid.get_cols()*cellsize, grid.get_rows()*cellsize)
        self.grid = grid
        self.cellsize = cellsize
        self.repaint()
        #self.grid.events.addObserver("set", self.repaint)

    def repaint(self, *a):
        self.clear()
        cr = self.cairo_create()

        for x in range(self.grid.get_cols()):
            for y in range(self.grid.get_rows()):
                if self.grid.get(x, y):
                    cr.rectangle(x*self.cellsize+1, y*self.cellsize+1, self.cellsize-2, self.cellsize-2)
                    cr.set_source_rgb(1, 1, 1)
                    cr.fill()



    

