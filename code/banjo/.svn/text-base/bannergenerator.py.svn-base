
from banjo.grid import Grid
from banjo.text import Font

f = Font("../art/pixelfonts/wired.txt")

g = Grid(64, 64)

g.line(0, "x ")
g.line(1, " x")
g.line(2, "xx")

avatar = Grid.from_file("samples/2.png", 20)
avatar.invert()
g.put(avatar, 24, 4)

#x,y = f.render(g, "WILLEM", (0,4))
#x,y = f.render(g, "VELTHOVEN", (0,y+1))

x,y = f.render(g, "TRAVIS", (0,22), center=True)
x,y = f.render(g, "GOODSPEED", (0,y+1), center=True)

y += 2

g.line(y+0, "xx")
g.line(y+1, " x")
g.line(y+2, "x ")

y += 5

f2 = Font("../art/pixelfonts/3x5.txt")
f2.render(g, "BEAT ARJAN ON", (0,y), center=True)
f2.render(g, "2010-11-20 22:00", (0,y+7))

y += 14

g.line(y+0, "x ")
g.line(y+1, " x")
g.line(y+2, "xx")

#g.to_file("/tmp/foo.png", 10)
g.to_file("/tmp/foo.bmp", 1, bitmap=True)
print g
