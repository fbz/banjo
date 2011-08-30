#!/usr/bin/env python

#from sparked import events

class BlendMode:
    OVERWRITE = 1
    AND = 2
    XOR = 3
    OR = 4


class Grid:

    _state = None
    
    _client = None # OSC client
    _pid = None # PID of running interpreter

    _cycles = 0


    def __init__(self, cols, rows):
        """ Initialize a grid, with rows and cols """
        self._state = {}
        self._state['rows'] = rows;
        self._state['cols'] = cols;
        self._state['data'] = [0] * self._state['rows']
        #self.events = events.EventDispatcher()


    def from_file(cls, fn, cellwidth=1):
        """ Initialize a grid from an image file. Static method: the
        image dimensions form the grid dimensions."""

        from PIL import Image
        im = Image.open(fn)
        w, h = im.size

        g = cls(w//cellwidth, h//cellwidth)
        g.clear()
        g.fill_from_image(im, cellwidth)
        return g
    from_file = classmethod(from_file)


    def to_file(self, filename, cellwidth=1, fg=(0,0,0,255), bg=(0,0,0,0), bitmap=False):

        from PIL import Image, ImageDraw
        im = Image.new("RGBA", (self._state['cols']*cellwidth, self._state['rows']*cellwidth), bg)

        draw = ImageDraw.Draw(im)
        
        for x in range(self._state['cols']):
            for y in range(self._state['rows']):
                if self.get(x, y):
                    fill = fg
                else:
                    fill = bg
                draw.rectangle( ( (x*cellwidth, y*cellwidth), ((x+1)*cellwidth, (y+1)*cellwidth)), fill=fill)
        if bitmap:
            im = im.convert("1")
        im.save(filename, filename.split(".")[-1].upper())
        


    def fill_from_image(self, im, cellwidth=1):
        """ Given a PIL image, fill the current grid with the
        image. Black pixels are left empty: non-black pixels
        give a"filled" pixel. Note: no bounds checking is
        done on the image! """

        for x in range(self._state['cols']):
            for y in range(self._state['rows']):
                try:
                    val = im.getpixel((x*cellwidth,y*cellwidth))
                except IndexError:
                    continue
                if type(val) == tuple:
                    if len(val) == 2:
                        val = val[1] # indexed + alpha
                    elif len(val) == 3:
                        val = sum(val)
                    else:
                        val = 255-val[3] # alpha channel RGBA
                if val > 0:
                    self.set(x, y, True)
        pass


    def resize(self, w, h):
        self._state['cols'] = w
        self._state['rows'] = h


    def _warp(self, x, y):
        """ Given a coordinate, 'warp' it so it falls into the
        grid. Can be overridden to get different grid behaviour."""

        return x, y


    def get(self, x, y):
        """ Get the pixel at (x,y). Returns TRUE when filled, or FALSE when empty. """
        x, y = self._warp(x, y)
        if x < 0 or y < 0 or x >= self._state['cols'] or y >= self._state['rows']:
            return False
        return bool(self._state['data'][y] & (1<<x))


    def set(self, x, y, val):
        """ Set the pixel at (x,y) to val (TRUE or FALSE). """
        x, y = self._warp(x, y)
        if x < 0 or x >= self.get_cols(): return
        if y < 0 or y >= self.get_rows(): return

        if val == True:
            self._state['data'][y] = self._state['data'][y] | (1<<x)
        else:
            self._state['data'][y] = self._state['data'][y] & (((1<<self._state['cols'])-1) ^ (1<<x))
        #self.events.dispatch("set", x, y, val)


    def toggle(self, x, y):
        """ toggle a pixel """
        self.set(x, y, not self.get(x, y))


    def clear(self):
        """ Clear the grid -- all pixels black. """
        self._state['data'] = [0] * self._state['rows']
        #self.events.dispatch("clear")


    def invert(self):
        """ Invert all pixels in the grid. """
        self._state['data'] = [((1<<self._state['cols'])-1) ^ c for c in self._state['data']]
        #self.events.dispatch("invert")


    def fill(self):
        """ Fill the grid. """
        self.clear()
        self.invert()


    def __str__(self):
        """ Represent this grid as a string, for debugging and such. """
        s = "Grid %dx%d:\n" % (self._state['cols'], self._state['rows'])
        for y in range(self._state['rows']):
            for x in range(self._state['cols']):
                if self.get(x, y):
                    s += "X"
                else:
                    s += "."
            s += "\n"
        return s


    def map(self, callback):
        """ Map the grid onto something. Callback takes 3 args: x, y, state. """
        for y in range(self._state['rows']):
            for x in range(self._state['cols']):
                callback(x, y, self.get(x, y))


    def get_size(self):
        """ Return the size tuple of this grid (cols, rows). """
        return self._state['cols'], self._state['rows']


    def get_cols(self):
        """ Return the number of columns in this grid. """
        return self._state['cols']


    def get_rows(self):
        """ Return the number of rows in this grid. """
        return self._state['rows']


    def put(self, grid, x=0, y=0, blend=BlendMode.OVERWRITE):
        """ Put a grid onto another grid. """
        for tx in range(grid.get_cols()):
            for ty in range(grid.get_rows()):
                new = grid.get(tx, ty)
                old = self.get(x+tx, y+ty)
                if blend == BlendMode.OVERWRITE:
                    value = new
                elif blend == BlendMode.AND:
                    value = old and new
                elif blend == BlendMode.XOR:
                    value = old ^ new
                elif blend == BlendMode.OR:
                    value = old or new
                self.set(x+tx, y+ty, value)

    def line(self, y, pattern="X "):
        repeat = int(self.get_cols()/len(pattern))+1
        s = repeat * pattern
        for x in range(self.get_cols()):
            self.set(x, y, s[x] != " ")


    def vline(self, x, pattern="X "):
        repeat = int(self.get_cols()/len(pattern))+1
        s = repeat * pattern
        for y in range(self.get_rows()):
            self.set(x, y, s[y] != " ")


    def as_silhouette(cls, grid):
        agenda = []
        w = grid.get_cols()
        h = grid.get_rows()
        newgrid = Grid(w, h)
        newgrid.clear()
        for x in range(w):
            agenda.append( (x,0) )
            agenda.append( (x,h-1) )
        for y in range(h):
            agenda.append( (0,x) )
            agenda.append( (w-1,x) )

        def look(x,y):
            if x<0 or x >= w or y<0 or y>=h:
                # limit
                return
            if grid.get(x,y) or newgrid.get(x,y):
                # border or already seen
                return
            newgrid.set(x,y,True)
            agenda.append((x-1,y))
            agenda.append((x+1,y))
            agenda.append((x,y-1))
            agenda.append((x,y+1))

        while len(agenda):
            todo = agenda.pop()
            look(*todo)
        newgrid.invert()
        return newgrid

    as_silhouette = classmethod(as_silhouette)


    def count_pixels(self):
        cnt = 0
        for x in range(self.get_cols()):
            for y in range(self.get_rows()):
                if self.get(x, y):
                    cnt += 1
        return cnt

    def flip(self):
        newgrid = Grid(self.get_cols(), self.get_rows())
        for y in range(self.get_rows()):
            for x in range(self.get_cols()):
                newgrid.set(x, y, self.get(self.get_cols()-1-x, y))
        return newgrid

    def flop(self):
        newgrid = Grid(self.get_cols(), self.get_rows())
        for y in range(self.get_rows()):
            for x in range(self.get_cols()):
                newgrid.set(x, y, self.get(x, self.get_rows()-1-y))
        return newgrid



def SubDividedGrid (Grid):
    pass

