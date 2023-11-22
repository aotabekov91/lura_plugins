from PyQt5 import QtCore
from gizmo.utils import tag

class CreateMixin:

    functor=None
    jumped=QtCore.pyqtSignal()
    marked=QtCore.pyqtSignal()
    unmarked=QtCore.pyqtSignal()

    def event_functor(self, e, ear):

        if self.functor and e.text():
            self.functor(e.text())
            ear.clearKeys()
            self.deactivate()
            return True

    def activate(self, functor):

        self.functor=functor
        super().activate()

    def deactivate(self):

        self.functor=None
        super().deactivate()

    @tag('m', modes=['normal'])
    def setMark(self):

        if self.checkView():
            self.activate(self.mark)

    @tag('t', modes=['normal'])
    def gotoMark(self):

        if self.checkView():
            self.activate(self.goto)

    def mark(self, m):

        v=self.checkView()
        if not v: return
        qm=self.getModel(v)
        if not qm: return
        ul=v.getUniqLocator()
        pl=v.getLocator(kind='position')
        ul.update(pl)
        ul['mark']=m
        qm.addElement(ul)
        self.deactivate()
        self.marked.emit()

    def goto(self, m):

        v=self.checkView()
        if not v: return
        qm=self.getModel(v)
        if not qm: return
        e=qm.findElement(m, by='mark')
        if not e: return
        k=self.locator_kind
        v.openLocator(e.data(), k)
        self.jumped.emit()
        self.deactivate()
