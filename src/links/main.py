from plug.qt import Plug
from gizmo.utils import register
from PyQt5 import QtCore, QtGui

class Links(Plug):

    linkSelected=QtCore.pyqtSignal()

    def __init__(
            self,
            *args, 
            listen_leader='<c-l>',
            leader_keys={
                'command': 'l',
                },
            **kwargs
            ):

        super().__init__(
                *args,
                leader_keys=leader_keys,
                listen_leader=listen_leader,
                **kwargs
                )
        self.key=''
        self.view=None
        self.links=None
        self.hinting=False
        self.selection=None
        self.listenerAddKeys=self.ear.addKeys
        self.ear.addKeys=self.ownAddKeys

    def ownAddKeys(self, event):

        if self.hinting:
            t=event.text()
            if t:
                self.key+=t
                self.view.updateHint(self.key)
                event.accept()
                return True
        return self.listenerAddKeys(event)

    def listen(self):

        super().listen()
        self.view.hintSelected.connect(
                self.selectHinted)
        self.view.hintFinished.connect(
                self.selectHinted)
        self.hint()

    def delisten(self): 

        super().delisten()
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

    def checkLeader(self, event, pressed):

        if super().checkLeader(event, pressed):
            if self.ear.listening:
                return True
            c=self.app.moder.current
            if c and c.name=='normal':
                v=c.getView()
                cond=['hasLinks', 'canHint']
                if v and v.check(cond):
                    self.view=v
                    return True
        return False
