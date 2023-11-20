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

        t=self.app.moder.type()
        qmodel=self.getModel(t.view)
        if not qmodel: return
        ul=t.view.getUniqLocator()
        pl=t.view.getLocator(kind='position')
        ul.update(pl)
        ul['mark']=m
        qmodel.add(ul)
        self.marked.emit()

    def _goto(self, m):

        t=self.app.moder.type()
        qm=self.getModel(t.view)
        if not qm: return
        e=qm.find(m, 'mark')
        if not e: return
        t.view.openLocator(
                e.data(), 
                kind='position')
        self.jumped.emit()

    def getModel(self, v): 

        uid=v.getUniqLocator()
        uid['type']='quickmarks'
        return self.app.buffer.getModel(uid)

    def checkMode(self):

        t=self.app.moder.type()
        v=t.view
        if v and v.check('canLocate'):
            return True
