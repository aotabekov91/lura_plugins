from PyQt5 import QtCore
from plug.qt import Plug
from gizmo.utils import tag

class Quickmark(Plug):

    isMode=True
    functor=None
    model_name='Quickmark'
    source_name='kind=table;'
    check_props=['canLocate']
    jumped=QtCore.pyqtSignal()
    marked=QtCore.pyqtSignal()
    unmarked=QtCore.pyqtSignal()

    def event_functor(self, e, ear):

        if e.text() and self.functor: 
            self.functor(e.text())
            self.octivate()
            return True

    def activate(self, functor):

        self.functor=functor
        super().activate()

    def octivate(self):

        self.functor=None
        super().octivate()

    @tag('m', modes=['normal'])
    def setMark(self):

        if self.checkType():
            self.activate(self.mark)

    @tag('M', modes=['normal'])
    def gotoMark(self):

        if self.checkType():
            self.activate(self.goto)

    def mark(self, m):

        t, tm=self.getModel()
        if tm:
            ul=t.getUniqLocator()
            pl=t.getLocator(kind='position')
            ul.update(pl)
            ul['mark']=m
            tm.addElement(ul)
            self.marked.emit()

    def goto(self, m):

        t, tm=self.getModel()
        if not tm: return
        e=tm.findElement(m, by='mark')
        if not e: return
        d=e.data()
        t.openLocator(d, kind='position')
        self.jumped.emit()

    def getModel(self, t=None):

        t=t or self.app.handler.type()
        if not t: return
        if not t.model().isType: return
        b=self.app.buffer
        n=self.model_name
        s=self.source_name
        l=t.getUniqLocator()
        return t, b.getModel((l, n, s))

    def checkType(self):

        p=self.check_props
        t=self.app.handler.type()
        return self.checkProp(p, t)
