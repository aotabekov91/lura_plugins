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
            # ear.clearKeys()
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

        if self.checkMode():
            self.activate(self.mark)

    @tag('t', modes=['normal'])
    def gotoMark(self):

        if self.checkMode():
            self.activate(self.goto)

    def mark(self, m):

        v=self.app.handler.type()
        qm=self.getModel(v)
        if qm:
            ul=v.getUniqLocator()
            pl=v.getLocator(kind='position')
            ul.update(pl)
            ul['mark']=m
            qm.addElement(ul)
            self.marked.emit()

    def goto(self, m):

        t=self.app.handler.type()
        qm=self.getModel(t)
        if not qm: return
        e=qm.find(m, by='mark')
        if e:
            d=e.data()
            t.openLocator(d, kind='position')
            self.jumped.emit()

    def getModel(self, t):

        if not t: return
        if not t.model().isType: return
        b=self.app.buffer
        n=self.model_name
        s=self.source_name
        l=t.getUniqLocator()
        return b.getModel((l, n, s))

    def checkMode(self):

        p=self.check_props
        t=self.app.handler.type()
        return self.checkProp(p, t)
