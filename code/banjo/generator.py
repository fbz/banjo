import tempfile
import time
import random

from banjo.grid import Grid
from banjo.text import Font
from datetime import datetime

seq = 0


def generateBanner(avatar, winner, loser):
    
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    m = months[int(datetime.now().strftime("%m"),10)-1]
    stamp = datetime.now().strftime("%d "+m+" %H:%M")

    datetime.now().strftime("%Y-%m-%d %H:%M")

    dinos = ["gamedata/banjo3.png"]

    f = Font("gamedata/wired.txt")

    g = Grid(64, 64)

    g.line(0, "x ")
    g.line(1, " x")
    g.line(2, "xx")

    avatar = Grid.from_file(avatar, 2)
    avatar.invert()
    g.put(avatar, 24, 4)

    dino = Grid.from_file(random.choice(dinos), 1)
    dino.invert()
    if random.random()>.5:
        dino = dino.flip()
    if random.random()>.5:
        dino = dino.flop()
    g.put(dino, 3, 4)

    dino = Grid.from_file(random.choice(dinos), 1)
    dino.invert()
    g.put(dino, 64-dino.get_cols()-3, 4)


    y = 22
    l = unicode(winner.upper()).split(" ")
    l = [s.strip() for s in l]

    maxname = lambda name: len(name)<11 and name or name.replace(" ", "")[0:11]

    x,y = f.render(g, maxname(l[0]), (0,22), center=True)

    y += 2

    g.line(y+0, "xx")
    g.line(y+1, " x")
    g.line(y+2, "x ")

    y += 5

    loser = loser.split(" ")[0]

    f2 = Font("gamedata/3x5.txt")
    f2.render(g, u"BEAT %s" % loser.upper(), (0,y), center=True)
    f2.render(g, unicode(stamp), (0,y+7), center=True)

    y += 14

    g.line(61, "x ")
    g.line(62, " x")
    g.line(63, "xx")

    dinos = ["gamedata/dino_top2.png", "gamedata/dino_top5.png"]

    x = 3
    for t in range(6):
        dino = Grid.from_file(random.choice(dinos), 1)
        dino.invert()
        if random.random()>0.5:
            dino = dino.flip()
        g.put(dino, x, y)
        x += dino.get_cols()+1


    
    g.vline(0, "X ")
    g.vline(1, " X")
    g.vline(62, " X")
    g.vline(63, "X ")


    global seq
    if seq % 2 == 1:
        g.invert()
    seq += 1

    base = tempfile.mkstemp()[1]
    base = "../output/result-%d" % time.time()
    g.to_file(base+".png", 10, fg=(255,255,255,255), bg=(0,0,0,255))

    g = g.flip()
    g = g.flop()
    g.to_file(base+".bmp", 1, fg=(255,255,255), bg=(0,0,0),bitmap=True)
    return base+".png", base+".bmp"

