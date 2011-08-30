import tempfile
import re

from twisted.python import log
from twisted.web import client
from twisted.internet import defer

from banjo import style
import ikcam.gfx.style
ikcam.gfx.style.Style = style.Style

from PIL import Image
from ikcam import plugin
from banjo import grid
from banjo.interface import ui

from fizzjik import rfid

__title__ = "Multi-threaded banjo dinosaur adventure 2D extreemeeeeee"



class IkCamPlugin (plugin.IkCamPluginBase):
    
    camera = False

    cellsize = 2

    def startService(self):
        self.timeoutValues = {'editing': 60}

        self.spriteGrid = grid.Grid(16, 16)
        self.setState("start")


    def registerObservers(self, hub):
        plugin.IkCamPluginBase.registerObservers(self, hub)
        hub.addObserver(rfid.TagAddedEvent, self.tagAdded)


    def enter_start(self):
        self.spriteGrid.clear()


    def tagAdded(self, e):
        tag = "urn:rfid:" + e.data

        if not self.api:
            self.error("Connect to AnyMeta site first.")
            return

        if self.state != "start":
            # cannot add tags while reviewing or snapshotting.
            return

        self.setState("loading")
        
        def ok(result):

            if not result:
                self.error("Unknown tag!")
                self.setState("start")
                return

            if 'name' in result:
                for k in ('first', 'full'):
                    if k in result['name'] and result['name'][k]:
                        result['the_name'] = result['name'][k]
                        break
            if 'the_name' not in result and 'text' in result:
                for k in ('title_short', 'title'):
                    if k in result['text'] and result['text'][k]:
                        result['the_name'] = result['text'][k]
                        break
            if 'the_name' not in result and 'title' in result and result['title']:
                result['the_name'] = result['title']

            if 'the_name' not in result or not result['the_name']:
                # Something went wrong with getting information;
                # Trust-view on profile might be less than members-only.
                self.error("Unknown tag..!")
                self.setState("start")
                return

            # strip HTML from title
            result['the_name'] = re.sub("<[^>]*>", "", result['the_name'])

            self.user = result
            d = self.loadAvatar(result)
            def ok(avatar):
                self.avatar = avatar
                self.setState("editing")
                print self.avatar

            d.addCallback(ok)


        def fail(f):
            msg = f.getErrorMessage()
            log.err(f)
            self.error(msg)
            self.setState("start")

        self.api.identity.identify(type='rfid', raw=tag).addCallback(ok).addErrback(fail)


    def avatarUniqueName(self):
        return  'BANJO_%s' % self.user['rsc_id']


    def validSprite(self):
        sil = grid.Grid.as_silhouette(self.spriteGrid)
        total = self.spriteGrid.get_cols()*self.spriteGrid.get_rows()
        fact = sil.count_pixels()/float(total)
        print fact
        return fact > 0.3


    def loadAvatar(self, res):

        d = self.api.anymeta.predicates.get(id=self.avatarUniqueName(), field=['text.title'])
        def ok(r):
            if r['result']['text.title']:
                # get the image
                url = self.api.entrypoint.replace("/services/rest/", "/image/" + r['result']['id'])
                print url

                fn = tempfile.mkstemp()[1]+".png"
                d2 = client.downloadPage(str(url),fn)
                def loadFile(_):
                    self.spriteGrid.fill_from_image(Image.open(fn), self.cellsize)
                    self.spriteGrid.invert()
                    print "YOOOOOOO"
                    return r['result']['id']
                d2.addCallback(loadFile)
                d2.addErrback(log.err)
                return d2
            else:
                return None

        d.addCallback(ok)
        d.addErrback(log.err)
        return d


    def saveAvatar(self):
        fn = tempfile.mkstemp()[1]+".png"
        self.spriteGrid.to_file(fn, self.cellsize)#, bg=(255,255,255), fg=(0,0,0)) # this makes it crash

        # delete previous avatar
        if self.avatar:
            print "*********** REPLACING", self.avatar
            d = self.api.anymeta.thing.update(thing_id=self.avatar, data={'symbolic_name': '', 'modifier_id': self.user['rsc_id']})
        else:
            d = defer.succeed(None)

        def upload(r):
            connect=[{'subject': 'SELF', 'predicate': 'AUTHOR', 'object': self.user['rsc_id']}]
            return self.api.anymeta.attachment.create(data="@"+fn, mime="image/png", title="%s's avatar" % self.user['the_name'],
                                                      connect=connect, modifier_id=self.user['rsc_id'])
        d.addCallback(upload)

        # set the symbolic name
        def update(r):
            id = r['thg_id']

            url = self.api.entrypoint.replace("/services/rest/", "/image/" + str(r['thg_id']))
            fp = open("/tmp/latest_avatars.txt", "a")
            fp.write(url+"\n")
            fp.close()

            print "*(**", id
            return self.api.anymeta.thing.update(thing_id=id, data={'symbolic_name': self.avatarUniqueName(), 'pubstate': 1, 'owner_id': self.user['rsc_id'], 'modifier_id': self.user['rsc_id']})

        d.addCallback(update)
        d.addErrback(log.err)
        return d


    def saveAndStop(self):
        self.setState("saving")
        d = self.saveAvatar()
        d.addErrback(log.err)
        d.addCallback(lambda _: self.setState('start'))


IkCamStagePlugin = ui.Stage
