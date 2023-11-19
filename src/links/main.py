from plug.qt import Plug
from gizmo.utils import tag
from PyQt5 import QtCore, QtGui

class Links(Plug):

    key=''
    view=None
    links=None
    hinting=False
    selection=None
    listen_leader='<c-l>'
    leader_keys={'command': 'l'}
    linkSelected=QtCore.pyqtSignal()

    def event_functor(self, e, ear):

        if self.hinting and e.text():
            self.key+=e.text()
            self.view.updateHint(self.key)
            return True

    def listen(self):

        super().listen()
        self.view.hintSelected.connect(
                self.selectHinted)
        self.view.hintFinished.connect(
                self.selectHinted)
        self.hint()

    def delisten(self): 

        super().delisten()
        self.app.earman.clearKeys()
        self.view.hintSelected.disconnect(
                self.selectHinted)
        self.view.hintFinished.disconnect(
                self.selectHinted)
        self.cleanUp()

    def hint(self, data=None):

        self.hinting=True
        citem=self.view.currentItem()
        links=citem.getLinks()
        self.view.hint(links)

    def selectHinted(self, l=None):

        self.hinting=False
        if l: self.view.openLink(l)
        self.deactivate()

    def cleanUp(self):

        self.key=''
        self.view=None
        self.links=None
        self.hinting=False
        self.selection=None

    def checkLeader(self, e, p):

        c=self.app.moder.current
        if c and c.name=='normal':
            v=c.getView()
            cond=['hasLinks', 'canHint']
            if v and v.check(cond):
                self.view=v
                return True
