# Renders the title knitting for the banjo project.
# Arjan Scherpenisse <arjan@scherpenisse.net>, 2010

from banjo.grid import Grid
from banjo.text import Font

f = Font("../art/pixelfonts/wired.txt")

g = Grid(64, 64)

g.line(0, "xx")
g.line(1, "x ")
g.line(2, " x")
g.line(3, "xx")

y = 5

x,y = f.render(g, "MULTI-THREADED BANJO DINOSAUR KNITTING ADVENTURE 2D EXTREME!!!", (2,y+1))

y += 1

g.line(y+0, "xx")
g.line(y+1, " x")
g.line(y+2, "x ")
g.line(y+3, "xx")

#g.to_file("/tmp/foo.png", 10)
g.to_file("/tmp/foo.bmp", 1, bitmap=True)
print g
