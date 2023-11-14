from PyQt5 import QtCore
from plug.qt import Plug
from gizmo.utils import register
from tables import Quickmark as Table

class Quickmark(Plug):

    jumped=QtCore.pyqtSignal()
    marked=QtCore.pyqtSignal()
    unmarked=QtCore.pyqtSignal()

    def setup(self):

        super().setup()
        self.view=None
        self.functor=None
        self.table = Table() 
        self.ear.suffix_functor=self.set

    def set(self, event):

        key=event.text()
        if key and self.functor: 
            self.functor(key)
            return True

    @register('m', modes=['normal'])
    def setMark(self):

        if self.checkMode():
            self.activate()
            self.functor=self._mark

    @register('u', modes=['normal'])
    def undoMark(self):

        if self.checkMode():
            self.activate()
            self.functor=self._unmark

    @register('M', modes=['normal'])
    def gotoMark(self):

        if self.checkMode():
            self.activate()
            self.functor=self._goto

    def _unmark(self, m):

        ul=self.view.getUniqLocator()
        ul['mark']=m
        self.table.removeRow(ul)
        self.unmarked.emit()
        self.modeWanted.emit(self.mode)

    def _mark(self, m):

        ul=self.view.getUniqLocator()
        pl=self.view.getLocator(kind='position')
        ul.update(pl)
        ul['mark']=m
        self.table.writeRow(ul)
        self.marked.emit()
        self.modeWanted.emit(self.mode)

    def _goto(self, m):

        ul=self.view.getUniqLocator()
        ul['mark']=m
        rs=self.table.getRow(ul)
        if rs: 
            self.view.openLocator(
                    rs[0], 
                    kind='position')
        self.jumped.emit()
        self.modeWanted.emit(self.mode)

    def checkMode(self):

        m=self.app.moder.current
        if m:
            v=m.getView()
            if v and v.check('canPosition'):
                self.mode=m
                self.view=v
                return True
