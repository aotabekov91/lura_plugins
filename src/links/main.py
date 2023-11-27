from plug.qt import Plug
from gizmo.utils import tag
from PyQt5 import QtCore, QtGui

class Links(Plug):

    isMode=True
    listen_leader='<c-l>'

    def event_functor(self, e, ear):

        if e.text():
            self.key+=e.text()
            self.view.updateHint(self.key)
            return True

    def activate(self):
        
        super().activate()
        self.view.hintSelected.connect(self.selectHinted)
        self.view.hintFinished.connect(self.selectHinted)
        self.hint()

    def octivate(self): 

        super().octivate()
        self.view.hintSelected.disconnect(self.selectHinted)
        self.view.hintFinished.disconnect(self.selectHinted)

    def hint(self, data=None):

        l=[]
        for i in self.view.visibleItems():
            l+=i.getLinks()
        if l: self.view.hint(l)

    def selectHinted(self, l=None):

        if l: self.view.openLink(l)
        self.octivate()

    def checkLeader(self, e, p):

        v=self.app.handler.view()
        c=['hasLinks', 'canHint']
        if v and self.checkProp(c, v):
            self.key=''
            self.view=v
            return True
