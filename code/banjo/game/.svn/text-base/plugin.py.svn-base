import tempfile
import re
import os
import time

from twisted.python import log
from twisted.web import client
from twisted.internet import reactor
#from twisted.internet import reactor

from anymeta.availability import base as avail


from banjo import style
import ikcam.gfx.style
ikcam.gfx.style.Style = style.Style

from ikcam import plugin, submit, events
from banjo.game import ui
from banjo import generator

from fizzjik import rfid

from banjo.game import managementTags

__title__ = "Multi-threaded banjo dinosaur adventure 2D extreemeeeeee"



class IkCamPlugin (plugin.IkCamPluginBase):

    cellsize = 20
    camera = False

    timeoutValues = {'wait2': 20,
                     'management': 60}

    tags = None
    participants = None

    title_template = None
    body_template = None

    event_id = None
    event_title = None

    default_node = None
    event_node = None

    submitter = None


    def startService(self):
        #self.sound = sound.SoundService()
        #reactor.callLater(0, self.sound.setServiceParent, self)
        self.setState("start")


    def registerObservers(self, hub):
        plugin.IkCamPluginBase.registerObservers(self, hub)
        hub.addObserver(rfid.TagAddedEvent, self.tagAdded)
        hub.addObserver(avail.AvailabilityChangedEvent, self.availabilityChanged)


    def enter_start(self):
        self.tags = []
        self.participants = {}
        self.setState("wait1")
        self.service.loadSettings() # reload the settings after each picture


    def tagAdded(self, e):
        tag = "urn:rfid:" + e.data
        print tag
        if not self.api:
            self.error("Connect to AnyMeta site first.")
            return

        if self.state == "management_print":
            self.error("Programming in progress!!")
            return

        if tag in managementTags:
            if self.state != "management":
                self.setState("management")
            return

        if self.state not in ["wait1", "wait2"]:
            # cannot add tags while reviewing or snapshotting.
            return
        if tag in self.tags:
            return

        self.tags.append(tag)

        def ok(result):
            if not result:
                self.error("Unknown tag!")
                del self.tags[self.tags.index(tag)]
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
                del self.tags[self.tags.index(tag)]
                return

            # strip HTML from title
            result['the_name'] = re.sub("<[^>]*>", "", result['the_name'])

            d = self.loadAvatar(result)
            def ok(avatar):
                if not avatar:
                    self.error("Make an avatar first!!")
                    del self.tags[self.tags.index(tag)]
                    return
                else:
                    result['avatar'] = avatar
                    self.participants[tag] = result
                    #self.setState("")
                    print "!!!!!!!!!!!!", self.tags, self.participants

                    if len(self.participants.keys()) == 1:
                        self.setState("wait2")
                    elif len(self.participants.keys()) == 2:
                        if self.state == "wait1":
                            self.setState("wait2")
                        self.setState("getready")
            d.addCallback(ok)


        def fail(f):
            msg = f.getErrorMessage()
            log.err(f)
            self.error(msg)
            self.setState("start")

        self.api.identity.identify(type='rfid', raw=tag).addCallback(ok).addErrback(fail)


    def avatarUniqueName(self, id):
        return  'BANJO_%s' % id


    def loadAvatar(self, res):
        d = self.api.anymeta.predicates.get(id=self.avatarUniqueName(res['rsc_id']), field=['text.title'])
        def ok(r):
            if r['result']['text.title']:
                # get the image
                url = self.api.entrypoint.replace("/services/rest/", "/image/" + r['result']['id'])

                fn = tempfile.mkstemp()[1]+".png"
                d2 = client.downloadPage(str(url),fn)
                def loadFile(_):
                    return fn
                d2.addCallback(loadFile)
                d2.addErrback(log.err)
                return d2
            else:
                return None

        d.addCallback(ok)
        d.addErrback(log.err)
        return d



    def enter_getready(self):
        if self.service.debug:
            self.setState("playing")
        else:
            self.setStateAfter("c3", 3)

    def enter_c3(self):
        self.setStateAfter("c2", 1)
    def enter_c2(self):
        self.setStateAfter("c1", 1)
    def enter_c1(self):
        self.setStateAfter("playing", 1)


    def enter_gameover(self):
        winner = self.participants[self.winner]['the_name']
        avatar = self.participants[self.winner]['avatar']
        loser = self.participants[self.loser]['the_name']

        try:
            png, bmp = generator.generateBanner(avatar, winner, loser)

            print "********", png
            png2 = os.getcwd()+"/"+png.replace(".png", "2.jpg")
            png2 = "/tmp/test.jpg"
            print "***2", png2

            os.system("mogrify -flip -flop %s" % bmp)


            os.system("convert %s -type TrueColor %s" % (png, png2))
            
            item = {'participants': self.participants, 'tags': self.tags, 'filename': png2, 'mime': 'image/jpeg', 'time': time.time(),
                    'title_template': self.title_template, 'body_template': self.body_template,
                    'event_id': self.event_id, 'event_title': self.event_title,
                    'default_node': self.default_node, 'event_node': self.event_node}

            self.submitter.submitItem(item)

            fp = open("../output/avatars.txt", "a")
            fp.write(str(bmp)+"\n")
            fp.close()

            self.parent.getServiceNamed("stage").showBanner(png)
        except Exception, e:
            self.error("Error generating...")
            log.err(e)

        self.setStateAfter("start", 20)


    def enter_management_print(self):
        # print!!!!
        target = self.gfx.bitmaps[self.gfx.currentKnitting]
        def go():
            cmd = "/home/mediamatic/work/banjo/code/printer/printfromgame.sh %s" % target
            print cmd
            os.system(cmd)
            self.setState("management_printed")
        reactor.callLater(0.5, go)


    def enter_management_printed(self):
        self.setStateAfter("start", 3)


    # IKCAM SUBMIT

    def setAPI(self, api):
        self.api = api
        if self.submitter:
            self.submitter.setAPI(self.api)
        else:
            self.submitter = submit.IkCamSubmitter(self.service.parent, self.api)



    def refreshEvent(self):
        def fail(f):
            self.event_title = None
            self.event_node = None
            e = events.IkCamEvent("event_change", self)
            self.service.parent.observe(e)

        def eventResult(r):
            if r:
                self.event_title = re.sub(r'<[^>]*?>', '', r['title'])
                self.event_node = "ikcam/by_event/%d" % int(self.event_id)
                e = events.IkCamEvent("event_change", self)
                self.service.parent.observe(e)
            else:
                fail(None)

        d = self.api.identity.identify(thg_id=self.event_id)
        d.addCallback(eventResult)
        d.addErrback(fail)


    def availabilityChanged(self, event):
        component = event.data
        if component.name == 'anymeta':
            if component.getState() == avail.OK:
                self.default_node = "ikcam/%d" % int(component.info['id'])
            else:
                self.default_node = None



    def settingsChanged(self, config):
        """
        Settings have come in from Anymeta. Put them in.
        """
        props = config['props']
        timing = props.get('timing', {})
        self.addextra_time = int(timing.get('addextra', 2))
        self.countdown_time = int(timing.get('countdown', 5))
        self.review_time = int(timing.get('review', 6))

        template = props.get('template', {})
        self.title_template = template.get('title', '%(names)s at %(event)s')
        self.body_template = template.get('text', 'This picture was taken with the [http://www.mediamatic.net/ikcam Mediamatic IkCam].')

        self.creates_report = props.get('createreport', 'no')

        self.keywords = config['keywords']

        self.site = config['site']

        if 'facebook' in config:
            self.facebook = config['facebook']
        else:
            self.facebook = False

        if 'event' in config:
            self.setEvent(config['event'])
        else:
            self.setEvent(False)



    def setEvent(self, event):
        if not event:
            self.event_id = None
            self.event_title = None
            self.event_node = None
            self.parent.observe(events.IkCamEvent("event_change", self))

        else:
            self.event_id = int(event['id'])
            self.event_title = re.sub(r'<[^>]*?>', '', event['title'])
            self.event_node = "ikcam/by_event/%d" % int(event['id'])
            self.parent.observe(events.IkCamEvent("event_change", self))



IkCamStagePlugin = ui.Stage
