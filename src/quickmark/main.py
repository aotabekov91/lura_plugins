from PyQt5 import QtCore
from plug.qt import Plug
from gizmo.utils import tag

class Quickmark(Plug):

    functor=None
    delisten_on_exec=True
    jumped=QtCore.pyqtSignal()
    marked=QtCore.pyqtSignal()
    unmarked=QtCore.pyqtSignal()

    def event_functor(self, e, ear):

        if e.text() and self.functor: 
            self.functor(e.text())
            ear.clearKeys()
            self.deactivate()
            return True

    def activate(self, functor):

        self.functor=functor
        super().activate()

    @tag('m', modes=['normal'])
    def setMark(self):

        if self.checkMode():
            self.activate(self._mark)

    @tag('M', modes=['normal'])
    def gotoMark(self):

        if self.checkMode():
            self.activate(self._goto)

    def _mark(self, m):

        v=self.app.moder.type()
        qm=self.getModel(v)
        if not qm: return
        ul=v.getUniqLocator()
        pl=v.getLocator(kind='position')
        ul.update(pl)
        ul['mark']=m
        qm.add(ul)
        self.marked.emit()

    def _goto(self, m):

        v=self.app.moder.type()
        ul=v.getUniqLocator()
        ul['mark']=m
        qm=self.getModel(v)
        if not qm: return
        d=qm.get(ul)
        if not d: return
        v.openLocator(
                d=[0], kind='position')
        self.jumped.emit()

    def getModel(self, v): 

        uid=v.getUniqLocator()
        uid['type']='quickmarks'
        return self.app.buffer.getModel(uid)

    def checkMode(self):

        v=self.app.moder.type()
        if v and v.check('canLocate'):
            return True
